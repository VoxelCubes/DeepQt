import sys
import shutil
from functools import partial
from math import ceil
from pathlib import Path
import platform
from enum import Enum

import psutil
import PySide6.QtCore as Qc
import PySide6.QtGui as Qg
import PySide6.QtWidgets as Qw
import deepl
from PySide6.QtCore import Signal, Slot
from loguru import logger

import deepqt.translation_interface as ai
import deepqt.backends.backend_interface as bi
import deepqt.backends.lookups as b_lut
import deepqt.config as cfg
import deepqt.glossary as gl
import deepqt.memory_watcher as mw
import deepqt.structures as st
import deepqt.worker_thread as wt
import deepqt.constants as ct
import deepqt.utils as ut
import deepqt.gui_utils as gu
import deepqt.issue_reporter_driver as ird
import deepqt.driver_backend_configuration as dbc
from deepqt import __program__, __version__

from deepqt.file_table import Column, make_output_filename
from deepqt.ui_generated_files.ui_mainwindow import Ui_MainWindow


# noinspection PyUnresolvedReferences
class MainWindow(Qw.QMainWindow, Ui_MainWindow):
    config: cfg.Config = None
    glossary: st.Glossary = None
    translating: bool
    debug: bool

    translation_mode: ct.TranslationMode

    backend_objects: dict[ct.Backend, bi.Backend]

    threadpool: Qc.QThreadPool

    hamburger_menu: Qw.QMenu
    theming_menu: Qw.QMenu

    text_params_changed = Signal(st.Glossary)
    text_output_changed = Signal()
    abort_translation_worker = Signal()

    label_stats: Qw.QLabel

    default_palette: Qg.QPalette
    default_style: str
    # default_icon_theme: str
    theme_is_dark: ut.Shared[bool]
    theme_is_dark_changed = Signal(bool)  # When true, the new theme is dark.

    memory_watcher: mw.MemoryWatcher  # The memory watcher for the window.
    mem_watcher_thread: Qc.QThread  # The thread for the memory watcher.

    def __init__(
        self,
        command: ct.Command,
        inputs: list[str] | str | None,
        api: ct.Backend | None,
        translate_now: bool,
        debug: bool,
    ) -> None:
        Qw.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(f"{__program__} {__version__}")
        self.setWindowIcon(Qg.QIcon(":/icons/logo.png"))
        self.debug = debug

        self.test_and_set_lock_file()

        self.theme_is_dark = ut.Shared[bool](True)

        self.translating = False  # If true, the translation is in progress.
        self.glossary = st.Glossary()  # Create a dummy glossary
        self.hamburger_menu = Qw.QMenu()

        self.initialize_ui()

        self.start_memory_watcher()

        self.threadpool = Qc.QThreadPool.globalInstance()

        self.config = self.load_config()
        self.config.save()
        self.config.pretty_log()
        # Share config with the file table.
        self.file_table.set_config(self.config)

        self.save_default_palette()
        self.load_config_theme()

        self.backend_objects = {
            ct.Backend(backend): b_lut.backend_to_class[backend]() for backend in ct.Backend
        }
        self.load_backend(api)

        Qc.QTimer.singleShot(0, self.post_init)

    @property
    def translation_mode(self) -> ct.TranslationMode:
        # The translation mode is dictated by the button states in the gui.
        return (
            ct.TranslationMode.File
            if self.pushButton_translate_files.isChecked()
            else ct.TranslationMode.Text
        )

    def initialize_ui(self) -> None:
        if platform.system() == "Windows":
            self.setWindowIcon(gu.load_custom_icon("logo.ico"))
        else:
            self.setWindowIcon(gu.load_custom_icon("logo.svg"))
        # Set window height to 650px.
        # self.resize(self.width(), 650)
        self.hide_progress()
        self.init_oom_banner()
        self.start_button_enabled(False)
        self.show_button_start()
        self.set_up_statusbar()
        self.set_up_hamburger_menu()

        # Make the start and abort buttons 50% taller.
        self.pushButton_start.setMinimumHeight(self.pushButton_start.height() * 1.5)
        self.pushButton_abort.setMinimumHeight(self.pushButton_abort.height() * 1.5)

        # Allow the table to accept file drops and hide the ID column.
        self.file_table.setAcceptDrops(True)
        self.file_table.setColumnHidden(Column.ID, True)
        self.file_table.setColumnWidth(Column.FILENAME, 200)
        self.file_table.setColumnWidth(Column.STATUS, 200)

        # Set up interactive panels.
        self.set_interactive_input_from_glossary_visible(False)
        self.set_interactive_translation_to_glossary_visible(False)

        # Connect signals.
        self.connect_combobox_slots()

        self.checkBox_use_glossary.toggled.connect(self.use_glossary_toggled)
        self.pushButton_out_dir_browse.clicked.connect(self.browse_out_dir)
        self.lineEdit_out_dir.textEdited.connect(partial(self.fixed_out_updated, False))
        self.lineEdit_out_dir.editingFinished.connect(partial(self.fixed_out_updated, True))

        self.pushButton_glossary_file_browse.clicked.connect(self.browse_glossary_file)
        self.lineEdit_glossary_file.textEdited.connect(
            partial(self.glossary_file_updated, self, False)
        )
        self.lineEdit_glossary_file.editingFinished.connect(
            partial(self.glossary_file_updated, self, True)
        )

        self.pushButton_configure_backend.clicked.connect(self.configure_backend)

        # self.pushButton_api_config.clicked.connect(self.configure_api)
        # self.pushButton_refresh.clicked.connect(self.load_config_to_ui)
        self.pushButton_show_to_interactive_glossary.toggled.connect(
            self.set_interactive_translation_to_glossary_visible
        )
        self.pushButton_show_from_interactive_glossary.toggled.connect(
            self.set_interactive_input_from_glossary_visible
        )

        self.text_output_changed.connect(self.file_table.update_all_output_filenames)
        self.text_params_changed.connect(self.file_table.update_all_text_params)

        # TODO make these part of the right click menu for the file table.
        # self.pushButton_file_add.clicked.connect(self.file_table.browse_add_file)
        # self.pushButton_file_preview.clicked.connect(self.file_table.preview_selected_file)
        # self.pushButton_file_remove.clicked.connect(self.file_table.remove_selected_file)
        # self.pushButton_file_remove_all.clicked.connect(self.file_table.remove_all_files)

        self.pushButton_start.clicked.connect(self.start_translating)
        self.pushButton_abort.clicked.connect(self.abort_translating)

        self.file_table.request_text_param_update.connect(self.update_file_table_params)
        self.file_table.ready_for_translation.connect(self.ready_to_translate)
        self.file_table.not_ready_for_translation.connect(self.not_ready_to_translate)
        self.file_table.statusbar_message.connect(self.statusbar.showMessage)
        self.file_table.recalculate_char_total.connect(self.recalculate_char_total)

    def post_init(self) -> None:
        """
        Post-initialization tasks, mostly stuff that needs to happen after the window is shown.
        """
        nuke_epub_cache()
        self.load_glossary()

        def exception_handler(exctype, value, traceback) -> None:
            gu.show_exception(
                self,
                "Uncaught Exception",
                "An uncaught exception was raised.",
                error_bundle=(exctype, value, traceback),
            )

        sys.excepthook = exception_handler

    def closeEvent(self, event: Qg.QCloseEvent) -> None:
        """
        Notify config on close.
        """
        logger.info("Closing window.")
        self.free_lock_file()
        self.memory_watcher.stop()
        self.abort_translation_worker.emit()
        if self.threadpool.activeThreadCount():
            self.statusbar.showMessage("Waiting for threads to finish...")
            # Process Qt events so that the message shows up.
            Qc.QCoreApplication.processEvents()
            self.threadpool.waitForDone()

        nuke_epub_cache()
        event.accept()

    def load_config(self) -> cfg.Config:
        """
        Load the config if there is one, handling errors as needed.

        :return: The loaded or default config.
        """
        # Check if there is a config at all.
        config_path = ut.get_config_path()
        if not config_path.exists():
            logger.info(f"No config found at {config_path}.")
            return cfg.Config()

        config, success, errors = cfg.load_config(config_path)

        # Format them like: ValueError: 'lang_from' must be a string.
        errors_str = "\n".join(map(str, errors))

        if not success:
            gu.show_warning(
                self,
                "Config Error",
                f"Failed to load the config file.\n\n{errors_str}\n\nProceeding with the default configuration.",
            )
        elif errors:
            gu.show_info(
                self,
                "Config Warnings",
                f"Minor issues were found and corrected in the config file.\n\n{errors_str}",
            )

        return config

    def connect_combobox_slots(self) -> None:
        """
        Connect the combobox slots.
        """
        self.comboBox_lang_from.currentIndexChanged.connect(self.lang_from_updated)
        self.comboBox_lang_to.currentIndexChanged.connect(self.lang_to_updated)

    def disconnect_combobox_slots(self) -> None:
        """
        Disconnect the combobox slots. This prevents erroneous signals from being sent during
        setup of new language options.
        """
        self.comboBox_lang_from.currentIndexChanged.disconnect()
        self.comboBox_lang_to.currentIndexChanged.disconnect()

    """
    Config interactions
    """

    def load_config_to_ui(self) -> None:
        """
        Apply data from config to ui widgets.
        """
        logger.debug("Loading config to UI.")

        self.lineEdit_out_dir.setText(self.config.fixed_output_path)

        self.lineEdit_glossary_file.setText(self.config.glossary_path)
        self.checkBox_use_glossary.setChecked(self.config.use_glossary)

        self.glossary_enabled(self.config.use_glossary)
        self.set_interactive_glossary_visible(self.config.use_glossary)

        backend = self.config.current_backend
        backend_config = self.config.backend_configs[backend]

        self.label_backend_name.setText(backend_config.name)
        icon_path = backend_config.icon
        self.label_backend_logo.setPixmap(backend_config.load_icon().pixmap(Qc.QSize(24, 24)))

        return
        # Ignore the mock because it cannot give language options. It is only to be used for translation.
        translator = self.open_translator(use_mock=False)

        self.show_api_status(translator is not None)
        self.update_current_usage(translator)

        if translator is not None:
            # Disconnect the slots to prevent signals from being sent during setup of new language options.
            self.disconnect_combobox_slots()  # vvv
            # Load language options from API.
            self.comboBox_lang_from.clear()
            self.comboBox_lang_to.clear()

            # Add automatic option.
            self.comboBox_lang_from.addTextItemLinkedData("Detect", "")

            for lang in translator.get_source_languages():
                self.comboBox_lang_from.addTextItemLinkedData(lang.name, lang.code)

            for lang in translator.get_target_languages():
                self.comboBox_lang_to.addTextItemLinkedData(lang.name, lang.code)

            self.connect_combobox_slots()  # ^^^

            # Try to select the configured languages.
            try:
                self.comboBox_lang_from.setCurrentIndexByLinkedData(self.config.lang_from)
            except ValueError:
                logger.debug(f"Configured lang_from '{self.config.lang_from}' not found")

            try:
                self.comboBox_lang_to.setCurrentIndexByLinkedData(self.config.lang_to)
            except ValueError:
                logger.debug(f"Configured lang_to '{self.config.lang_to}' not found")
        else:
            self.statusbar.showMessage("Error connecting to the API.")

    def lang_from_updated(self) -> None:
        """
        Copy lang_from from the combobox into the config and save it.
        """
        self.config.lang_from = self.comboBox_lang_from.currentLinkedData()
        logger.debug(f"Saving lang_from: {self.config.lang_from}")
        self.config.save()

    def lang_to_updated(self) -> None:
        """
        Copy lang_to from the combobox into the config and save it.
        """
        self.config.lang_to = self.comboBox_lang_to.currentLinkedData()
        logger.debug(f"Saving lang_to: {self.config.lang_to}")
        self.text_output_changed.emit()
        self.config.save()

    def browse_out_dir(self) -> None:
        """
        Browse for a directory to save files to.
        """
        dir_path = Qw.QFileDialog.getExistingDirectory(
            self, "Select output directory", self.config.fixed_output_path
        )
        if dir_path:
            self.lineEdit_file_out_dir.setText(dir_path)
            self.config.fixed_output_path = dir_path
            self.text_output_changed.emit()
            self.config.save()

    def fixed_out_updated(self, save: bool, *_) -> None:
        """
        Copy fixed_file_out from the lineedit into the config and save it.
        Don't save until the line edit signals the end of editing.
        Throw away the text in the line edit that the signal passes along by using *_.
        This is because the signal for editing finished does not pass along the text,
        making it unreliable.

        :param save: Whether to save the config.
        """
        self.config.fixed_output_path = self.lineEdit_file_out_dir.text()
        if save:
            self.config.save()
        self.text_output_changed.emit()

    def use_glossary_toggled(self) -> None:
        """
        Enable or disable the glossary checkbox and save it to the config.
        """
        self.config.use_glossary = self.checkBox_use_glossary.isChecked()
        self.glossary_enabled(self.config.use_glossary)
        self.set_interactive_glossary_visible(self.config.use_glossary)
        self.config.save()
        if self.config.use_glossary:
            self.load_glossary()
        self.text_params_changed.emit(self.glossary)

    def browse_glossary_file(self) -> None:
        """
        Browse for a glossary file.
        Accepts whatever pyexcel can handle.
        """
        file_path = Qw.QFileDialog.getOpenFileName(
            self, "Select glossary file", self.config.glossary_path
        )
        if file_path:
            self.lineEdit_glossary_file.setText(file_path[0])
            self.config.glossary_path = file_path[0]
            self.config.save()
            self.load_glossary()

    def glossary_file_updated(self, save: bool, *_) -> None:
        """
        Copy glossary_file from the lineedit into the config and save it.
        Don't save until the line edit signals the end of editing.
        Throw away the text in the line edit that the signal passes along by using *_.
        This is because the signal for editing finished does not pass along the text,
        making it unreliable.

        :param save: Whether to save the config.
        """
        self.config.glossary_path = self.lineEdit_glossary_file.text()
        if save:
            self.config.save()
            self.load_glossary()

    # def extra_quote_protection_toggled(self) -> None:
    #     """
    #     Enable or disable the extra quote protection checkbox and save it to the config.
    #     """
    #     self.config.use_quote_protection = self.checkBox_extra_quote_protection.isChecked()
    #     self.config.save()
    #     self.text_params_changed.emit(self.glossary)

    # ======================================== Backends ========================================

    def load_backend(self, backend: ct.Backend | None = None) -> None:
        """
        Load the backend specified as an argument, or fall back to the config's last used one.

        :param backend: [Optional] The backend to load.
        """
        if backend is not None:
            logger.info(f"Loading backend: {backend.name}")
            self.config.current_backend = backend
        else:
            logger.info(f"Reloading current backend: {self.config.current_backend.name}")

        self.load_config_to_ui()

        # Prompt the backend to connect.
        backend = self.config.current_backend
        backend_obj = self.backend_objects[backend]
        backend_config = self.config.backend_configs[backend]

        backend_obj.set_config(backend_config)

        if backend_obj.status().connection == bi.ConnectionStatus.Offline:
            backend_obj.connect()

    # ======================================== Dialogs ========================================

    def configure_backend(self) -> None:
        """
        Open the backend chooser/configuration dialog.
        """
        backend_conf_dialog = dbc.BackendConfiguration(
            self, self.config, self.debug, self.theme_is_dark, self.theme_is_dark_changed
        )
        response = backend_conf_dialog.exec()
        if response == Qw.QDialog.Accepted:
            # Adopt changes from the dialog.
            logger.debug("Adopting backend changes.")
            self.config = backend_conf_dialog.get_modified_config()
            self.config.save()
            self.load_backend()

    # ======================================= Misc. Helpers =======================================

    def open_translator(self, use_mock: bool = True) -> deepl.Translator | None:
        """
        Open a translator instance.

        :return: translator instance and whether it was successful
        """

        if self.config.api_key == "":
            # Fail silently if no API key is set, since this is the default value.
            logger.warning("No API key set")
            return None
        try:
            if self.config.tl_mock and use_mock:
                logger.info("Opening mock translator.")
                return deepl.Translator(
                    auth_key="1234567890",
                    server_url="http://localhost:3000",
                )
            else:
                logger.info("Opening translator.")
                translator = deepl.Translator(auth_key=self.config.api_key)
                # Test the api, since initialization doesn't mean success.
                translator.get_source_languages()
                return translator
        except Exception as e:
            show_warning(self, "API Error", f"Failed to connect to DeepL API\n\n{e}")
            return None

    def update_file_table_params(self) -> None:
        """
        Update the file table with the current parameters.
        """
        self.text_params_changed.emit(self.glossary)

    """
    Glossary
    """

    def load_glossary(self) -> None:
        """
        Open a glossary file and parse it.
        Afterwards, notify any files to apply it.
        """
        path = Path(self.config.glossary_path)

        if not path.is_file():
            logger.warning(f"Glossary file not found: {path}")
            self.statusbar.showMessage(f"Glossary file not found.", 10_000)
            return

        # Check if we haven't loaded the file before.
        if self.glossary.is_same_glossary(path):
            logger.info("Glossary file unchanged")
            return
        # Start the worker.
        self.glossary_worker_start(path)

    def glossary_worker_start(self, path: Path) -> None:
        """
        Initialize generic QRunner worker to load a glossary file.

        :param path: Path to the glossary file.
        """
        self.statusbar.showMessage("Loading glossary...")
        worker = wt.Worker(gl.parse_glossary, path=path, no_progress_callback=True)
        worker.signals.result.connect(self.glossary_worker_result)
        worker.signals.error.connect(self.glossary_worker_error)
        logger.debug(f"Loading glossary from {path}")
        # Execute.
        self.threadpool.start(worker)

    def glossary_worker_result(self, glossary: st.Glossary) -> None:
        """
        Notify any files to apply the glossary.

        :param glossary: The glossary received from the worker.
        """
        self.glossary = glossary
        terms_found = len(glossary)
        self.statusbar.showMessage(
            f"Loaded {terms_found} {ut.f_plural(terms_found, 'term')} from glossary."
        )
        logger.info(f"Glossary loaded, {terms_found} {ut.f_plural(terms_found, 'term')} found.")
        # logger.debug(f"Glossary dump: \n{glossary}")
        self.text_params_changed.emit(self.glossary)

    def glossary_worker_error(self, error: wt.WorkerError) -> None:
        """
        Notify the user of an error.
        """
        self.statusbar.showMessage(f"Error loading glossary.", 10_000)
        gu.show_warning(self, "Glossary Error", f"Failed to open glossary file\n\n{error.value}")
        logger.error(f"Failed to open glossary file.\n{error}")

    """
    Translation
    """

    def start_translating(self) -> None:
        logger.info("Starting translation.")
        # Check if the API is ready.
        translator = self.open_translator()
        if translator is None:
            gu.show_warning(
                self, "API Error", "Failed to open DeepL translator. Please check account settings."
            )
        if self.config.tl_mock:
            gu.show_warning(
                self,
                "Mock Mode",
                "Translations are being performed with the mock translator.\nDo not expect accurate results.",
            )
        else:
            # Skip the char count warning when mocking because then we can't load usage stats and it doesn't matter.
            if not self.char_count_warning(translator):
                return

        # Restrict user interaction.
        self.translating = True
        self.update_input_buttons()
        self.set_translation_parameters_enabled(False)
        self.abort_button_enabled(True)
        self.show_button_abort()
        self.progressBar.setValue(0)
        self.show_progress()
        self.label_progress.setText("Preparing...")
        self.statusbar.showMessage("Translating...")

        # Send the data off to the worker.
        worker = ai.DeeplWorker(
            translator=translator, input_files=self.file_table.files, config=self.config
        )
        worker.signals.result.connect(self.translation_worker_result)
        worker.signals.progress.connect(self.translation_worker_progress)
        worker.signals.error.connect(self.translation_worker_error)
        self.abort_translation_worker.connect(worker.abort)
        self.threadpool.start(worker)

    def char_count_warning(self, translator: deepl.Translator) -> bool:
        # Make sure the user is aware of how many characters will be translated.
        # Check if the allotted character count won't exceed the quota.
        total_chars = sum(file.char_count for file in self.file_table.files.values())
        api_usage = translator.get_usage()
        if api_usage.character.limit != DEEPL_USAGE_UNLIMITED:
            allowed_chars = api_usage.character.limit - api_usage.character.count
            remaining_chars = allowed_chars - total_chars
            warning_msg = (
                f"You are about to translate {ut.format_char_count(total_chars)} "
                f"{ut.f_plural(total_chars, 'character')},\n"
                f"leaving you with {ut.format_char_count(remaining_chars)} "
                f"{ut.f_plural(remaining_chars, 'character')}."
                f"\nProceed?"
            )
            if api_usage.character.limit_reached:
                warning_msg = "You have reached your character limit.\nProceed anyway?"
            elif total_chars > allowed_chars:
                warning_msg = (
                    f"You are about to translate {ut.format_char_count(total_chars)} "
                    f"{ut.f_plural(total_chars, 'character')}, "
                    f"which exceeds your remaining character limit of {ut.format_char_count(allowed_chars)}.\nProceed anyway?"
                )
        else:
            warning_msg = (
                f"You are about to translate {ut.format_char_count(total_chars)} "
                f"{ut.f_plural(total_chars, 'character')}."
                f"\nProceed?"
            )
        # Ask the user if he wants to proceed, just in case.
        logger.info(f"Character limit warning: {warning_msg}")
        affirmation = gu.show_question(self, "API Limit", warning_msg)
        if not affirmation:
            logger.info("Translation cancelled.")
            return False
        return True

    def translation_worker_result(self, exit_code: ai.State) -> None:
        """
        If we made it here, the translation was either successful or aborted.
        Notify the user, write the output, and reset the ui.

        :param exit_code: The exit code of the translation.
        """

        logger.info(f"Translation finished with exit code {exit_code}")
        self.text_output_changed.emit()

        if exit_code == ai.State.DONE:
            self.statusbar.showMessage("Translation finished.")
            gu.show_info(self, "Finished", "Translations successfully completed.")
            for file_id in self.file_table.files:
                self.write_output_file(file_id)

        elif exit_code == ai.State.ABORTED:
            self.statusbar.showMessage("Translation aborted.")
            gu.show_info(self, "Aborted", "Translation aborted.")
            if self.config.dump_on_abort:
                for file_id in self.file_table.files:
                    self.write_output_file(file_id)

        elif exit_code == ai.State.QUOTA_EXCEEDED:
            self.statusbar.showMessage("API quota exceeded.")
            gu.show_warning(
                self,
                "API Quota Exceeded",
                "The DeepL API quota has been exceeded.\nDumping output files.",
            )
            for file_id in self.file_table.files:
                self.write_output_file(file_id)

        self.translation_worker_finished()

    def translation_worker_progress(
        self, key: str, message: str, processed_chars: int | None, total_chars: int | None
    ) -> None:
        """
        Update the file with the key in the file table to display this message.

        :param key: InputFile ID.
        :param message: Progress status.
        :param processed_chars: Number of characters processed.
        :param total_chars: Total number of characters to process.
        """
        logger.debug(f"Translation progress: {key} {message} {processed_chars} {total_chars}")
        self.file_table.show_file_progress(key, message)
        if processed_chars is not None and total_chars is not None:
            self.update_translation_status(processed_chars, total_chars)

    def translation_worker_error(self, error: wt.WorkerError) -> None:
        logger.error(f"Translation failed.\n{error}")
        self.statusbar.showMessage(f"Translation failed.")
        gu.show_warning(self, "Translation Error", f"Translation failed.\n\n{error.value}")
        self.translation_worker_finished()

    def translation_worker_finished(self) -> None:
        """
        Update the UI to reflect the finished state.
        """
        self.translating = False
        self.update_input_buttons()
        self.set_translation_parameters_enabled(True)
        self.abort_button_enabled(False)
        self.show_button_start()
        self.hide_progress()
        self.config.save()  # Save the last average time/1000 characters.
        self.load_config_to_ui()

    def abort_translating(self) -> None:
        logger.info("Aborting translation.")
        self.abort_translation_worker.emit()
        self.statusbar.showMessage("Aborting translation...")

    def write_output_file(self, file_id: str) -> None:
        """
        Write the output file to disk.
        Check the type of the file (text or epub) and run the appropriate function.

        :param file_id: InputFile ID.
        """

        file = self.file_table.files[file_id]
        try:
            if isinstance(file, st.TextFile):
                self.write_output_text_file(file_id)
            elif isinstance(file, st.EpubFile):
                self.write_output_epub_file(file_id)
            else:
                raise TypeError(f"Unknown file type: {file}")

        except OSError as e:
            path_out = make_output_filename(file, self.config)
            logger.error(f"Failed to write translation to {path_out}.\n{e}\n\n")
            gu.show_warning(
                self,
                "Output Error",
                f"Failed to write translation to {path_out}.\n\n{e}\n\n"
                f"Please make sure you have write permissions to the output directory.\n"
                f"To save the translation in another location without needing to re-translate, "
                f'select your file, then click the "preview" button.\n'
                f'There, select the translated version and press the "Save Preview to File" button.',
            )
            self.file_table.show_file_progress(file_id, "Could not write output!")

    def write_output_text_file(self, file_id: str) -> None:
        """
        Write the translation of a file to the assigned output path.

        Check the status of the file. We decide 3 cases:
        1. File is not translated.
           - Skip this file.
        2. File is translated.
           - Write the translation to the output path.
        3. File is partially translated.
           - Dump the translation to the output path, if so configured.

        :param file_id: InputFile ID.
        """
        file = self.file_table.files[file_id]
        text_out = file.get_translated_text()
        path_out = make_output_filename(file, self.config)

        if text_out is None:  # Case 1.
            logger.info(f"Skipping file {file_id} because it has not been translated.")
            self.file_table.show_file_progress(file_id, "Not translated.")
            return
        else:
            # Ensure the output directory exists.
            path_out.parent.mkdir(parents=True, exist_ok=True)

            with open(path_out, "w", encoding="utf-8") as f:
                f.write(text_out)
                logger.info(f"Wrote translation to {path_out}")
                if file.translation_incomplete():
                    self.file_table.show_file_progress(file_id, "Incomplete output written.")
                else:
                    self.file_table.show_file_progress(file_id, "Translation written.")

    def write_output_epub_file(self, file_id: str) -> None:
        """
        Write the translation of a file to the assigned output path.

        Check the status of the file. We decide 3 cases:
        1. File is not translated.
           - Skip this file.
        2. File is translated.
           - Write the translation to the output path.
        3. File is partially translated.
           - Dump the translation to the output path, if so configured.

        :param file_id: InputFile ID.
        """
        file: st.EpubFile = self.file_table.files[file_id]
        path_out = make_output_filename(file, self.config)

        if not file.translation_incomplete() and not file.is_translated():
            # Skip this because we have nothing to dump.
            logger.info(f"Skipping file {file_id} because nothing has been translated.")
            self.file_table.show_file_progress(file_id, "Not translated.")
            return

        file.write(st.ProcessLevel.TRANSLATED, path_out)

    """
    Log file
    """

    def set_up_statusbar(self) -> None:
        """
        Add a label to show the current char total and time estimate.
        Add a flat button to the statusbar to offer opening the config file.
        Add a flat button to the statusbar to offer opening the log file.
        """
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setContentsMargins(0, 0, 6, 0)

        self.label_stats = Qw.QLabel("")
        self.statusbar.addPermanentWidget(self.label_stats)

        button_log = Qw.QPushButton("Open Log")
        button_log.clicked.connect(self.open_log_viewer)
        button_log.setIcon(Qg.QIcon.fromTheme("text-x-changelog"))
        button_log.setFlat(True)
        self.statusbar.addPermanentWidget(button_log)

    def set_up_hamburger_menu(self) -> None:
        """
        This is the hamburger menu on the main window.
        It contains several menu-bar-esque actions.
        """
        self.pushButton_menu.setMenu(self.hamburger_menu)
        # Add theming menu.
        self.theming_menu = self.hamburger_menu.addMenu(
            Qg.QIcon.fromTheme("games-config-theme"), "Theme"
        )
        themes = [("", "System")]
        themes.extend(ut.get_available_themes())
        for theme, name in themes:
            action = Qg.QAction(name, self)
            action.setCheckable(True)
            action.theme = theme
            action.triggered.connect(partial(self.set_theme, theme))
            self.theming_menu.addAction(action)

        if self.debug:
            # Add an intentional crash button.
            self.hamburger_menu.addSeparator()
            action = Qg.QAction(Qg.QIcon.fromTheme("tools-report-bug"), "Simulate crash", self)
            action.triggered.connect(self.simulate_crash)
            logger.warning("Debug mode active.")
            self.hamburger_menu.addAction(action)

    def open_log_viewer(self) -> None:
        logger.debug("Opening issue reporter.")
        issue_reporter = ird.IssueReporter(self)
        issue_reporter.exec()

    # ============================= Simple UI manipulation functions =============================

    def hide_progress(self) -> None:
        self.frame_progress_drawer.hide()

    def show_progress(self) -> None:
        self.frame_progress_drawer.show()

    @Slot(bool)
    def set_interactive_input_from_glossary_visible(self, visible: bool) -> None:
        self.plainTextEdit_from_interactive_glossary.setVisible(visible)
        if visible:
            self.pushButton_show_from_interactive_glossary.setIcon(Qg.QIcon.fromTheme("arrow-down"))
            self.pushButton_show_from_interactive_glossary.setText("Hide input after glossary")
        else:
            self.pushButton_show_from_interactive_glossary.setIcon(Qg.QIcon.fromTheme("arrow-up"))
            self.pushButton_show_from_interactive_glossary.setText("Show input after glossary")

    @Slot(bool)
    def set_interactive_translation_to_glossary_visible(self, visible: bool) -> None:
        self.plainTextEdit_to_interactive_glossary.setVisible(visible)
        if visible:
            self.pushButton_show_to_interactive_glossary.setIcon(Qg.QIcon.fromTheme("arrow-down"))
            self.pushButton_show_to_interactive_glossary.setText(
                "Show translation before applying glossary"
            )
        else:
            self.pushButton_show_to_interactive_glossary.setIcon(Qg.QIcon.fromTheme("arrow-up"))
            self.pushButton_show_to_interactive_glossary.setText(
                "Hide translation before applying glossary"
            )

    def set_interactive_glossary_visible(self, visible: bool) -> None:
        # This will entirely hide both glossary panels and the buttons.
        # This is for when the glossary isn't enabled to begin with.
        show_from_textfield = self.pushButton_show_from_interactive_glossary.isChecked() and visible
        show_to_textfield = self.pushButton_show_to_interactive_glossary.isChecked() and visible

        self.set_interactive_input_from_glossary_visible(show_from_textfield)
        self.set_interactive_translation_to_glossary_visible(show_to_textfield)

        self.pushButton_show_from_interactive_glossary.setVisible(visible)
        self.pushButton_show_to_interactive_glossary.setVisible(visible)

    def glossary_enabled(self, enabled: bool) -> None:
        self.lineEdit_glossary_file.setEnabled(enabled)
        self.pushButton_glossary_file_browse.setEnabled(enabled)

    def start_button_enabled(self, enabled: bool) -> None:
        self.pushButton_start.setEnabled(enabled)

    def abort_button_enabled(self, enabled: bool) -> None:
        self.pushButton_abort.setEnabled(enabled)

    def show_button_start(self) -> None:
        self.pushButton_start.show()
        self.pushButton_abort.hide()

    def show_button_abort(self) -> None:
        self.pushButton_start.hide()
        self.pushButton_abort.show()

    def show_api_status(self, good: bool) -> None:
        self.label_api_status_good.setVisible(good)
        self.label_api_status_good_icon.setVisible(good)
        self.label_api_status_bad.setVisible(not good)
        self.label_api_status_bad_icon.setVisible(not good)

    def update_current_usage(self, translator: deepl.Translator | None) -> None:
        return
        if translator is None:
            self.label_api_usage.setText("—")
            self.label_api_usage_warn_icon.hide()
            self.label_api_usage_error_icon.hide()
            return

        usage = translator.get_usage()
        count = usage.character.count
        limit = usage.character.limit
        percentage = count / limit * 100  # Output with 2 decimals.

        count_str = ut.format_char_count(count)
        limit_str = ut.format_char_count(limit)

        if limit == DEEPL_USAGE_UNLIMITED:
            self.label_api_usage.setText(f"{count_str} characters / Unlimited")
        else:
            self.label_api_usage.setText(f"{percentage:.2f}%  {count_str} / {limit_str} characters")

        if percentage < 90:
            self.label_api_usage_warn_icon.hide()
            self.label_api_usage_error_icon.hide()
        elif percentage < 100:
            self.label_api_usage_warn_icon.show()
            self.label_api_usage_error_icon.hide()
        else:
            self.label_api_usage_warn_icon.hide()
            self.label_api_usage_error_icon.show()

    def ready_to_translate(self) -> None:
        logger.info("Ready to translate.")
        if self.threadpool.activeThreadCount() > 0:
            logger.error("Threadpool still has active threads.")
        self.start_button_enabled(True)
        self.show_button_start()
        self.statusbar.showMessage("Ready to translate.")

    def not_ready_to_translate(self) -> None:
        logger.info("Not ready to translate.")
        self.start_button_enabled(False)
        self.show_button_start()

    def set_translation_parameters_enabled(self, enabled: bool) -> None:
        """
        When translating, language, output, glossary, and account settings must all be locked.

        :param enabled: Sets the enabled flag for all relevant widgets accordingly.
        """
        self.groupBox_language.setEnabled(enabled)
        self.groupBox_glossary.setEnabled(enabled)
        self.groupBox_api.setEnabled(enabled)
        self.checkBox_file_fixed_dir.setEnabled(enabled)
        self.lineEdit_file_out_dir.setEnabled(enabled)
        self.pushButton_file_dir_browse.setEnabled(enabled)

    def recalculate_char_total(self) -> None:
        """
        Calculate a new total of characters to translate and display it in the status bar.
        """
        char_total = sum(file.char_count for file in self.file_table.files.values())
        if char_total == 0:
            self.label_stats.setText("")
            return

        time_total = ceil(self.config.avg_time_per_mille * char_total / 1000)
        char_text = ut.format_char_count(char_total) + ut.f_plural(char_total, " character")
        time_text = f"Approx. {ut.f_time(time_total)}"
        self.label_stats.setText(char_text + "   " + time_text)

    def update_translation_status(self, processed_chars: int, char_total: int) -> None:
        """
        Update the translation status label.
        """
        if char_total == 0:
            logger.info("Total character count is 0. Nothing to do.")
            return
        char_text = ut.format_char_count(processed_chars) + " / " + ut.format_char_count(char_total)
        time_total = ceil(self.config.avg_time_per_mille * (char_total - processed_chars) / 1000)
        self.label_progress.setText(
            f"Translated {char_text} {ut.f_plural(char_total, 'character')}\n"
            f"Approximately {ut.f_time(time_total)} remaining"
        )
        self.progressBar.setValue(processed_chars / char_total * 100)

    # ========================================== Lock File ==========================================

    def test_and_set_lock_file(self) -> None:
        """
        Create a lock file to warn against multiple instances of the application from running at the same time.
        """
        # In debug mode, don't bother with the lock file. All of the frequent crashing and force quitting
        # will make it a nuisance.
        if self.debug:
            return

        lock_file = ut.get_lock_file_path()
        if lock_file.exists():
            # Check if the lock file is newer than the current uptime.
            if lock_file.stat().st_mtime >= psutil.boot_time():
                # Make sure other referenced PID is still running.
                if psutil.pid_exists(int(lock_file.read_text())):
                    logger.warning("Found active lock file.")
                    response = gu.show_critical(
                        self,
                        self.tr("Multiple Instances"),
                        self.tr(
                            "Another instance of DeepQt appears to be running already."
                            "Opening a new instance will make the old session unstable.\n\n"
                            "Continue anyway?"
                        ),
                        detailedText=self.tr("Found process ID in lock file: ")
                        + lock_file.read_text(),
                    )
                    if response == Qw.QMessageBox.Abort:
                        logger.critical("User aborted due to lock file.")
                        raise SystemExit(1)
                    logger.warning("User overrode lock file.")
                else:
                    logger.warning("Found lock file, but referenced PID is not running.")
            else:
                logger.warning(
                    "Found lock file, but it is older than the current uptime. Overwriting."
                )

        with lock_file.open("w") as file:
            file.write(str(Qw.QApplication.applicationPid()))

    def free_lock_file(self) -> None:
        """
        Remove the lock file.
        """
        if self.debug:
            return

        lock_file = ut.get_lock_file_path()
        if lock_file.exists():
            logger.debug("Removing lock file.")
            lock_file.unlink()
        else:
            logger.error("Lock file not found, a new instance was likely started.")

    # =========================================== Theming ===========================================

    def save_default_palette(self) -> None:
        self.default_palette = self.palette()
        # Patch palette to use the text color with 50% opacity for placeholder text.
        placeholder_color = self.default_palette.color(Qg.QPalette.Inactive, Qg.QPalette.Text)
        placeholder_color.setAlphaF(0.5)
        logger.debug(f"Placeholder color: {placeholder_color.name()}")
        self.default_palette.setColor(Qg.QPalette.PlaceholderText, placeholder_color)
        # self.default_icon_theme = Qg.QIcon.themeName()
        self.default_style = Qw.QApplication.style().objectName()

    def load_config_theme(self) -> None:
        """
        Load the theme specified in the config, or the system theme if none.
        """
        theme = self.config.gui_theme
        self.set_theme(theme)

    def set_theme(self, theme: str = "") -> None:
        """
        Apply the given theme to the application, or if none, revert to the default theme.
        """
        palette: Qg.QPalette

        if not theme:
            logger.info(f"Using system theme.")
            palette = self.default_palette
            # Qg.QIcon.setThemeName(self.default_icon_theme)
            # Check if we need to restore the style.
            if Qw.QApplication.style().objectName() != self.default_style:
                Qw.QApplication.setStyle(self.default_style)
        else:
            logger.info(f"Using theme: {theme}")
            palette = gu.load_color_palette(theme)

            Qg.QIcon.setThemeName(theme)
            if platform.system() == "Windows":
                Qw.QApplication.setStyle("Fusion")

        self.setPalette(palette)
        Qw.QApplication.setPalette(self.palette())

        # Check the brightness of the background color to determine if the theme is dark.
        # This is a heuristic, but it works well enough.
        background_color = palette.color(Qg.QPalette.Window)
        self.theme_is_dark.set(background_color.lightness() < 128)
        logger.info(f"Theme is dark: {self.theme_is_dark.get()}")
        self.theme_is_dark_changed.emit(self.theme_is_dark)

        # Also just setting the icon theme here, since with qt6 even breeze dark is having issues.
        # Update the fallback icon theme accordingly.
        if self.theme_is_dark.get():
            Qg.QIcon.setFallbackThemeName("breeze-dark")
            Qg.QIcon.setThemeName("breeze-dark")
            logger.info("Setting icon theme to breeze-dark.")
        else:
            Qg.QIcon.setFallbackThemeName("breeze")
            Qg.QIcon.setThemeName("breeze")
            logger.info("Setting icon theme to breeze.")

        # Toggle the theme menu items.
        for action in self.theming_menu.actions():
            action.setChecked(action.theme == theme)

        self.update()
        event = Qc.QEvent(Qc.QEvent.PaletteChange)
        self.widget_backend_status.changeEvent(event)
        self.label_glossary_help.changeEvent(event)
        self.label_outdir_help.changeEvent(event)

        # Update the config it necessary.
        prev_value = self.config.gui_theme
        if prev_value != theme:
            self.config.gui_theme = theme
            self.config.save()

    def changeEvent(self, event) -> None:
        """
        Listen for palette change events to notify all widgets.
        """
        if event.type() == Qc.QEvent.ApplicationPaletteChange:
            background_color = self.palette().color(Qg.QPalette.Window)
            self.theme_is_dark.set(background_color.lightness() < 128)
            logger.info(f"Theme is dark: {self.theme_is_dark.get()}")
            self.theme_is_dark_changed.emit(self.theme_is_dark)

    def simulate_crash(self) -> None:
        """
        Simulate a crash by raising an exception.
        """
        raise Exception("This is a simulated crash.")

    def start_memory_watcher(self) -> None:
        """
        Run the memory watcher in a separate thread.
        Callbacks are sent over signals.
        """
        self.memory_watcher = mw.MemoryWatcher()
        self.memory_watcher.oom_warning.connect(self.show_oom_warning)
        self.memory_watcher.oom_relaxed.connect(self.hide_oom_warning)
        self.memory_watcher.start()

    @Slot(str)
    def show_oom_warning(self, message: str) -> None:
        logger.warning(message)
        self.widget_oom_banner.show()
        self.label_oom_message.setText(message)

    def hide_oom_warning(self) -> None:
        self.widget_oom_banner.hide()

    def init_oom_banner(self) -> None:
        self.widget_oom_banner.hide()
        self.label_oom_icon.setPixmap(Qg.QIcon.fromTheme("dialog-warning").pixmap(24, 24))
        self.widget_oom_banner.setStyleSheet(f"background-color: #550000; color: #ffffff;")
        font = self.label_oom_message.font()
        font.setPointSize(round(font.pointSize() * 1.5))
        self.label_oom_message.setFont(font)


def nuke_epub_cache() -> None:
    """
    Perform a sanity check first. The folder must exist and be named "epub".
    """
    epub_cache_path = ut.epub_cache_path()
    if not epub_cache_path.is_dir():
        logger.info("Epub cache folder does not exist. Nothing to do.")
        return

    if epub_cache_path.name != "epubs":
        logger.error(
            f"Epub cache folder is not named 'epubs', instead {epub_cache_path}. Aborting."
        )
        return

    try:
        shutil.rmtree(epub_cache_path)
    except OSError as e:
        logger.error("Failed to delete epub cache folder.", exc_info=e)
        return
