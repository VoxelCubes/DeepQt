import re
import PySide6.QtWidgets as Qw

import deepqt.config as cfg
from deepqt.ui_generated_files.ui_api_config import Ui_Dialog_API
from deepqt.gui_utils import show_info


class ConfigureAccount(Qw.QDialog, Ui_Dialog_API):
    """
    A little dialog to enter the API key and account type.
    This way the API key is normally hidden from the user.
    """

    def __init__(self, parent, config: cfg.Config):
        # Don't pass the parent due to a bug in PySide6.
        Qw.QDialog.__init__(self)
        self.setupUi(self)

        self.lineEdit_api_key.setText(config.api_key)
        self.lineEdit_api_key.setFocus()

        self.buttonBox.helpRequested.connect(self.show_api_help)

        self.comboBox_api_type.setCurrentIndex(1 if config.is_pro_version else 0)

    def get_key(self):
        """
        If the api is supposed to be PRO, remove :fx from the key and vice versa.
        """
        key = self.lineEdit_api_key.text().strip()
        # Don't try to fix an empty key.
        if key == "":
            return key

        if self.comboBox_api_type.currentIndex() == 1:
            key = re.sub(":fx$", "", key)
        else:
            key = re.sub("^(.*?)(:fx)?$", r"\1:fx", key)
        return key

    def show_api_help(self):
        """
        Show the deepl api documentation in a web browser.
        Open the github page for this.
        """
        show_info(
            self,
            "Glossary info",
            # language=HTML
            """<html>
                    <head/>
                    <body>
                        <p> To use this application you need a DeepL API key.
                            You can get one by signing up for an account at 
                            <a href="https://www.deepl.com/pro-api">
                                deepl.com
                            </a>.
                        </p>
                        <p>
                           For more information on the API, see the 
                            <a href="https://github.com/VoxelCubes/DeepQt/blob/master/docs/api_help.md">
                                online documentation
                            </a>
                            .
                        </p>
                    </body>
                </html>""",
        )
