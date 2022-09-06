import re
from bs4 import BeautifulSoup
import minify_html

from logzero import logger


def strip_kobo_spans(raw_html: str) -> str:
    """
    Strip spans that Kobo adds to the html.
    These have the class "koboSpan".
    This means removing all attributes from the span tags, rendering them empty.
    Empty spans are removed by the html cleaner later on.
    """
    logger.debug("Neutering Kobo spans")

    soup = BeautifulSoup(raw_html, "lxml")

    for span in soup.find_all("span", class_="koboSpan"):
        span.attrs.clear()

    return str(soup)


def bust_empty_spans(text: str) -> str:
    """
    Remove empty spans from the text.
    """

    soup = BeautifulSoup(text, "lxml")

    for span in soup.find_all("span"):
        if not span.attrs:
            span.replace_with_children()

    return str(soup)


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
