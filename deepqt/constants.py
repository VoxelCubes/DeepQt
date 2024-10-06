from enum import Enum, StrEnum, auto
from typing import Sequence, NewType

from attrs import frozen

# Create a new type for percentages as floats. These are between 0 and 100.
Percentage = NewType("Percentage", float)

Milliseconds = NewType("Milliseconds", int)

Seconds = NewType("Seconds", int)

SecondsF = NewType("Seconds", float)

APIKey = NewType("APIKey", str)

HTML = NewType("HTML", str)


class TranslationMode(StrEnum):
    Text = "Text"
    File = "File"


class Command(Enum):
    NONE = None
    FILES = "files"
    TEXT = "text"
    CLIPBOARD = "clipboard"


class Backend(StrEnum):
    MOCK = "MOCK"  # Mocking a reliable backend.
    # MOCK_LLM = "MOCK_LLM"  # Mocking an unreliable backend.
    DEEPL = "DEEPL"


# debug_backends = [Backend.MOCK, Backend.MOCK_LLM]
debug_backends = [Backend.MOCK]


@frozen
class FileType:
    name: str
    extensions: Sequence[str]
    mimetype: str


class Formats(Enum):
    TEXT = FileType("Plain text", (".txt",), "text/plain")
    EPUB = FileType("EPUB", (".epub",), "application/epub+zip")
    PDF = FileType("PDF", (".pdf",), "application/pdf")
    DOCX = FileType(
        "Word",
        (".docx",),
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    ODT = FileType("OpenDocument", (".odt",), "application/vnd.oasis.opendocument.text")
    PPTX = FileType(
        "PowerPoint",
        (".pptx",),
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )
    ODP = FileType(
        "OpenDocument Presentation", (".odp",), "application/vnd.oasis.opendocument.presentation"
    )
    XLSX = FileType(
        "Excel", (".xlsx",), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    ODS = FileType(
        "OpenDocument Spreadsheet", (".ods",), "application/vnd.oasis.opendocument.spreadsheet"
    )
    HTML = FileType("HTML", (".html",), "text/html")
    XLF = FileType(
        "XLIFF", (".xlf", ".xliff"), "application/x-xliff+xml"
    )  # May be recognized as just XML.
    UNKNOWN = FileType("Unknown", (), "")


# Reverse indexes.
mime_to_format = {fmt.value.mimetype: fmt for fmt in Formats}
extension_to_format = {ext: fmt for fmt in Formats for ext in fmt.value.extensions}
