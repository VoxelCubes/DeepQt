from tests.helpers import mock_file_path
from pathlib import Path

import deepqt.utils as ut
import deepqt.constants as ct
from tests.mock_files import mime_types


def test_mime_recognition():
    path = mock_file_path("text.txt", module=mime_types)
    assert ut.read_mime_type(path) == ct.Formats.TEXT, "Text file not recognized."

    path = mock_file_path("book.epub", module=mime_types)
    assert ut.read_mime_type(path) == ct.Formats.EPUB, "EPUB file not recognized."

    path = mock_file_path("document.pdf", module=mime_types)
    assert ut.read_mime_type(path) == ct.Formats.PDF, "PDF file not recognized."

    path = mock_file_path("writer.odt", module=mime_types)
    assert ut.read_mime_type(path) == ct.Formats.ODT, "ODT file not recognized."

    path = mock_file_path("word.docx", module=mime_types)
    assert ut.read_mime_type(path) == ct.Formats.DOCX, "DOCX file not recognized."

    path = mock_file_path("impress.odp", module=mime_types)
    assert ut.read_mime_type(path) == ct.Formats.ODP, "ODP file not recognized."

    path = mock_file_path("powerpoint.pptx", module=mime_types)
    assert ut.read_mime_type(path) == ct.Formats.PPTX, "PPTX file not recognized."

    path = mock_file_path("calc.ods", module=mime_types)
    assert ut.read_mime_type(path) == ct.Formats.ODS, "ODS file not recognized."

    path = mock_file_path("excel.xlsx", module=mime_types)
    assert ut.read_mime_type(path) == ct.Formats.XLSX, "XLSX file not recognized."

    path = mock_file_path("website.html", module=mime_types)
    assert ut.read_mime_type(path) == ct.Formats.HTML, "HTML file not recognized."

    path = mock_file_path("translation.xliff", module=mime_types)
    assert ut.read_mime_type(path) == ct.Formats.XLF, "XLF file not recognized."

    path = mock_file_path("archive.zip", module=mime_types)
    assert ut.read_mime_type(path) == ct.Formats.UNKNOWN, "ZIP file recognized as something."

    path = mock_file_path("blank_file")
    assert ut.read_mime_type(path) == ct.Formats.UNKNOWN, "Blank file not recognized."
