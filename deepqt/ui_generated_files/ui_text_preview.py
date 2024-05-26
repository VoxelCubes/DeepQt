# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'text_preview.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QDialog, QPushButton, QSizePolicy,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_TextPreview(object):
    def setupUi(self, TextPreview):
        if not TextPreview.objectName():
            TextPreview.setObjectName(u"TextPreview")
        TextPreview.resize(720, 800)
        self.verticalLayout = QVBoxLayout(TextPreview)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, -1)
        self.tabWidget = QTabWidget(TextPreview)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setUsesScrollButtons(False)

        self.verticalLayout.addWidget(self.tabWidget)

        self.pushButton_save = QPushButton(TextPreview)
        self.pushButton_save.setObjectName(u"pushButton_save")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_save.sizePolicy().hasHeightForWidth())
        self.pushButton_save.setSizePolicy(sizePolicy)
        icon = QIcon()
        iconThemeName = u"document-save"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_save.setIcon(icon)

        self.verticalLayout.addWidget(self.pushButton_save, 0, Qt.AlignHCenter)


        self.retranslateUi(TextPreview)

        QMetaObject.connectSlotsByName(TextPreview)
    # setupUi

    def retranslateUi(self, TextPreview):
        TextPreview.setWindowTitle(QCoreApplication.translate("TextPreview", u"Placeholder", None))
        self.pushButton_save.setText(QCoreApplication.translate("TextPreview", u"Save Preview to File", None))
    # retranslateUi

