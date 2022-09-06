import PySide6.QtWidgets as Qw
from functools import partial

import deepqt.config as cfg
import deepqt.structures as st
from deepqt.ui_generated_files.ui_epub_preview import Ui_EpubPreview


class EpubPreview(Qw.QDialog, Ui_EpubPreview):
    """
    Preview text files with and without glossaries/quote protection applied.
    Also offer to save the previews to a file.
    """

    config: cfg.Config
    epub_file: st.EpubFile

    def __init__(self, parent, epub_file: st.EpubFile, config: cfg.Config):
        Qw.QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.setWindowTitle(f"{epub_file.path.name} - Preview")

        self.config = config
        self.epub_file = epub_file

        self.preview_epub()

        self.pushButton_save.clicked.connect(self.save_preview)

        self.radioButton_original.toggled.connect(partial(self.stackedWidget.setCurrentIndex, 0))
        self.radioButton_glossary.toggled.connect(partial(self.stackedWidget.setCurrentIndex, 1))
        self.radioButton_translation.toggled.connect(partial(self.stackedWidget.setCurrentIndex, 2))

        if epub_file.process_level == st.ProcessLevel.RAW:
            self.radioButton_original.hide()
            self.radioButton_glossary.hide()
            self.radioButton_translation.hide()

        if not epub_file.finished:
            self.radioButton_translation.hide()

    def preview_epub(self):
        """
        Determine how many previews to generate and show each in a tab.
        """
        for xml_file in self.epub_file.xml_files:
            self.add_preview(self.tabWidget_original, xml_file.path.name, xml_file.text)

        if self.epub_file.process_level == st.ProcessLevel.GLOSSARY:
            for xml_file in self.epub_file.xml_files:
                self.add_preview(self.tabWidget_glossary, xml_file.path.name, xml_file.text_glossary)

        if self.epub_file.is_translated:
            for xml_file in self.epub_file.xml_files:
                self.add_preview(self.tabWidget_translation, xml_file.path.name, xml_file.translation)

    @staticmethod
    def add_preview(stack_page: Qw.QTabWidget, title: str, text: str):
        """
        Add a preview tab to the dialog.
        Show the text in a QPlainTextEdit set to read only mode.
        Also show line numbers.
        """
        preview_tab = Qw.QWidget()
        preview_tab.setObjectName(title)
        preview_layout = Qw.QVBoxLayout(preview_tab)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setSpacing(0)
        preview_layout.setObjectName("preview_layout")
        preview_text = Qw.QPlainTextEdit(preview_tab)
        preview_text.setReadOnly(True)
        preview_text.setObjectName("preview_text")
        preview_text.setPlainText(text)
        preview_layout.addWidget(preview_text)
        stack_page.addTab(preview_tab, title)

    def save_preview(self):
        """
        Save the current state of the epub.
        """
        raise NotImplementedError
