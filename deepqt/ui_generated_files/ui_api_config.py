# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'api_config.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_Dialog_API(object):
    def setupUi(self, Dialog_API):
        if not Dialog_API.objectName():
            Dialog_API.setObjectName("Dialog_API")
        Dialog_API.resize(450, 200)
        self.verticalLayout = QVBoxLayout(Dialog_API)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QLabel(Dialog_API)
        self.label.setObjectName("label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit_api_key = QLineEdit(Dialog_API)
        self.lineEdit_api_key.setObjectName("lineEdit_api_key")
        self.lineEdit_api_key.setMaxLength(100)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_api_key)

        self.label_2 = QLabel(Dialog_API)
        self.label_2.setObjectName("label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.comboBox_api_type = QComboBox(Dialog_API)
        self.comboBox_api_type.addItem("")
        self.comboBox_api_type.addItem("")
        self.comboBox_api_type.setObjectName("comboBox_api_type")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBox_api_type)

        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(Dialog_API)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Help | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_API)
        self.buttonBox.accepted.connect(Dialog_API.accept)
        self.buttonBox.rejected.connect(Dialog_API.reject)

        QMetaObject.connectSlotsByName(Dialog_API)

    # setupUi

    def retranslateUi(self, Dialog_API):
        Dialog_API.setWindowTitle(QCoreApplication.translate("Dialog_API", "Account Settings", None))
        self.label.setText(QCoreApplication.translate("Dialog_API", "API Key:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog_API", "Account Type:", None))
        self.comboBox_api_type.setItemText(0, QCoreApplication.translate("Dialog_API", "DeepL API FREE", None))
        self.comboBox_api_type.setItemText(1, QCoreApplication.translate("Dialog_API", "DeepL API PRO", None))

    # retranslateUi
