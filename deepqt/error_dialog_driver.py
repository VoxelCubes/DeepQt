import PySide6.QtCore as Qc
import PySide6.QtGui as Qg
import PySide6.QtWidgets as Qw
from loguru import logger

import pcleaner.gui.log_parser as lp
from pcleaner.gui.ui_generated_files.ui_ErrorDialog import Ui_ErrorDialog


class ErrorDialog(Qw.QDialog, Ui_ErrorDialog):
    """
    Show logs of individual sessions and allow the user to report an issue.
    """

    session_log: lp.LogSession

    def __init__(
        self,
        parent=None,
        title: str = "Error",
        message: str = "An error occurred.",
    ) -> None:
        """
        Init the widget.

        :param parent: The parent widget.
        """
        Qw.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.label_error_icon.setPixmap(Qg.QIcon.fromTheme("dialog-error").pixmap(64, 64))

        self.setWindowTitle(title)
        self.label_message.setText(message)

        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_open_issues.clicked.connect(self.open_issues)
        self.pushButton_clipboard.clicked.connect(self.copy_to_clipboard)

        self.label_name_hidden.setText(
            self.tr("Note: Name {name} was hidden").format(name=lp.get_username())
        )
        self.load_session_log()

    @staticmethod
    def open_issues() -> None:
        """
        Open the issues page in the browser.
        """
        logger.debug("Opening github issues page.")
        Qg.QDesktopServices.openUrl(Qc.QUrl("https://github.com/VoxelCubes/PanelCleaner/issues"))

    def load_session_log(self) -> None:
        """
        Load the logs.
        """
        log_text = lp.load_log_file()
        if log_text is None:
            return

        sessions = lp.parse_log_file(log_text, max_sessions=1)
        if len(sessions) != 1:
            self.session_log = lp.LogSession(self.tr("Failed to load log."))
        else:
            self.session_log = lp.parse_log_file(log_text, max_sessions=1)[0]

        self.log_viewer.show_log(self.session_log.text)
        self.log_viewer.scroll_to_bottom()

    def copy_to_clipboard(self) -> None:
        """
        Copy the issue report to the clipboard.
        """
        logger.debug("Copying issue report to clipboard.")
        Qg.QGuiApplication.clipboard().setText(self.session_log.text)
