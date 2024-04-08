import PySide6.QtWidgets as Qw

import deepqt.constants as ct
from deepqt.ui_generated_files.ui_api_key_input import Ui_Dialog_API
from deepqt.gui_utils import show_info


class KeyInputDialog(Qw.QDialog, Ui_Dialog_API):
    """
    A little dialog to enter the API key.
    This way the API key is normally hidden from the user.
    """

    key: ct.APIKey
    help_html: ct.HTML

    def __init__(self, parent, key: ct.APIKey, help_html: ct.HTML) -> None:
        # Don't pass the parent due to a bug in PySide6.
        Qw.QDialog.__init__(self)
        self.setupUi(self)

        self.lineEdit_api_key.setText(key)
        self.lineEdit_api_key.setFocus()

        self.key = key
        self.help_html = help_html

        if help_html:
            self.buttonBox.helpRequested.connect(self.show_api_help)
        else:
            # Hide the help button.
            self.buttonBox.button(Qw.QDialogButtonBox.Help).hide()

    def get_key(self) -> ct.APIKey:
        return ct.APIKey(self.lineEdit_api_key.text().strip())

    def show_api_help(self) -> None:
        show_info(self, "API Help", self.help_html)
