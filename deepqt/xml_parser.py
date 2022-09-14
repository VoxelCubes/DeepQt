import re
import warnings
import zipfile
from functools import cache
from pathlib import Path

import minify_html
from bs4 import BeautifulSoup
from logzero import logger
from lxml import etree


# It throws this erroneous warning when encountering xhtml, which may be found in epubs.
warnings.filterwarnings("ignore", category=UserWarning, module="bs4")


def prepare_html_text(text: str, nuke_ruby: bool, nuke_indents: bool, nuke_kobo: bool, crush_html_text: bool) -> str:
    """
    Prepares the raw XML text.
    Apply heuristics to shrink the size.
    """

    # Perform raw text manipulations.
    if nuke_ruby:
        text = bust_ruby_tags(text)
    if nuke_indents:
        text = flatten_indents(text)

    # Perform parsed element manipulations.
    soup = BeautifulSoup(text, "lxml")
    if nuke_kobo:
        soup = strip_kobo_spans(soup)

    # Perform this one either way.
    soup = bust_empty_spans(soup)

    # Convert back to text.
    text = str(soup)

    # Minify the html last.
    if crush_html_text:
        text = crush_html(text)

    return text


def strip_kobo_spans(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Strip spans that Kobo adds to the html.
    These have the class "koboSpan".
    This means removing all attributes from the span tags, rendering them empty.
    Empty spans are removed by the html cleaner later on.
    """
    logger.debug("Neutering Kobo spans")

    for span in soup.find_all("span", class_="koboSpan"):
        span.attrs.clear()

    return soup


def bust_empty_spans(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Remove empty spans from the text.
    """
    logger.debug("Busting attribute-less spans")

    for span in soup.find_all("span"):
        if not span.attrs:
            span.replace_with_children()

    return soup


def flatten_indents(text: str) -> str:
    """
    Flatten all indents.
    """
    logger.debug("Flattening indents")
    indent = re.compile(r"^\s+", re.MULTILINE)
    return indent.sub("", text)


def crush_html(raw_html: str) -> str:
    """
    Minify the html.
    """

    return minify_html.minify(
        raw_html,
        do_not_minify_doctype=True,
        ensure_spec_compliant_unquoted_attribute_values=True,
        keep_spaces_between_attributes=True,
    )


def bust_ruby_tags(text: str) -> str:
    """
    Remove ruby tags from the text.
    """
    # Skip this if the text doesn't claim to be Japanese.
    if not re.search(r'lang="ja"', text):
        return text

    lines = [deruby(line) for line in text.splitlines()]
    return "\n".join(lines)


def html_contains_text(html: str) -> bool:
    """
    Check if the html contains any text.
    """
    soup = BeautifulSoup(html, "lxml")
    # Exclude the title.
    text = soup.find("body").text.strip()
    return bool(text)


# This is an expensive pure function, taking around 300ms to run for an entire epub.
# When loading multiple epubs, each one triggers a recount when updating parameters.
# So cache results for a massive speed up: 300ms -> 0.02ms: 15,000x speed up.
@cache
def get_char_count(html: str) -> int:
    """
    Get the number of characters in the html.
    """
    soup = BeautifulSoup(html, "lxml")
    return len(
        soup.text,
    )


def deruby(line: str) -> str:
    """
    Converts this:
    <ruby><rb>皇</rb><rt>こう</rt><rb>室</rb><rt>しつ</rt><rb>典</rb><rt>てん</rt><rb>範</rb><rt>ぱん</rt></ruby>
    To this:
    皇室典範（こうしつてんぱん）

    Works on html files.

    :param line: The line to process.
    :return: The processed line.
    """
    # Skip this if the line doesn't contain ruby tags.
    if "<ruby>" not in line:
        return line
    else:
        states = {"ruby": "start", "/ruby": "end", "rb": "main", "/rb": "main", "rt": "ruby", "/rt": "main"}
        tag = ""
        out = ""
        main = ""
        ruby = ""
        cstate = "normal"
        reading_tag = False

        for char in line:
            if char == "<":  # New tag
                tag = ""
                reading_tag = True

            elif char == ">":  # Evaluate tag
                reading_tag = False
                if tag in states:
                    cstate = states[tag]
                    if cstate == "start":  # Ruby opened
                        # clear current strings
                        main = ""
                        ruby = ""
                        cstate = "main"
                    if cstate == "end":  # Ruby closed
                        # paste back untangled rubytext
                        out += f"{main}（{ruby}）"
                        cstate = "normal"
                else:
                    # leave tag untouched
                    out += f"<{tag}>"

            else:
                if not reading_tag:
                    if cstate == "normal":
                        out += char
                    elif cstate == "main":
                        main += char
                    elif cstate == "ruby":
                        ruby += char
                else:
                    tag += char

        return out


####################################################################################################
#
#  Code below taken and modified from Alamot
#  https://alamot.github.io/epub_cover/
#  License: Unlicense
#
####################################################################################################


def get_epub_cover(epub_path: str | Path) -> Path | None:
    """
    Return the cover image file from an epub archive.

    :param epub_path: The path to the epub file.
    :return: The path to the cover image file, if one was found.
    """

    # Let's define the required XML namespaces
    namespaces = {
        "calibre": "http://calibre.kovidgoyal.net/2009/metadata",
        "dc": "http://purl.org/dc/elements/1.1/",
        "dcterms": "http://purl.org/dc/terms/",
        "opf": "http://www.idpf.org/2007/opf",
        "u": "urn:oasis:names:tc:opendocument:xmlns:container",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xhtml": "http://www.w3.org/1999/xhtml",
    }

    # We open the epub archive using zipfile.ZipFile():
    with zipfile.ZipFile(epub_path) as z:

        # We load "META-INF/container.xml" using lxml.etree.fromString():
        t = etree.fromstring(z.read("META-INF/container.xml"))
        # We use xpath() to find the attribute "full-path":
        """
        <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
          <rootfiles>
            <rootfile full-path="OEBPS/content.opf" ... />
          </rootfiles>
        </container>
        """
        rootfile_path = t.xpath("/u:container/u:rootfiles/u:rootfile", namespaces=namespaces)[0].get("full-path")
        logger.debug("Path of root file found: " + rootfile_path)

        # We load the "root" file, indicated by the "full_path" attribute of "META-INF/container.xml", using lxml.etree.fromString():
        t = etree.fromstring(z.read(rootfile_path))

        cover_href = None
        try:
            # For EPUB 2.0, we use xpath() to find a <meta>
            # named "cover" and get the attribute "content":
            """
            <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
              ...
              <meta content="my-cover-image" name="cover"/>
              ...
            </metadata>"""

            cover_id = t.xpath("//opf:metadata/opf:meta[@name='cover']", namespaces=namespaces)[0].get("content")
            logger.debug("ID of cover image found: " + cover_id)
            # Next, we use xpath() to find the <item> (in <manifest>) with this id
            # and get the attribute "href":
            """
            <manifest>
                ...
                <item id="my-cover-image" href="images/978.jpg" ... />
                ... 
            </manifest>
            """
            cover_href = t.xpath("//opf:manifest/opf:item[@id='" + cover_id + "']", namespaces=namespaces)[0].get(
                "href"
            )
        except IndexError:
            pass

        if not cover_href:
            # For EPUB 3.0, We use xpath to find the <item> (in <manifest>) that
            # has properties='cover-image' and get the attribute "href":
            """
            <manifest>
              ...
              <item href="images/cover.png" id="cover-img" media-type="image/png" properties="cover-image"/>
              ...
            </manifest>
            """
            try:
                cover_href = t.xpath("//opf:manifest/opf:item[@properties='cover-image']", namespaces=namespaces)[
                    0
                ].get("href")
            except IndexError:
                pass

        if not cover_href:
            # Some EPUB files do not declare explicitly a cover image.
            # Instead, they use an "<img src=''>" inside the first xhmtl file.
            try:
                # The <spine> is a list that defines the linear reading order
                # of the content documents of the book. The first item in the
                # list is the first item in the book.
                """
                <spine toc="ncx">
                  <itemref idref="cover"/>
                  <itemref idref="nav"/>
                  <itemref idref="s04"/>
                </spine>
                """
                cover_page_id = t.xpath("//opf:spine/opf:itemref", namespaces=namespaces)[0].get("idref")
                # Next, we use xpath() to find the item (in manifest) with this id
                # and get the attribute "href":
                cover_page_href = t.xpath(
                    "//opf:manifest/opf:item[@id='" + cover_page_id + "']", namespaces=namespaces
                )[0].get("href")
                # In order to get the full path for the cover page,
                # we have to join rootfile_path and cover_page_href:
                cover_page_path = Path(rootfile_path).parent / cover_page_href
                logger.debug(f"Path of cover page found: {cover_page_path}")
                # We try to find the <img> and get the "src" attribute:
                t = etree.fromstring(z.read(cover_page_path))
                cover_href = t.xpath("//xhtml:img", namespaces=namespaces)[0].get("src")
            except IndexError:
                pass

        if not cover_href:
            logger.warning("Cover image not found.")
            return None

        # In order to get the full path for the cover image,
        # we have to join rootfile_path and cover_href:
        cover_path = Path(rootfile_path).parent / cover_href
        logger.debug(f"Path of cover image found: {cover_path}")

        # We return the image path
        return Path(cover_path)
