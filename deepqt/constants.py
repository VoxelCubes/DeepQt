from enum import Enum, StrEnum


class Command(Enum):
    NONE = None
    FILES = "files"
    TEXT = "text"
    CLIPBOARD = "clipboard"


class Backend(StrEnum):
    MOCK = "mock"  # Mocking a reliable backend.
    MOCK_LLM = "mock_llm"  # Mocking an unreliable backend.
    DEEPL = "deepl"


debug_backends = [Backend.MOCK, Backend.MOCK_LLM]


class Formats(Enum):
    TEXT = "txt"  # Plain text
    EPUB = "epub"  # Ebook format
    PDF = "pdf"  # Portable Document Format
    DOCX = "docx"  # Microsoft Word Document
    PPTX = "pptx"  # Microsoft PowerPoint Document
    XLSX = "xlsx"  # Microsoft Excel Document
    HTML = "html"  # HTML Document
    XLF = "xlf;xliff"  # XLIFF Document
