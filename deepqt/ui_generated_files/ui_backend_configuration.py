# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'backend_configuration.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QFrame, QHBoxLayout, QLabel,
    QListWidgetItem, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from deepqt.CustomQ.CListWidget import CListWidget
from deepqt.backend_settings import BackendSettings

class Ui_BackendConfiguration(object):
    def setupUi(self, BackendConfiguration):
        if not BackendConfiguration.objectName():
            BackendConfiguration.setObjectName(u"BackendConfiguration")
        BackendConfiguration.resize(649, 520)
        self.horizontalLayout_2 = QHBoxLayout(BackendConfiguration)
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.listWidget_backends = CListWidget(BackendConfiguration)
        self.listWidget_backends.setObjectName(u"listWidget_backends")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_backends.sizePolicy().hasHeightForWidth())
        self.listWidget_backends.setSizePolicy(sizePolicy)
        self.listWidget_backends.setMinimumSize(QSize(200, 0))
        self.listWidget_backends.setMaximumSize(QSize(200, 16777215))
        self.listWidget_backends.setFrameShape(QFrame.NoFrame)
        self.listWidget_backends.setFrameShadow(QFrame.Plain)
        self.listWidget_backends.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listWidget_backends.setProperty("showDropIndicator", False)
        self.listWidget_backends.setIconSize(QSize(24, 24))
        self.listWidget_backends.setSpacing(6)

        self.horizontalLayout_2.addWidget(self.listWidget_backends)

        self.line = QFrame(BackendConfiguration)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(24)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_icon = QLabel(BackendConfiguration)
        self.label_icon.setObjectName(u"label_icon")
        self.label_icon.setText(u"<icon>")

        self.horizontalLayout.addWidget(self.label_icon)

        self.horizontalSpacer = QSpacerItem(12, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_backend_name = QLabel(BackendConfiguration)
        self.label_backend_name.setObjectName(u"label_backend_name")
        self.label_backend_name.setText(u"<backend name>")

        self.horizontalLayout.addWidget(self.label_backend_name)

        self.label_cost_icon = QLabel(BackendConfiguration)
        self.label_cost_icon.setObjectName(u"label_cost_icon")

        self.horizontalLayout.addWidget(self.label_cost_icon)

        self.label_reliability_icon = QLabel(BackendConfiguration)
        self.label_reliability_icon.setObjectName(u"label_reliability_icon")
        self.label_reliability_icon.setText(u"<reliability icon>")

        self.horizontalLayout.addWidget(self.label_reliability_icon)

        self.horizontalLayout.setStretch(2, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_description = QLabel(BackendConfiguration)
        self.label_description.setObjectName(u"label_description")
        self.label_description.setText(u"*description*")
        self.label_description.setTextFormat(Qt.MarkdownText)
        self.label_description.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_description, 0, Qt.AlignTop)

        self.scrollArea = QScrollArea(BackendConfiguration)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.backend_settings = BackendSettings()
        self.backend_settings.setObjectName(u"backend_settings")
        self.backend_settings.setGeometry(QRect(0, 0, 408, 350))
        self.scrollArea.setWidget(self.backend_settings)

        self.verticalLayout.addWidget(self.scrollArea)

        self.buttonBox = QDialogButtonBox(BackendConfiguration)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.RestoreDefaults)

        self.verticalLayout.addWidget(self.buttonBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_2.setStretch(2, 1)

        self.retranslateUi(BackendConfiguration)
        self.buttonBox.accepted.connect(BackendConfiguration.accept)
        self.buttonBox.rejected.connect(BackendConfiguration.reject)

        QMetaObject.connectSlotsByName(BackendConfiguration)
    # setupUi

    def retranslateUi(self, BackendConfiguration):
        BackendConfiguration.setWindowTitle(QCoreApplication.translate("BackendConfiguration", u"Translation Services", None))
        self.label_cost_icon.setText(QCoreApplication.translate("BackendConfiguration", u"<cost icon>", None))
    # retranslateUi

