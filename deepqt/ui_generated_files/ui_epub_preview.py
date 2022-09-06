# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'epub_preview.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QPushButton,
    QRadioButton, QSizePolicy, QStackedWidget, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_EpubPreview(object):
    def setupUi(self, EpubPreview):
        if not EpubPreview.objectName():
            EpubPreview.setObjectName(u"EpubPreview")
        EpubPreview.resize(720, 800)
        self.verticalLayout = QVBoxLayout(EpubPreview)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 6, 0, -1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButton_original = QRadioButton(EpubPreview)
        self.radioButton_original.setObjectName(u"radioButton_original")
        self.radioButton_original.setChecked(True)

        self.horizontalLayout.addWidget(self.radioButton_original)

        self.radioButton_glossary = QRadioButton(EpubPreview)
        self.radioButton_glossary.setObjectName(u"radioButton_glossary")

        self.horizontalLayout.addWidget(self.radioButton_glossary)

        self.radioButton_translation = QRadioButton(EpubPreview)
        self.radioButton_translation.setObjectName(u"radioButton_translation")

        self.horizontalLayout.addWidget(self.radioButton_translation)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.stackedWidget = QStackedWidget(EpubPreview)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_original = QWidget()
        self.page_original.setObjectName(u"page_original")
        self.verticalLayout_4 = QVBoxLayout(self.page_original)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_original = QTabWidget(self.page_original)
        self.tabWidget_original.setObjectName(u"tabWidget_original")

        self.verticalLayout_4.addWidget(self.tabWidget_original)

        self.stackedWidget.addWidget(self.page_original)
        self.page_glossary = QWidget()
        self.page_glossary.setObjectName(u"page_glossary")
        self.verticalLayout_3 = QVBoxLayout(self.page_glossary)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_glossary = QTabWidget(self.page_glossary)
        self.tabWidget_glossary.setObjectName(u"tabWidget_glossary")

        self.verticalLayout_3.addWidget(self.tabWidget_glossary)

        self.stackedWidget.addWidget(self.page_glossary)
        self.page_translated = QWidget()
        self.page_translated.setObjectName(u"page_translated")
        self.verticalLayout_2 = QVBoxLayout(self.page_translated)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_translation = QTabWidget(self.page_translated)
        self.tabWidget_translation.setObjectName(u"tabWidget_translation")

        self.verticalLayout_2.addWidget(self.tabWidget_translation)

        self.stackedWidget.addWidget(self.page_translated)

        self.verticalLayout.addWidget(self.stackedWidget)

        self.pushButton_save = QPushButton(EpubPreview)
        self.pushButton_save.setObjectName(u"pushButton_save")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
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


        self.retranslateUi(EpubPreview)

        QMetaObject.connectSlotsByName(EpubPreview)
    # setupUi

    def retranslateUi(self, EpubPreview):
        EpubPreview.setWindowTitle(QCoreApplication.translate("EpubPreview", u"Placeholder", None))
        self.radioButton_original.setText(QCoreApplication.translate("EpubPreview", u"Original", None))
        self.radioButton_glossary.setText(QCoreApplication.translate("EpubPreview", u"Glossary", None))
        self.radioButton_translation.setText(QCoreApplication.translate("EpubPreview", u"Translated", None))
        self.pushButton_save.setText(QCoreApplication.translate("EpubPreview", u"Save Preview to File", None))
    # retranslateUi

