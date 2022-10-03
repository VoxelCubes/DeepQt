import hashlib
import re
import zipfile
from dataclasses import dataclass, field
from enum import IntEnum
from functools import partial, cache
from pathlib import Path

from logzero import logger

import deepqt.helpers as hp
from deepqt import trie
from deepqt import xml_parser


class ProcessLevel(IntEnum):
    # Represent the values in bit increments, so that gloss_prot = gloss | prot
    Error = -1
    RAW = 0
    GLOSSARY = 1
    PROTECTED = 2
    GLOSSARY_PROTECTED = 3
    TRANSLATED = 4  # Only used for dumping.


@dataclass(slots=True)
class InputFile:
    path: Path
    locked: bool = False
    finished: bool = False
    glossary_hash: str = ""  # To Prevent re-applying the same glossary.

    def __post_init__(self):
        """
        Ensure the path exists.
        """
        if not self.path.exists():
            raise FileNotFoundError(f"File {self.path} does not exist.")

    def translation_incomplete(self):
        pass

    @property
    def char_count(self) -> int:
        raise NotImplementedError

    @property
    def is_translated(self) -> bool:
        raise NotImplementedError

    def clear_translations(self):
        raise NotImplementedError


@dataclass(slots=True)
class TextFile(InputFile):
    text: str = ""
    text_glossary: str = ""
    text_protected: str = ""
    text_glossary_protected: str = ""
    process_level: ProcessLevel = ProcessLevel.RAW
    text_chunks: list[str] = field(default_factory=list)
    translation_chunks: list[str] = field(default_factory=list)
    translation: str = ""

    def __post_init__(self):
        InputFile.__post_init__(self)
        with self.path.open("r", encoding="utf8") as f:
            self.text = f.read()

    def current_text(self):
        match self.process_level:
            case ProcessLevel.RAW:
                return self.text
            case ProcessLevel.GLOSSARY:
                return self.text_glossary
            case ProcessLevel.PROTECTED:
                return self.text_protected
            case ProcessLevel.GLOSSARY_PROTECTED:
                return self.text_glossary_protected

    @property
    def char_count(self):
        # Use caching to speed up the process, since the text doesn't change often, but can be very long.
        return text_length(self.current_text())

    def get_translated_text(self) -> str | None:
        if self.translation:
            return self.translation
        elif self.translation_chunks:
            return incomplete_translation_banner() + "".join(self.translation_chunks)
        else:
            return None

    def translation_incomplete(self):
        return self.translation_chunks and not self.translation

    @property
    def is_translated(self) -> bool:
        return bool(self.translation)

    def clear_translations(self):
        self.translation = ""
        self.translation_chunks = []


@cache
def text_length(text: str) -> int:
    """
    Simple wrapper to take advantage of caching.
    """
    return len(text)


def incomplete_translation_banner() -> str:
    return """
#==============================#

     INCOMPLETE TRANSLATION

#==============================#

"""


@dataclass(slots=True)
class CSSFile:
    path: Path
    text: str = ""

    def __post_init__(self):
        with self.path.open("r", encoding="utf8") as f:
            self.text = f.read()


@dataclass(slots=True)
class XMLFile:
    """
    XML files don't support quote protection.
    """

    path: Path
    text: str = ""
    text_glossary: str = ""
    process_level: ProcessLevel = ProcessLevel.RAW
    translation: str = ""

    def __post_init__(self):
        with self.path.open("r", encoding="utf8") as f:
            self.text = f.read()

    def prepare_text(self, *args, **kwargs):
        pass

    def current_text(self):
        match self.process_level:
            case ProcessLevel.RAW:
                return self.text
            case ProcessLevel.GLOSSARY:
                return self.text_glossary

    @property
    def char_count(self):
        return xml_parser.get_char_count(self.current_text())

    def get_translated_text(self) -> str | None:
        if self.translation:
            return self.translation
        else:
            return None

    @property
    def is_translated(self) -> bool:
        return bool(self.translation)

    def clear_translations(self):
        self.translation = ""


@dataclass(slots=True)
class HTMLFile(XMLFile):
    def prepare_text(self, nuke_ruby: bool, nuke_indents: bool, nuke_kobo: bool, crush_html: bool):
        # Apply heuristic improvements to html files.
        len_before = len(self.text)

        self.text = xml_parser.prepare_html_text(self.text, nuke_ruby, nuke_indents, nuke_kobo, crush_html)

        logger.debug(f"Cleaned {self.path.name}, {len_before} -> {len(self.text)}, diff: {len_before - len(self.text)}")


@dataclass(slots=True)
class TocNCXFile(XMLFile):
    """
    The NCX file is a special XML file that contains the table of contents.
    It isn't a standard HTML file, so it needs to be handled separately.
    Its text is contained within <text> tags.
    """

    @staticmethod
    def get_texts(xml: str) -> list[str]:
        # Find the contents of the <text> tags.
        return [match.group(1) for match in re.finditer(r"<text>\s*(.*?)\s*</text>", xml, re.DOTALL)]

    @staticmethod
    def set_texts(xml: str, texts: list[str]) -> str:
        # Replace the contents of the <text> tags in order.
        return re.sub(r"<text>.*?</text>", lambda m: f"<text>{texts.pop(0)}</text>", xml, re.DOTALL)

    @property
    def char_count(self):
        return sum(len(text) for text in self.get_texts(self.text))


