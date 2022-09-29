import PySide6.QtWidgets as Qw
from logzero import logger

import deepqt.config as cfg
import deepqt.helpers as hp
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

        # Abort if the epub file was not initialized.
        if not self.epub_file.initialized:
            hp.show_warning(self, "Warning", "Please wait for the Epub to finish loading.")
            self.close()

        # Show process level of all files
        for xml_file in self.epub_file.html_files:
            logger.debug(f"{xml_file.path.name} - {xml_file.process_level}")

        self.preview_epub()

        self.pushButton_save.clicked.connect(self.save_preview)

        self.radioButton_original.toggled.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.radioButton_glossary.toggled.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.radioButton_translation.toggled.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        if epub_file.process_level == st.ProcessLevel.RAW:
            self.radioButton_original.hide()
            self.radioButton_glossary.hide()
            self.radioButton_translation.hide()

        if not epub_file.is_translated():
            self.radioButton_translation.hide()

    def preview_epub(self):
        """
        Determine how many previews to generate and show each in a tab.
        Show the html files and the toc file.
        """
        logger.debug("Loading original previews.")
        toc_file = self.epub_file.toc_file

        self.add_preview(self.tabWidget_original, toc_file.path.name, toc_file.text)
        for html_file in self.epub_file.html_files:
            self.add_preview(self.tabWidget_original, html_file.path.name, html_file.text)

        if self.epub_file.process_level == st.ProcessLevel.GLOSSARY:
            logger.debug("Loading glossary previews.")
            self.add_preview(self.tabWidget_glossary, toc_file.path.name, toc_file.text_glossary)
            for html_file in self.epub_file.html_files:
                self.add_preview(self.tabWidget_glossary, html_file.path.name, html_file.text_glossary)

        if self.epub_file.is_translated():
            logger.debug("Loading translation previews.")
            self.add_preview(self.tabWidget_translation, toc_file.path.name, toc_file.translation)
            for html_file in self.epub_file.html_files:
                self.add_preview(self.tabWidget_translation, html_file.path.name, html_file.translation)

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
        # hp.zip_folder_to_epub(self.epub_file.cache_dir, self.epub_file.cache_dir.parent / self.epub_file.path.name)
        if self.radioButton_original.isChecked():
            process_level = st.ProcessLevel.RAW
            name_suffix = "original"
        elif self.radioButton_glossary.isChecked():
            process_level = st.ProcessLevel.GLOSSARY
            name_suffix = "glossary"
        else:
            process_level = st.ProcessLevel.TRANSLATED
            name_suffix = "translated"

        save_path = self.epub_file.path.with_stem(self.epub_file.path.stem + "_" + name_suffix)
        file_path = Qw.QFileDialog.getSaveFileName(
            self,
            "Save Preview",
            str(save_path),
            "EPUB Files (*.epub)",
        )[0]
        if file_path:

            try:
                self.epub_file.write(process_level=process_level, output_path=file_path)
            except OSError as e:
                Qw.QMessageBox.warning(self, "Error", f"Could not save preview to {file_path}\n\n{e}")
