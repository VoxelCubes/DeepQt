# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QFormLayout,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTableWidgetItem, QVBoxLayout, QWidget)

from deepqt.CustomQ.CComboBox import CComboBox
from deepqt.file_table import FileTable

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 742)
        font = QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 6, -1, -1)
        self.groupBox_language = QGroupBox(self.centralwidget)
        self.groupBox_language.setObjectName(u"groupBox_language")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_language.sizePolicy().hasHeightForWidth())
        self.groupBox_language.setSizePolicy(sizePolicy)
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_language)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.groupBox_language)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.comboBox_lang_from = CComboBox(self.groupBox_language)
        self.comboBox_lang_from.setObjectName(u"comboBox_lang_from")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_lang_from.sizePolicy().hasHeightForWidth())
        self.comboBox_lang_from.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.comboBox_lang_from)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_3 = QLabel(self.groupBox_language)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_6.addWidget(self.label_3)

        self.comboBox_lang_to = CComboBox(self.groupBox_language)
        self.comboBox_lang_to.setObjectName(u"comboBox_lang_to")
        sizePolicy1.setHeightForWidth(self.comboBox_lang_to.sizePolicy().hasHeightForWidth())
        self.comboBox_lang_to.setSizePolicy(sizePolicy1)

        self.horizontalLayout_6.addWidget(self.comboBox_lang_to)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)


        self.verticalLayout.addWidget(self.groupBox_language)

        self.groupBox_files = QGroupBox(self.centralwidget)
        self.groupBox_files.setObjectName(u"groupBox_files")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_files)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton_file_remove = QPushButton(self.groupBox_files)
        self.pushButton_file_remove.setObjectName(u"pushButton_file_remove")
        icon = QIcon()
        iconThemeName = u"edit-delete-remove"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_file_remove.setIcon(icon)

        self.gridLayout_2.addWidget(self.pushButton_file_remove, 1, 0, 1, 1)

        self.pushButton_file_remove_all = QPushButton(self.groupBox_files)
        self.pushButton_file_remove_all.setObjectName(u"pushButton_file_remove_all")
        icon1 = QIcon()
        iconThemeName = u"edit-delete"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_file_remove_all.setIcon(icon1)

        self.gridLayout_2.addWidget(self.pushButton_file_remove_all, 1, 1, 1, 1)

        self.pushButton_file_add = QPushButton(self.groupBox_files)
        self.pushButton_file_add.setObjectName(u"pushButton_file_add")
        icon2 = QIcon()
        iconThemeName = u"list-add"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_file_add.setIcon(icon2)

        self.gridLayout_2.addWidget(self.pushButton_file_add, 0, 0, 1, 1)

        self.pushButton_file_preview = QPushButton(self.groupBox_files)
        self.pushButton_file_preview.setObjectName(u"pushButton_file_preview")
        icon3 = QIcon()
        iconThemeName = u"document-preview"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_file_preview.setIcon(icon3)

        self.gridLayout_2.addWidget(self.pushButton_file_preview, 0, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_2)

        self.checkBox_file_fixed_dir = QCheckBox(self.groupBox_files)
        self.checkBox_file_fixed_dir.setObjectName(u"checkBox_file_fixed_dir")

        self.verticalLayout_4.addWidget(self.checkBox_file_fixed_dir)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lineEdit_file_out_dir = QLineEdit(self.groupBox_files)
        self.lineEdit_file_out_dir.setObjectName(u"lineEdit_file_out_dir")
        self.lineEdit_file_out_dir.setClearButtonEnabled(True)

        self.horizontalLayout_4.addWidget(self.lineEdit_file_out_dir)

        self.pushButton_file_dir_browse = QPushButton(self.groupBox_files)
        self.pushButton_file_dir_browse.setObjectName(u"pushButton_file_dir_browse")
        icon4 = QIcon()
        iconThemeName = u"document-open-folder"
        if QIcon.hasThemeIcon(iconThemeName):
            icon4 = QIcon.fromTheme(iconThemeName)
        else:
            icon4.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_file_dir_browse.setIcon(icon4)
        self.pushButton_file_dir_browse.setFlat(True)

        self.horizontalLayout_4.addWidget(self.pushButton_file_dir_browse)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addWidget(self.groupBox_files)

        self.groupBox_glossary = QGroupBox(self.centralwidget)
        self.groupBox_glossary.setObjectName(u"groupBox_glossary")
        sizePolicy.setHeightForWidth(self.groupBox_glossary.sizePolicy().hasHeightForWidth())
        self.groupBox_glossary.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_glossary)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.checkBox_use_glossary = QCheckBox(self.groupBox_glossary)
        self.checkBox_use_glossary.setObjectName(u"checkBox_use_glossary")
        self.checkBox_use_glossary.setChecked(True)

        self.horizontalLayout_8.addWidget(self.checkBox_use_glossary)

        self.pushButton_glossary_help = QPushButton(self.groupBox_glossary)
        self.pushButton_glossary_help.setObjectName(u"pushButton_glossary_help")
        icon5 = QIcon()
        iconThemeName = u"help-about"
        if QIcon.hasThemeIcon(iconThemeName):
            icon5 = QIcon.fromTheme(iconThemeName)
        else:
            icon5.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_glossary_help.setIcon(icon5)
        self.pushButton_glossary_help.setFlat(True)

        self.horizontalLayout_8.addWidget(self.pushButton_glossary_help)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_glossary_file = QLineEdit(self.groupBox_glossary)
        self.lineEdit_glossary_file.setObjectName(u"lineEdit_glossary_file")
        self.lineEdit_glossary_file.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.lineEdit_glossary_file)

        self.pushButton_glossary_file_browse = QPushButton(self.groupBox_glossary)
        self.pushButton_glossary_file_browse.setObjectName(u"pushButton_glossary_file_browse")
        icon6 = QIcon()
        iconThemeName = u"document-open"
        if QIcon.hasThemeIcon(iconThemeName):
            icon6 = QIcon.fromTheme(iconThemeName)
        else:
            icon6.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_glossary_file_browse.setIcon(icon6)
        self.pushButton_glossary_file_browse.setFlat(True)

        self.horizontalLayout.addWidget(self.pushButton_glossary_file_browse)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.checkBox_extra_quote_protection = QCheckBox(self.groupBox_glossary)
        self.checkBox_extra_quote_protection.setObjectName(u"checkBox_extra_quote_protection")
        self.checkBox_extra_quote_protection.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_extra_quote_protection)


        self.verticalLayout.addWidget(self.groupBox_glossary)

        self.groupBox_api = QGroupBox(self.centralwidget)
        self.groupBox_api.setObjectName(u"groupBox_api")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_api)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_5 = QLabel(self.groupBox_api)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_api_status_good_icon = QLabel(self.groupBox_api)
        self.label_api_status_good_icon.setObjectName(u"label_api_status_good_icon")

        self.horizontalLayout_2.addWidget(self.label_api_status_good_icon)

        self.label_api_status_good = QLabel(self.groupBox_api)
        self.label_api_status_good.setObjectName(u"label_api_status_good")

        self.horizontalLayout_2.addWidget(self.label_api_status_good)

        self.label_api_status_bad_icon = QLabel(self.groupBox_api)
        self.label_api_status_bad_icon.setObjectName(u"label_api_status_bad_icon")

        self.horizontalLayout_2.addWidget(self.label_api_status_bad_icon)

        self.label_api_status_bad = QLabel(self.groupBox_api)
        self.label_api_status_bad.setObjectName(u"label_api_status_bad")

        self.horizontalLayout_2.addWidget(self.label_api_status_bad)

        self.horizontalSpacer_2 = QSpacerItem(0, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButton_refresh = QPushButton(self.groupBox_api)
        self.pushButton_refresh.setObjectName(u"pushButton_refresh")
        self.pushButton_refresh.setText(u"")
        icon7 = QIcon()
        iconThemeName = u"view-refresh"
        if QIcon.hasThemeIcon(iconThemeName):
            icon7 = QIcon.fromTheme(iconThemeName)
        else:
            icon7.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_refresh.setIcon(icon7)
        self.pushButton_refresh.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton_refresh)


        self.formLayout_2.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_6 = QLabel(self.groupBox_api)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_6)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_api_usage_error_icon = QLabel(self.groupBox_api)
        self.label_api_usage_error_icon.setObjectName(u"label_api_usage_error_icon")

        self.horizontalLayout_10.addWidget(self.label_api_usage_error_icon)

        self.label_api_usage_warn_icon = QLabel(self.groupBox_api)
        self.label_api_usage_warn_icon.setObjectName(u"label_api_usage_warn_icon")

        self.horizontalLayout_10.addWidget(self.label_api_usage_warn_icon)

        self.label_api_usage = QLabel(self.groupBox_api)
        self.label_api_usage.setObjectName(u"label_api_usage")

        self.horizontalLayout_10.addWidget(self.label_api_usage)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_3)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_10)


        self.verticalLayout_3.addLayout(self.formLayout_2)

        self.pushButton_api_config = QPushButton(self.groupBox_api)
        self.pushButton_api_config.setObjectName(u"pushButton_api_config")
        icon8 = QIcon()
        iconThemeName = u"configure"
        if QIcon.hasThemeIcon(iconThemeName):
            icon8 = QIcon.fromTheme(iconThemeName)
        else:
            icon8.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_api_config.setIcon(icon8)

        self.verticalLayout_3.addWidget(self.pushButton_api_config)


        self.verticalLayout.addWidget(self.groupBox_api)

        self.verticalSpacer = QSpacerItem(350, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButton_start = QPushButton(self.centralwidget)
        self.pushButton_start.setObjectName(u"pushButton_start")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.pushButton_start.setFont(font1)
        icon9 = QIcon()
        iconThemeName = u"media-playback-start"
        if QIcon.hasThemeIcon(iconThemeName):
            icon9 = QIcon.fromTheme(iconThemeName)
        else:
            icon9.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_start.setIcon(icon9)

        self.horizontalLayout_9.addWidget(self.pushButton_start)

        self.pushButton_abort = QPushButton(self.centralwidget)
        self.pushButton_abort.setObjectName(u"pushButton_abort")
        self.pushButton_abort.setFont(font1)
        icon10 = QIcon()
        iconThemeName = u"process-stop"
        if QIcon.hasThemeIcon(iconThemeName):
            icon10 = QIcon.fromTheme(iconThemeName)
        else:
            icon10.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_abort.setIcon(icon10)

        self.horizontalLayout_9.addWidget(self.pushButton_abort)


        self.verticalLayout.addLayout(self.horizontalLayout_9)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.file_table = FileTable(self.centralwidget)
        if (self.file_table.columnCount() < 5):
            self.file_table.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.file_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.file_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.file_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.file_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.file_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.file_table.setObjectName(u"file_table")
        self.file_table.setFocusPolicy(Qt.NoFocus)
        self.file_table.setAcceptDrops(True)
        self.file_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.file_table.setAlternatingRowColors(True)
        self.file_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_table.setTextElideMode(Qt.ElideNone)
        self.file_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.file_table.setCornerButtonEnabled(False)
        self.file_table.horizontalHeader().setDefaultSectionSize(100)
        self.file_table.horizontalHeader().setStretchLastSection(True)
        self.file_table.verticalHeader().setMinimumSectionSize(40)
        self.file_table.verticalHeader().setDefaultSectionSize(40)

        self.gridLayout.addWidget(self.file_table, 0, 1, 1, 1)

        self.label_progress = QLabel(self.centralwidget)
        self.label_progress.setObjectName(u"label_progress")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_progress.sizePolicy().hasHeightForWidth())
        self.label_progress.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label_progress, 1, 0, 1, 1)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.gridLayout.addWidget(self.progressBar, 1, 1, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"placeholder", None))
        self.groupBox_language.setTitle(QCoreApplication.translate("MainWindow", u"Language", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"From:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"To:", None))
        self.groupBox_files.setTitle(QCoreApplication.translate("MainWindow", u"Input Files", None))
        self.pushButton_file_remove.setText(QCoreApplication.translate("MainWindow", u"Remove file", None))
        self.pushButton_file_remove_all.setText(QCoreApplication.translate("MainWindow", u"Clear all", None))
        self.pushButton_file_add.setText(QCoreApplication.translate("MainWindow", u"Add file", None))
        self.pushButton_file_preview.setText(QCoreApplication.translate("MainWindow", u"Preview", None))
        self.checkBox_file_fixed_dir.setText(QCoreApplication.translate("MainWindow", u"Use fixed output directory:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_file_dir_browse.setToolTip(QCoreApplication.translate("MainWindow", u"Browse", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_file_dir_browse.setText("")
        self.groupBox_glossary.setTitle(QCoreApplication.translate("MainWindow", u"Glossary", None))
        self.checkBox_use_glossary.setText(QCoreApplication.translate("MainWindow", u"Use glossary:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_glossary_help.setToolTip(QCoreApplication.translate("MainWindow", u"This glossary does not use DeepL's glossaries. Click for more details.", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_glossary_help.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_glossary_file_browse.setToolTip(QCoreApplication.translate("MainWindow", u"Browse", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_glossary_file_browse.setText("")
        self.checkBox_extra_quote_protection.setText(QCoreApplication.translate("MainWindow", u"Use extra quotation protection", None))
        self.groupBox_api.setTitle(QCoreApplication.translate("MainWindow", u"API", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Status:", None))
        self.label_api_status_good_icon.setText(QCoreApplication.translate("MainWindow", u"okay_icon", None))
        self.label_api_status_good.setText(QCoreApplication.translate("MainWindow", u"Okay", None))
        self.label_api_status_bad_icon.setText(QCoreApplication.translate("MainWindow", u"error_icon", None))
        self.label_api_status_bad.setText(QCoreApplication.translate("MainWindow", u"Error", None))
#if QT_CONFIG(tooltip)
        self.pushButton_refresh.setToolTip(QCoreApplication.translate("MainWindow", u"Refresh", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Usage:", None))
        self.label_api_usage_error_icon.setText(QCoreApplication.translate("MainWindow", u"error_icon", None))
        self.label_api_usage_warn_icon.setText(QCoreApplication.translate("MainWindow", u"warn_icon", None))
        self.label_api_usage.setText(QCoreApplication.translate("MainWindow", u"usage_placeholder", None))
        self.pushButton_api_config.setText(QCoreApplication.translate("MainWindow", u"Account settings", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButton_abort.setText(QCoreApplication.translate("MainWindow", u"Abort", None))
        ___qtablewidgetitem = self.file_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"ID", None));
        ___qtablewidgetitem1 = self.file_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"File Name", None));
        ___qtablewidgetitem2 = self.file_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtablewidgetitem3 = self.file_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Characters", None));
        ___qtablewidgetitem4 = self.file_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Output Path", None));
        self.label_progress.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