@dataclass(slots=True)
class EpubFile(InputFile):
    """
    Epub file support works by unzipping the file to a cache directory and then
    processing the html and toc files like text files.
    """

    cache_dir: Path | None = None
    html_files: list[HTMLFile] = field(default_factory=list)
    css_files: list[CSSFile] = field(default_factory=list)
    toc_file: TocNCXFile | None = None
    initialized: bool = False
    cover_image: Path | None = None

    def __post_init__(self):
        InputFile.__post_init__(self)
        self.cache_dir = Path(self.cache_dir) / self.path.stem
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def initialize_files(
        self,
        nuke_ruby: bool,
        nuke_indents: bool,
        nuke_kobo: bool,
        crush_html: bool,
        make_text_horizontal: bool,
        ignore_empty: bool,
    ):
        """
        Apply heuristic improvements to html files.
        """

        if self.initialized:
            return

        logger.debug(f"Initializing {self.path.name}...")

        self.html_files, self.css_files, self.toc_file, self.cover_image = extract_epub(self.path, self.cache_dir)

        # Ignore files that contain no actual text (tags aside).
        logger.debug(f"Found {len(self.html_files)} html files in {self.path}")

        if ignore_empty:
            self.html_files = [file for file in self.html_files if xml_parser.html_contains_text(file.text)]
            logger.debug(f"Found {len(self.html_files)} html files with text in {self.path}")

        # Sort the html files by file name.
        self.html_files.sort(key=lambda f: f.path.name)

        for html_file in self.html_files:
            html_file.prepare_text(nuke_ruby, nuke_indents, nuke_kobo, crush_html)

        if make_text_horizontal:
            logger.debug(f"Making text horizontal in {self.path.name}...")
            for css_file in self.css_files:
                css_file.text = re.sub(r"writing-mode:\s*vertical-rl;", "writing-mode: horizontal-tb;", css_file.text)

        self.initialized = True

    @property
    def char_count(self):
        return sum(f.char_count for f in self.html_files)

    @property
    def process_level(self):
        if all(f.process_level == ProcessLevel.GLOSSARY for f in self.html_files):
            return ProcessLevel.GLOSSARY
        else:
            return ProcessLevel.RAW

    @process_level.setter
    def process_level(self, value):
        for f in self.html_files:
            f.process_level = value

    def translation_incomplete(self):
        # Return true, if some, but not all, are translated.
        all_translated = all(f.is_translated for f in self.html_files)
        any_translated = any(f.is_translated for f in self.html_files)
        return any_translated and not all_translated

    def is_translated(self) -> bool:
        return all(f.is_translated for f in self.html_files)

    @property
    def file_count(self):
        return len(self.html_files) + 1  # +1 for the toc file.

    def write_to_cache(self, process_level: ProcessLevel):
        """
        Write the current text of the given process level to the cache folder.
        """
        self.html_files: list[XMLFile]
        self.toc_file: XMLFile

        xml_files: list[XMLFile] = [self.toc_file] + self.html_files
        for xml_file in xml_files:
            if process_level == ProcessLevel.RAW:
                text = xml_file.text
            elif process_level == ProcessLevel.GLOSSARY:
                text = xml_file.text_glossary
            elif process_level == ProcessLevel.TRANSLATED:
                text = xml_file.translation
            else:
                raise ValueError(f"Invalid process level: {process_level}")

            xml_file.path.write_text(text, encoding="utf8")

        for css_file in self.css_files:
            css_file.path.write_text(css_file.text, encoding="utf8")

    def write(self, process_level: ProcessLevel, output_path: Path):
        """
        Write the current text of the given process level to the output file.

        :param process_level: The process level to write. Options are RAW, GLOSSARY, and TRANSLATED.
        :param output_path: The path to write the file to.
        """
        self.write_to_cache(process_level)
        # Rebuild the epub file.
        hp.zip_folder_to_epub(self.cache_dir, output_path)

    def clear_translations(self):
        for f in self.html_files:
            f.clear_translations()
        self.toc_file.clear_translations()


