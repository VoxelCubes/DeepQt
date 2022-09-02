from enum import IntEnum
from functools import partial
from pathlib import Path
from uuid import uuid4

import PySide6.QtCore as Qc
import PySide6.QtGui as Qg
import PySide6.QtWidgets as Qw
from PySide6.QtCore import Slot
from logzero import logger

import deepqt.config as cfg
import deepqt.driver_text_preview as dtp
import deepqt.glossary as gls
import deepqt.helpers as hp
import deepqt.quote_protection as qp
import deepqt.structures as st
import deepqt.worker_thread as wt
from deepqt.CustomQ.CTableWidget import CTableWidget


class Column(IntEnum):
    ID = 0
    FILENAME = 1
    STATUS = 2
    CHARS = 3
    OUTPUT = 4


# noinspection PyUnresolvedReferences
class FileTable(CTableWidget):
    """
    Extends the functionality with custom helpers
    """

    config: cfg.Config  # Reference to the MainWindow's config.
    files: dict[str, st.TextFile | st.EpubFile]

    request_text_param_update = Qc.Signal()
    ready_for_translation = Qc.Signal()
    not_ready_for_translation = Qc.Signal()
    statusbar_message = Qc.Signal(str, int)
    recalculate_char_total = Qc.Signal()

    def __init__(self, parent=None):
        CTableWidget.__init__(self, parent)

        self.files = {}
        self.threadpool = Qc.QThreadPool.globalInstance()
        self.finished_drop.connect(lambda: self.request_text_param_update.emit())

    def set_config(self, config: cfg.Config):
        self.config = config

    def handleDrop(self, path: str):
        logger.debug(f"Dropped {path}")
        self.add_file(Path(path))

    def add_file(self, path: Path):
        logger.info(f"Added {path}")
        # Make sure the file is not already in the table.
        paths_in_table = [file.path for file in self.files.values()]
        if path in paths_in_table:
            logger.warning(f"File {path} already in table.")
            hp.show_warning(self, "Duplicate file", f"File {path} is already in the table.")
            return

        self.not_ready_for_translation.emit()
        file_id = str(uuid4())

        try:
            self.files[file_id] = self.initialize_file(path=path)
        except OSError as e:
            logger.error(f"Failed to add file {path}")
            logger.error(e)
            hp.show_warning(None, "Failed to add file", f"Failed to add file {path}\n\n{e}")
            return
        # Add the new file to the table.
        self.appendRow(
            file_id,
            path.name,
            "File added",
            hp.format_char_count(self.files[file_id].char_count),
            str(make_output_filename(self.files[file_id], self.config)),
            select_new=True,
        )
        # Align Char count to the right.
        self.item(self.rowCount() - 1, Column.CHARS).setTextAlignment(Qg.Qt.AlignRight | Qg.Qt.AlignVCenter)
        self.resizeColumnToContents(Column.OUTPUT)

    @staticmethod
    def initialize_file(path: Path) -> st.TextFile | st.EpubFile:
        """
        Read and populate the basic information of the file.
        Text files (utf8) and epub files are supported.

        :param path: The path to the file.
        """
        logger.debug(f"Initializing file {path}")
        if path.suffix.lower() == ".epub":
            return st.EpubFile(path=path)
        else:
            return st.TextFile(path=path)

    @Slot()
    def update_all_output_filenames(self):
        """
        Update all output filenames in the table.
        The file names need to match the output directory preference and target language.
        Don't update locked files.
        """
        for row in range(self.rowCount()):
            file_id = self.item(row, Column.ID).text()
            file = self.files[file_id]
            if file.locked:
                continue
            new_output_filename = make_output_filename(file, self.config)
            self.item(row, Column.OUTPUT).setText(str(new_output_filename))

        logger.debug("All output filenames updated.")
        self.resizeColumnToContents(Column.OUTPUT)

    """
    Text Processing
    """

    def update_text_params(self, row: int, glossary: st.Glossary):
        """
        Update the text file parameters for the given row.
        This means processing the glossary and quote protection, if so configured.

        :param row: The row in the table to update.
        :param glossary: The glossary to apply.
        """
        logger.debug(f"Updating text parameters for {row}")
        file_id = self.item(row, Column.ID).text()
        text_file = self.files[file_id]

        # If no processing, check if the label should be updated to say that changes were reverted.
        if not self.config.use_glossary and not self.config.use_quote_protection:
            if text_file.process_level != st.ProcessLevel.RAW:
                text_file.process_level = st.ProcessLevel.RAW
                self.item(row, Column.STATUS).setText("Reset to original")
                self.recalculate_char_count(file_id)
                return

        if self.config.use_glossary and glossary.is_valid() and glossary.hash != text_file.glossary_hash:
            glossary_to_pass = glossary
        else:
            glossary_to_pass = None

        # Test and set lock.
        if text_file.locked:
            logger.warning(f"File {text_file.path} is locked, access denied.")
            return
        text_file.locked = True

        file_id = self.item(row, Column.ID).text()
        # Crunch time begins for the worker. Bless his soul.
        # (Move this to another thread because it's CPU intensive.)
        worker = wt.Worker(
            self.text_process_work,
            file_id=file_id,
            text_file=text_file,
            glossary=glossary_to_pass,
            apply_glossary=self.config.use_glossary,
            apply_protection=self.config.use_quote_protection,
        )
        worker.signals.result.connect(self.text_process_worker_result)
        worker.signals.progress.connect(self.text_process_worker_progress)
        worker.signals.error.connect(self.text_process_worker_error)
        worker.signals.finished.connect(self.text_process_worker_finished)
        logger.debug(
            f"Worker Thread processing text file {text_file.path}: "
            f"Glossary: {glossary_to_pass is not None} | Protection: {self.config.use_quote_protection}"
        )
        # Execute.
        logger.info(f"Executing worker thread {text_file.path}")
        self.threadpool.start(worker)

    @staticmethod
    def text_process_work(
        file_id: str,
        text_file: st.TextFile,
        glossary: st.Glossary,
        apply_glossary: bool,
        apply_protection: bool,
        progress_callback: Qc.Signal,
    ):
        """
        Apply the glossary to the given text file.

        :param file_id: The ID of the file to process.
        :param text_file: The text file to apply the glossary to.
        :param glossary: The glossary to apply. None if no glossary is to be applied.
        :param apply_glossary: True if the glossary is to be applied.
        :param apply_protection: Whether to apply quote protection.
        :param progress_callback: A callback to call with the progress of the processing.
        """

        if apply_glossary:
            progress_callback.emit((file_id, "Applying glossary..."))
            if glossary is not None:  # In this case, the glossary was already applied and still cached.
                text_file.text_glossary = gls.process_text(text_file.text, glossary)
                text_file.glossary_hash = glossary.hash
            text_file.process_level = st.ProcessLevel.GLOSSARY

            if apply_protection:
                progress_callback.emit((file_id, "Applying EQP next..."))
                text_file.text_glossary_protected = qp.protect_text(text_file.text_glossary)
                text_file.process_level = st.ProcessLevel.GLOSSARY_PROTECTED
        elif apply_protection:
            progress_callback.emit((file_id, "Applying EQP..."))
            text_file.text_protected = qp.protect_text(text_file.text)
            text_file.process_level = st.ProcessLevel.PROTECTED

        progress_callback.emit((file_id, "Ready"))

        # Return the row to update the table.
        logger.info(f"Text file {text_file.path} processed.")
        return file_id

    def text_process_worker_result(self, file_id: str):
        """
        Update the table with the result of the glossary processing.
        """
        self.recalculate_char_count(file_id)

    def text_process_worker_progress(self, progress: tuple[str, str]):
        """
        Update the progress bar in the table.
        Unwrap the tuple. This is just because worker signals only transmit 1 object.

        :param progress: The progress tuple: (file_id, message)
        """
        file_id, message = progress
        self.show_file_progress(file_id, message)

    def text_process_worker_error(self, error: wt.WorkerError):
        """
        Display an error message in the table.
        """
        # Extract the row from the WorkerError's kwargs.
        row = error.kwargs["row"]
        logger.error(f"Failed to process {self.item(row, Column.FILENAME).text()}\n{error}")
        self.item(row, Column.STATUS).setText(f"Failed to process.")

    def text_process_worker_finished(self, initial_args: tuple[list, dict]):
        """
        Unlock the file after processing is finished.
        """
        args, kwargs = initial_args
        file_id = kwargs["file_id"]
        text_file = self.files[file_id]
        text_file.locked = False
        logger.debug(f"Worker thread {text_file.path} finished.")
        if self.all_files_ready():
            self.ready_for_translation.emit()

    @Slot(st.Glossary)
    def update_all_text_params(self, glossary: st.Glossary):
        """
        Update all text file parameters.
        This means processing the glossary and quote protection, if so configured.
        """
        # Abort if no text files.
        if self.rowCount() == 0:
            return

        # Try again in 1 second if the threadpool is busy.
        if self.threadpool.activeThreadCount() > 0:
            self.statusbar_message.emit("Waiting for previous threads to finish...", 1000)
            Qc.QTimer.singleShot(500, partial(self.update_all_text_params, glossary))
            return

        self.statusbar_message.emit("Processing...", -1)

        # Show a progress message for all files.
        for row in range(self.rowCount()):
            # If the file is locked, skip it.
            if not self.files[self.item(row, Column.ID).text()].locked:
                self.item(row, Column.STATUS).setText("Processing...")

        logger.debug("Updating all text params")
        for row in range(self.rowCount()):
            self.update_text_params(row, glossary)

    """
    Misc.
    """

    def show_file_progress(self, file_id: str, message: str):
        """
        Show the translation progress in the table.
        """
        self.item(self.findItems(file_id, Qc.Qt.MatchExactly)[0].row(), Column.STATUS).setText(message)

    def all_files_ready(self) -> bool:
        """
        Check if all files' process level matches the expected value and are not locked.
        If no files exist, return False.

        :return: True if all files are ready.
        """
        expected_process_level = st.ProcessLevel.RAW
        if self.config.use_glossary:
            expected_process_level |= st.ProcessLevel.GLOSSARY
        if self.config.use_quote_protection:
            expected_process_level |= st.ProcessLevel.PROTECTED

        if self.rowCount() == 0:
            return False

        for row in range(self.rowCount()):
            if self.files[self.item(row, Column.ID).text()].locked:
                return False
            if self.files[self.item(row, Column.ID).text()].process_level != expected_process_level:
                return False
        return True

    def browse_add_file(self):
        """
        Browse for a file and add it to the table.
        Supported file types: txt and epub.
        """
        path = Qw.QFileDialog.getOpenFileName(self, "Select file", "", "Text files (*.txt);;Epub files (*.epub)")[0]
        if path:
            self.add_file(Path(path))
            self.request_text_param_update.emit()

    def preview_selected_file(self):
        """
        Open the preview window for the selected file.
        """
        selected_row = self.selectedItems()[0].row()
        file_id = self.item(selected_row, Column.ID).text()
        file = self.files[file_id]
        dtp.TextPreview(self, file, self.config).exec()

    def remove_selected_file(self):
        """
        Remove the selected file from the table.
        """
        selected_row = self.selectedItems()[0].row()
        file_id = self.item(selected_row, Column.ID).text()
        self.removeRow(selected_row)
        # This isn't automatically emitted when removing a row, but is necessary to update the buttons.
        self.itemSelectionChanged.emit()
        del self.files[file_id]
        if self.all_files_ready():
            self.ready_for_translation.emit()
        else:
            self.not_ready_for_translation.emit()
        self.recalculate_char_total.emit()

    def remove_all_files(self):
        """
        Remove all files from the table.
        """
        self.clearAll()
        self.files.clear()
        self.not_ready_for_translation.emit()
        self.recalculate_char_total.emit()

    def recalculate_char_count(self, file_id: str):
        """
        Update the table after a file has been processed.

        :param file_id: The ID of the file to update.
        """
        text_file = self.files[file_id]
        self.item(self.findItems(file_id, Qc.Qt.MatchExactly)[0].row(), Column.CHARS).setText(
            hp.format_char_count(text_file.char_count)
        )
        self.recalculate_char_total.emit()


def make_output_filename(input_file: st.InputFile, config: cfg.Config) -> Path:
    # Append the language code to the file stem.
    path = input_file.path
    # Add lang extension.
    path = path.with_stem(f"{path.stem}_{config.lang_to.lower()}")
    # Add dump extension if translation failed.
    if input_file.translation_incomplete():
        path = path.with_suffix(".DUMP")

    if config.use_fixed_output_path:
        path = Path(config.fixed_output_path) / path.name

    path = hp.ensure_unique_file_path(path)

    return path
