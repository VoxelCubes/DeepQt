import hashlib
import re
from dataclasses import dataclass, field
from enum import IntEnum
from functools import partial
from pathlib import Path

from deepqt import trie


class ProcessLevel(IntEnum):
    # Represent the values in bit increments, so that gloss_prot = gloss | prot
    Error = -1
    RAW = 0
    GLOSSARY = 1
    PROTECTED = 2
    GLOSSARY_PROTECTED = 3


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
    def char_count(self):
        return None


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
        return len(self.current_text())

    def get_translated_text(self) -> str | None:
        if self.translation:
            return self.translation
        elif self.translation_chunks:
            return incomplete_translation_banner() + "".join(self.translation_chunks)
        else:
            return None

    def translation_incomplete(self):
        return self.translation_chunks and not self.translation


def incomplete_translation_banner() -> str:
    return """
#==============================#

     INCOMPLETE TRANSLATION

#==============================#

"""


@dataclass(slots=True)
class XMLFile(TextFile):
    """
    XML files don't support quote protection.
    """


@dataclass(slots=True)
class EpubFile(InputFile):
    """
    Epub file support works by unzipping the file to a cache directory and then
    processing the html and toc files like text files.
    """

    cache_dir: Path = field(default_factory=Path)
    xml_files: list[XMLFile] = field(default_factory=list)

    def __post_init__(self):
        raise NotImplementedError("Epub files are not yet supported.")

    @property
    def char_count(self):
        return sum(f.char_count for f in self.xml_files)


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
