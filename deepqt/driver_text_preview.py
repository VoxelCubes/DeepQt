import PySide6.QtWidgets as Qw

import deepqt.config as cfg
import deepqt.structures as st
from deepqt.ui_generated_files.ui_text_preview import Ui_TextPreview


class TextPreview(Qw.QDialog, Ui_TextPreview):
    """
    Preview text files with and without glossaries/quote protection applied.
    Also offer to save the previews to a file.
    """

    config: cfg.Config
    text_file: st.TextFile

    def __init__(self, parent, text_file: st.TextFile, config: cfg.Config):
        Qw.QDialog.__init__(self, parent=parent)
        self.setupUi(self)
        self.setWindowTitle(f"{text_file.path.name} - Preview")

        self.config = config
        self.text_file = text_file

        self.preview_text()

        self.pushButton_save.clicked.connect(self.save_preview)

    def preview_text(self):
        """
        Determine how many previews to generate and show each in a tab.
        """
        self.add_preview("Original", self.text_file.text)

        if self.text_file.process_level & st.ProcessLevel.GLOSSARY:
            self.add_preview("Glossary", self.text_file.text_glossary)

        if self.text_file.process_level == st.ProcessLevel.PROTECTED:
            self.add_preview("Protected", self.text_file.text_protected)
        elif self.text_file.process_level == st.ProcessLevel.GLOSSARY_PROTECTED:
            self.add_preview("Glossary Protected", self.text_file.text_glossary_protected)

        if self.text_file.translation:
            self.add_preview("Translation", self.text_file.translation)

    def add_preview(self, title: str, text: str):
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
        self.tabWidget.addTab(preview_tab, title)

    def save_preview(self):
        """
        Save the preview in the currently visible QPlainTextEdit to a file.
        """
        preview_text = self.tabWidget.currentWidget().findChild(Qw.QPlainTextEdit, "preview_text")
        save_path = self.text_file.path.with_stem(
            self.text_file.path.stem + "_" + self.tabWidget.tabText(self.tabWidget.currentIndex()).replace(" ", "_")
        )
        file_path = Qw.QFileDialog.getSaveFileName(
            self,
            "Save Preview",
            str(save_path),
            "Text Files (*.txt)",
        )[0]
        if file_path:
            try:
                with open(file_path, "w", encoding="utf8") as f:
                    f.write(preview_text.toPlainText())
            except OSError as e:
                Qw.QMessageBox.warning(self, "Error", f"Could not save preview to {file_path}\n\n{e}")
