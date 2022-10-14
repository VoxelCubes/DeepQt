# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'api_config.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QLabel, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Dialog_API(object):
    def setupUi(self, Dialog_API):
        if not Dialog_API.objectName():
            Dialog_API.setObjectName(u"Dialog_API")
        Dialog_API.resize(450, 125)
        self.verticalLayout = QVBoxLayout(Dialog_API)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Dialog_API)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit_api_key = QLineEdit(Dialog_API)
        self.lineEdit_api_key.setObjectName(u"lineEdit_api_key")
        self.lineEdit_api_key.setMaxLength(100)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_api_key)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(Dialog_API)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Help|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog_API)
        self.buttonBox.accepted.connect(Dialog_API.accept)
        self.buttonBox.rejected.connect(Dialog_API.reject)

        QMetaObject.connectSlotsByName(Dialog_API)
    # setupUi

    def retranslateUi(self, Dialog_API):
        Dialog_API.setWindowTitle(QCoreApplication.translate("Dialog_API", u"Account Settings", None))
        self.label.setText(QCoreApplication.translate("Dialog_API", u"API Key:", None))
    # retranslateUi