def extract_epub(epub_path: Path, cache_dir: Path) -> tuple[list[HTMLFile], list[CSSFile], TocNCXFile, Path | None]:
    """
    Extract the epub file to the cache directory and return a list of XMLFile
    objects representing the html files.
    """
    logger.debug(f"Extracting {epub_path} to {cache_dir}")

    with zipfile.ZipFile(epub_path, "r") as epub_zip:
        epub_zip.extractall(cache_dir)

    html_files = []
    css_files = []
    toc_file = None
    # Find .html and .toc files in all subfolders.
    for xml_path in cache_dir.glob("**/*"):
        if xml_path.suffix in (".html", ".xhtml"):
            html_files.append(HTMLFile(xml_path))
        elif xml_path.suffix == ".css":
            css_files.append(CSSFile(xml_path))
        elif xml_path.suffix == ".ncx":
            toc_file = TocNCXFile(xml_path)

    if not toc_file:
        raise ValueError(f"No table of contents toc.ncx file found in {epub_path}. This isn't a valid epub file.")

    # Find cover of the epub using the metadata.
    cover_image = xml_parser.get_epub_cover(epub_path)
    logger.debug(f"Found cover image {cover_image} in {epub_path}")

    logger.debug(f"Extracted {len(html_files)} html and toc files.")
    return html_files, css_files, toc_file, cover_image


@dataclass(slots=True)
class Glossary:
    """
    This type of glossary contains various types of entries, some providing more power than simple exact replacements.
    Each type consists of a dict that maps the input pattern to the substitution.
    Along with each dict, there is an optimized regex pattern that is used to match the input.
    All patterns, except regex and "no suffix" will append an additional space to the end of the substitution.
    Patterns making use of whitespace may be written like /pattern/ to
    prevent spreadsheet software from stripping it out.

    The glossary hash is an md5 hash of the glossary file.

    Following mappings are supported, with the symbol denoting the type: (applied in order)
    - exact: # Context free substitution.
    - regex: : Regular expression substitution. Warning: these cannot be optimized and are slower.
    - honorific $ Honorifics must be preceded by the pattern "[a-z] "
    - titles: ! Titles must be followed by the pattern " [A-Z]"
    - no suffix: | Don't append a space after successfully matching the pattern.
    - post terms: ~ These replacements are made last.
    """

    exact_terms: dict[str, str] = field(default_factory=dict)
    regex_terms: dict[str, str] = field(default_factory=dict)
    honorific_terms: dict[str, str] = field(default_factory=dict)
    title_terms: dict[str, str] = field(default_factory=dict)
    post_terms: dict[str, str] = field(default_factory=dict)
    no_suffix_terms: dict[str, str] = field(default_factory=dict)

    # Prefill the regex terms with a pattern that will never match.
    dummy_pattern = partial(re.compile, "^\b$")
    exact_pattern: re.Pattern = field(default_factory=dummy_pattern)
    honorific_pattern: re.Pattern = field(default_factory=dummy_pattern)
    title_pattern: re.Pattern = field(default_factory=dummy_pattern)
    post_pattern: re.Pattern = field(default_factory=dummy_pattern)
    no_suffix_pattern: re.Pattern = field(default_factory=dummy_pattern)

    hash: str = ""  # To Prevent re-applying the same glossary.

    def generate_patterns(self):
        """
        Generate the regex patterns from the dictionaries.
        """

        if self.exact_terms:
            self.exact_pattern = trie.trie_regex_from_words(self.exact_terms.keys())

        if self.honorific_terms:
            self.honorific_pattern = trie.trie_regex_from_words(
                self.honorific_terms.keys(), prefix=r"([a-z]) (", suffix=")"
            )
        if self.title_terms:
            self.title_pattern = re.compile("|".join(self.title_terms.keys()) + "[A-Z]")
        if self.post_terms:
            self.post_pattern = trie.trie_regex_from_words(self.post_terms.keys())
        if self.no_suffix_terms:
            self.no_suffix_pattern = trie.trie_regex_from_words(self.no_suffix_terms.keys())

    def set_hash(self, path: Path):
        """
        Set the glossary hash to the md5 hash of the glossary file.
        """
        with path.open("rb") as f:
            self.hash = hashlib.md5(f.read()).hexdigest()

    def is_same_glossary(self, path: Path):
        """
        Check if the glossary file is the same as the one already applied.
        """
        return self.hash == hashlib.md5(path.read_bytes()).hexdigest()

    def __len__(self):
        """
        Return the number of terms in the glossary.
        Sum up the values in each of the dictionaries.
        """
        return sum(
            len(d)
            for d in (
                self.exact_terms,
                self.regex_terms,
                self.honorific_terms,
                self.title_terms,
                self.post_terms,
                self.no_suffix_terms,
            )
        )

    def is_valid(self):
        """
        Check if the glossary is valid.
        It needs a file hash showing it isn't the uninitialized glossary,
        and it needs to have at least one term.
        """
        return self.hash != "" and len(self) > 0

    def __str__(self):
        """
        Print the glossary with each term on it's own line, divided into the different groups.
        """
        return "\n".join(
            f"{key}: {value}"
            for d in (
                {"exact terms": "--------------------"},
                self.exact_terms,
                {"regex terms": "--------------------"},
                self.regex_terms,
                {"honorific terms": "----------------"},
                self.honorific_terms,
                {"title terms": "--------------------"},
                self.title_terms,
                {"post terms": "---------------------"},
                self.post_terms,
                {"no suffix terms": "----------------"},
                self.no_suffix_terms,
            )
            for key, value in d.items()
        )
