import PySide6.QtWidgets as Qw

import deepq.config as cfg
from deepq.ui_generated_files.ui_api_config import Ui_Dialog_API


class ConfigureAccount(Qw.QDialog, Ui_Dialog_API):
    """
    A little dialog to enter the API key and account type.
    This way the API key is normally hidden from the user.
    """

    def __init__(self, parent, config: cfg.Config):
        Qw.QDialog.__init__(self, parent=parent)
        self.setupUi(self)

        self.lineEdit_api_key.setText(config.api_key)
        self.lineEdit_api_key.setFocus()

        self.comboBox_api_type.setCurrentIndex(1 if config.is_pro_version else 0)
