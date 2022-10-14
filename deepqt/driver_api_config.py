import PySide6.QtWidgets as Qw

import deepqt.config as cfg
from deepqt.ui_generated_files.ui_api_config import Ui_Dialog_API
from deepqt.helpers import show_info


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

        self.buttonBox.helpRequested.connect(self.show_api_help)

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
