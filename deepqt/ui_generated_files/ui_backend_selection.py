# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'backend_selection.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QScrollArea, QSizePolicy, QVBoxLayout, QWidget)

from deepqt.backend_settings import BackendSettings

class Ui_BackendSelector(object):
    def setupUi(self, BackendSelector):
        if not BackendSelector.objectName():
            BackendSelector.setObjectName(u"BackendSelector")
        BackendSelector.resize(649, 520)
        self.horizontalLayout_2 = QHBoxLayout(BackendSelector)
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.listWidget_backends = QListWidget(BackendSelector)
        self.listWidget_backends.setObjectName(u"listWidget_backends")

        self.horizontalLayout_2.addWidget(self.listWidget_backends)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_icon = QLabel(BackendSelector)
        self.label_icon.setObjectName(u"label_icon")

        self.horizontalLayout.addWidget(self.label_icon)

        self.label_backend_name = QLabel(BackendSelector)
        self.label_backend_name.setObjectName(u"label_backend_name")

        self.horizontalLayout.addWidget(self.label_backend_name)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_description = QLabel(BackendSelector)
        self.label_description.setObjectName(u"label_description")

        self.verticalLayout.addWidget(self.label_description, 0, Qt.AlignTop)

        self.scrollArea = QScrollArea(BackendSelector)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.backend_settings = BackendSettings()
        self.backend_settings.setObjectName(u"backend_settings")
        self.backend_settings.setGeometry(QRect(0, 0, 411, 382))
        self.scrollArea.setWidget(self.backend_settings)

        self.verticalLayout.addWidget(self.scrollArea)

        self.buttonBox = QDialogButtonBox(BackendSelector)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.RestoreDefaults)

        self.verticalLayout.addWidget(self.buttonBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)

        self.retranslateUi(BackendSelector)
        self.buttonBox.accepted.connect(BackendSelector.accept)
        self.buttonBox.rejected.connect(BackendSelector.reject)

        QMetaObject.connectSlotsByName(BackendSelector)
    # setupUi

    def retranslateUi(self, BackendSelector):
        BackendSelector.setWindowTitle(QCoreApplication.translate("BackendSelector", u"Translation Services", None))
        self.label_icon.setText(QCoreApplication.translate("BackendSelector", u"<icon>", None))
        self.label_backend_name.setText(QCoreApplication.translate("BackendSelector", u"<backend name>", None))
        self.label_description.setText(QCoreApplication.translate("BackendSelector", u"<description>", None))
    # retranslateUi

