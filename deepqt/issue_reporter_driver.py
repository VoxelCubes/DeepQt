from datetime import datetime
from typing import Sequence

import PySide6.QtCore as Qc
import PySide6.QtGui as Qg
import PySide6.QtWidgets as Qw
from loguru import logger

import deepqt.log_parser as lp
import deepqt.utils as ut
from deepqt.ui_generated_files.ui_IssueReporter import Ui_IssueReporter


class IssueReporter(Qw.QDialog, Ui_IssueReporter):
    """
    Show logs of individual sessions and allow the user to report an issue.
    """

    sessions: Sequence[lp.LogSession]

    def __init__(
        self,
        parent=None,
    ) -> None:
        """
        Init the widget.

        :param parent: The parent widget.
        """
        Qw.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_open_issues.clicked.connect(self.open_issues)
        self.pushButton_clipboard.clicked.connect(self.copy_to_clipboard)

        self.load_logs()
        # Only connect the signal after the logs are loaded to not double-trigger
        # the update when making the initial selection.
        self.comboBox_sessions.currentIndexChanged.connect(self.show_log)
        self.show_log()

        self.label_log_path.setText(str(ut.get_log_path()))
        self.label_name_hidden.setText("Note: Name {name} and api keys were hidden".format(name=lp.get_username()))

    def load_logs(self) -> None:
        """
        Load the logs.
        """

        log_text = lp.load_log_file()
        if log_text is None:
            return

        self.sessions = lp.parse_log_file(log_text)

        for index, session in enumerate(self.sessions):
            text: str
            if session.corrupted:
                text = "Corrupted log session"
            elif index == 0:
                text = "Current session"
            else:
                today = datetime.now().date()
                if session.date_time.date() == today:
                    text = "Today" + session.date_time.strftime(" %H:%M:%S")
                else:
                    text = session.date_time.strftime("%Y-%m-%d %H:%M:%S")

            if session.errors or session.criticals:
                text += " – "
            if session.errors:
                text += f"{session.errors} " + ut.f_plural(session.errors, "Error", "Errors")
                if session.criticals:
                    text += ", "
            if session.criticals:
                text += f"{session.criticals} " + ut.f_plural(session.criticals, "Critical", "Criticals")

            self.comboBox_sessions.addTextItemLinkedData(text, index)

    def show_log(self) -> None:
        """
        Show the log in the text edit.
        """

        session_index = self.comboBox_sessions.currentLinkedData()

        session = self.sessions[session_index]
        self.log_viewer.show_log(session.text)

    @staticmethod
    def open_issues() -> None:
        """
        Open the issues page in the browser.
        """
        logger.debug("Opening github issues page.")
        Qg.QDesktopServices.openUrl(Qc.QUrl("https://github.com/VoxelCubes/DeepQt/issues"))

    def copy_to_clipboard(self) -> None:
        """
        Copy the issue report to the clipboard.
        """
        logger.debug("Copying issue report to clipboard.")
        text = self.log_viewer.get_log()
        Qg.QGuiApplication.clipboard().setText(text)
