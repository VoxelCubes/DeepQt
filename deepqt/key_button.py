import PySide6.QtWidgets as Qw
import PySide6.QtGui as Qg
import PySide6.QtCore as Qc
from PySide6.QtCore import Qt

import deepqt.constants as ct
import deepqt.driver_api_key_input as dak


class APIKeyButton(Qw.QPushButton):
    """
    A button to show the API key dialog, while also storing the key.
    """

    key: ct.APIKey | None
    help_html: ct.HTML | None

    def __init__(self, parent=None) -> None:
        """
        Set up a button to show the API key dialog.

        :param parent: Parent widget.
        """
        # Qg.QIcon.fromTheme("database-change-key")
        super(APIKeyButton, self).__init__("Set Key", parent)

        self.key = None
        self.help_html = None
        self.clicked.connect(self.get_input)

    def setup(self, key: ct.APIKey, help_html: ct.HTML = "") -> None:
        """
        Set the key and help text. This must be done before the button is clicked.

        :param key: The API key.
        :param help_html: [Optional] The help text for the API key. Leave empty for no help.
        """
        self.key = key
        self.help_html = help_html

    def get_key(self) -> ct.APIKey:
        """
        Get the API key.
        """
        return self.key

    def set_key(self, key: ct.APIKey) -> None:
        """
        Set the API key.
        """
        self.key = key

    def get_input(self) -> None:
        """
        Show the API key dialog.
        """
        dialog = dak.KeyInputDialog(self, self.key, self.help_html)
        if dialog.exec():
            self.key = dialog.get_key()
