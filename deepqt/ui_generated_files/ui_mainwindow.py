# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPlainTextEdit,
    QProgressBar, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QStackedWidget, QStatusBar,
    QTableWidgetItem, QVBoxLayout, QWidget)

from deepqt.CustomQ.CComboBox import CComboBox
from deepqt.CustomQ.CDropFrame import CDropFrame
from deepqt.CustomQ.CTooltipLabel import CTooltipLabel
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
        self.gridLayout.setHorizontalSpacing(12)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_translate_files = QPushButton(self.centralwidget)
        self.pushButton_translate_files.setObjectName(u"pushButton_translate_files")
        icon = QIcon()
        iconThemeName = u"document-multiple"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_translate_files.setIcon(icon)
        self.pushButton_translate_files.setCheckable(True)
        self.pushButton_translate_files.setAutoExclusive(True)
        self.pushButton_translate_files.setAutoDefault(True)

        self.horizontalLayout_3.addWidget(self.pushButton_translate_files)

        self.pushButton_translate_text = QPushButton(self.centralwidget)
        self.pushButton_translate_text.setObjectName(u"pushButton_translate_text")
        icon1 = QIcon()
        iconThemeName = u"view-list-text"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_translate_text.setIcon(icon1)
        self.pushButton_translate_text.setCheckable(True)
        self.pushButton_translate_text.setAutoExclusive(True)
        self.pushButton_translate_text.setAutoDefault(True)

        self.horizontalLayout_3.addWidget(self.pushButton_translate_text)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.pushButton_menu = QPushButton(self.centralwidget)
        self.pushButton_menu.setObjectName(u"pushButton_menu")
        icon2 = QIcon()
        iconThemeName = u"application-menu"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_menu.setIcon(icon2)
        self.pushButton_menu.setFlat(True)

        self.horizontalLayout_3.addWidget(self.pushButton_menu)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.groupBox_api = QGroupBox(self.centralwidget)
        self.groupBox_api.setObjectName(u"groupBox_api")
        self.groupBox_api.setFlat(True)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_api)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.label_api_logo = QLabel(self.groupBox_api)
        self.label_api_logo.setObjectName(u"label_api_logo")

        self.horizontalLayout_2.addWidget(self.label_api_logo)

        self.label_api_name = QLabel(self.groupBox_api)
        self.label_api_name.setObjectName(u"label_api_name")

        self.horizontalLayout_2.addWidget(self.label_api_name)

        self.pushButton_api_change = QPushButton(self.groupBox_api)
        self.pushButton_api_change.setObjectName(u"pushButton_api_change")
        icon3 = QIcon()
        iconThemeName = u"exchange-positions"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_api_change.setIcon(icon3)
        self.pushButton_api_change.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton_api_change)

        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.pushButton_api_settings_visibility = QPushButton(self.groupBox_api)
        self.pushButton_api_settings_visibility.setObjectName(u"pushButton_api_settings_visibility")
        icon4 = QIcon()
        iconThemeName = u"arrow-right"
        if QIcon.hasThemeIcon(iconThemeName):
            icon4 = QIcon.fromTheme(iconThemeName)
        else:
            icon4.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_api_settings_visibility.setIcon(icon4)
        self.pushButton_api_settings_visibility.setCheckable(True)
        self.pushButton_api_settings_visibility.setFlat(True)

        self.verticalLayout_3.addWidget(self.pushButton_api_settings_visibility)

        self.scrollArea = QScrollArea(self.groupBox_api)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 436, 83))
        self.verticalLayout_8 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.stackedWidget_api_overview = QStackedWidget(self.scrollAreaWidgetContents)
        self.stackedWidget_api_overview.setObjectName(u"stackedWidget_api_overview")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_9 = QVBoxLayout(self.page)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.stackedWidget_api_overview.addWidget(self.page)

        self.verticalLayout_8.addWidget(self.stackedWidget_api_overview)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)


        self.verticalLayout.addWidget(self.groupBox_api)

        self.groupBox_language = QGroupBox(self.centralwidget)
        self.groupBox_language.setObjectName(u"groupBox_language")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_language.sizePolicy().hasHeightForWidth())
        self.groupBox_language.setSizePolicy(sizePolicy)
        self.groupBox_language.setFlat(True)
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_language)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.groupBox_language)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.comboBox_lang_from = CComboBox(self.groupBox_language)
        self.comboBox_lang_from.setObjectName(u"comboBox_lang_from")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
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
        self.groupBox_files.setFlat(True)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_files)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.checkBox_use_glossary = QCheckBox(self.groupBox_files)
        self.checkBox_use_glossary.setObjectName(u"checkBox_use_glossary")
        self.checkBox_use_glossary.setChecked(True)

        self.horizontalLayout_8.addWidget(self.checkBox_use_glossary)

        self.label_glossary_info = CTooltipLabel(self.groupBox_files)
        self.label_glossary_info.setObjectName(u"label_glossary_info")
        self.label_glossary_info.setToolTipDuration(-1)
        self.label_glossary_info.setText(u"<helper>")

        self.horizontalLayout_8.addWidget(self.label_glossary_info)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_glossary_file = QLineEdit(self.groupBox_files)
        self.lineEdit_glossary_file.setObjectName(u"lineEdit_glossary_file")
        self.lineEdit_glossary_file.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.lineEdit_glossary_file)

        self.pushButton_glossary_file_browse = QPushButton(self.groupBox_files)
        self.pushButton_glossary_file_browse.setObjectName(u"pushButton_glossary_file_browse")
        icon5 = QIcon()
        iconThemeName = u"document-open"
        if QIcon.hasThemeIcon(iconThemeName):
            icon5 = QIcon.fromTheme(iconThemeName)
        else:
            icon5.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_glossary_file_browse.setIcon(icon5)
        self.pushButton_glossary_file_browse.setFlat(True)

        self.horizontalLayout.addWidget(self.pushButton_glossary_file_browse)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label = QLabel(self.groupBox_files)
        self.label.setObjectName(u"label")

        self.horizontalLayout_10.addWidget(self.label)

        self.label_outdir_help = CTooltipLabel(self.groupBox_files)
        self.label_outdir_help.setObjectName(u"label_outdir_help")
        self.label_outdir_help.setToolTipDuration(-1)
        self.label_outdir_help.setText(u"<helper>")

        self.horizontalLayout_10.addWidget(self.label_outdir_help)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lineEdit_out_dir = QLineEdit(self.groupBox_files)
        self.lineEdit_out_dir.setObjectName(u"lineEdit_out_dir")
        self.lineEdit_out_dir.setClearButtonEnabled(True)

        self.horizontalLayout_4.addWidget(self.lineEdit_out_dir)

        self.pushButton_out_dir_browse = QPushButton(self.groupBox_files)
        self.pushButton_out_dir_browse.setObjectName(u"pushButton_out_dir_browse")
        icon6 = QIcon()
        iconThemeName = u"document-open-folder"
        if QIcon.hasThemeIcon(iconThemeName):
            icon6 = QIcon.fromTheme(iconThemeName)
        else:
            icon6.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_out_dir_browse.setIcon(icon6)
        self.pushButton_out_dir_browse.setFlat(True)

        self.horizontalLayout_4.addWidget(self.pushButton_out_dir_browse)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addWidget(self.groupBox_files)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.checkBox_auto_start = QCheckBox(self.centralwidget)
        self.checkBox_auto_start.setObjectName(u"checkBox_auto_start")
        self.checkBox_auto_start.setChecked(True)

        self.horizontalLayout_15.addWidget(self.checkBox_auto_start)

        self.spinBox_auto_start = QSpinBox(self.centralwidget)
        self.spinBox_auto_start.setObjectName(u"spinBox_auto_start")
        self.spinBox_auto_start.setMinimum(1)
        self.spinBox_auto_start.setMaximum(10000)

        self.horizontalLayout_15.addWidget(self.spinBox_auto_start)


        self.verticalLayout.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButton_start = QPushButton(self.centralwidget)
        self.pushButton_start.setObjectName(u"pushButton_start")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.pushButton_start.setFont(font1)
        icon7 = QIcon()
        iconThemeName = u"media-playback-start"
        if QIcon.hasThemeIcon(iconThemeName):
            icon7 = QIcon.fromTheme(iconThemeName)
        else:
            icon7.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_start.setIcon(icon7)

        self.horizontalLayout_9.addWidget(self.pushButton_start)

        self.pushButton_abort = QPushButton(self.centralwidget)
        self.pushButton_abort.setObjectName(u"pushButton_abort")
        self.pushButton_abort.setFont(font1)
        icon8 = QIcon()
        iconThemeName = u"process-stop"
        if QIcon.hasThemeIcon(iconThemeName):
            icon8 = QIcon.fromTheme(iconThemeName)
        else:
            icon8.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_abort.setIcon(icon8)

        self.horizontalLayout_9.addWidget(self.pushButton_abort)


        self.verticalLayout.addLayout(self.horizontalLayout_9)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_files = QWidget()
        self.page_files.setObjectName(u"page_files")
        self.verticalLayout_6 = QVBoxLayout(self.page_files)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.file_table = FileTable(self.page_files)
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

        self.verticalLayout_6.addWidget(self.file_table)

        self.stackedWidget.addWidget(self.page_files)
        self.page_greeter = QWidget()
        self.page_greeter.setObjectName(u"page_greeter")
        self.verticalLayout_5 = QVBoxLayout(self.page_greeter)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_greeter = CDropFrame(self.page_greeter)
        self.frame_greeter.setObjectName(u"frame_greeter")
        self.frame_greeter.setFrameShape(QFrame.StyledPanel)
        self.frame_greeter.setFrameShadow(QFrame.Raised)
        self.frame_greeter.setLineWidth(4)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_greeter)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(30)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_5)

        self.label_drop_2 = QLabel(self.frame_greeter)
        self.label_drop_2.setObjectName(u"label_drop_2")
        self.label_drop_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_11.addWidget(self.label_drop_2)

        self.label_drop_icon = QLabel(self.frame_greeter)
        self.label_drop_icon.setObjectName(u"label_drop_icon")
        self.label_drop_icon.setText(u"<drop icon>")
        self.label_drop_icon.setAlignment(Qt.AlignCenter)

        self.verticalLayout_11.addWidget(self.label_drop_icon)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_6)


        self.horizontalLayout_11.addLayout(self.verticalLayout_11)


        self.verticalLayout_5.addWidget(self.frame_greeter)

        self.stackedWidget.addWidget(self.page_greeter)
        self.page_interactive_reliable = QWidget()
        self.page_interactive_reliable.setObjectName(u"page_interactive_reliable")
        self.gridLayout_2 = QGridLayout(self.page_interactive_reliable)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_7, 2, 1, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_4 = QLabel(self.page_interactive_reliable)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_13.addWidget(self.label_4)

        self.comboBox_lang_from_interactive = CComboBox(self.page_interactive_reliable)
        self.comboBox_lang_from_interactive.setObjectName(u"comboBox_lang_from_interactive")
        sizePolicy1.setHeightForWidth(self.comboBox_lang_from_interactive.sizePolicy().hasHeightForWidth())
        self.comboBox_lang_from_interactive.setSizePolicy(sizePolicy1)
        self.comboBox_lang_from_interactive.setFrame(False)

        self.horizontalLayout_13.addWidget(self.comboBox_lang_from_interactive)


        self.verticalLayout_2.addLayout(self.horizontalLayout_13)

        self.plainTextEdit_from_interactive = QPlainTextEdit(self.page_interactive_reliable)
        self.plainTextEdit_from_interactive.setObjectName(u"plainTextEdit_from_interactive")

        self.verticalLayout_2.addWidget(self.plainTextEdit_from_interactive)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 1, 1, 1)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_5 = QLabel(self.page_interactive_reliable)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_14.addWidget(self.label_5)

        self.comboBox_lang_to_interactive = CComboBox(self.page_interactive_reliable)
        self.comboBox_lang_to_interactive.setObjectName(u"comboBox_lang_to_interactive")
        sizePolicy1.setHeightForWidth(self.comboBox_lang_to_interactive.sizePolicy().hasHeightForWidth())
        self.comboBox_lang_to_interactive.setSizePolicy(sizePolicy1)
        self.comboBox_lang_to_interactive.setFrame(False)

        self.horizontalLayout_14.addWidget(self.comboBox_lang_to_interactive)


        self.verticalLayout_7.addLayout(self.horizontalLayout_14)

        self.plainTextEdit_to_interactive = QPlainTextEdit(self.page_interactive_reliable)
        self.plainTextEdit_to_interactive.setObjectName(u"plainTextEdit_to_interactive")

        self.verticalLayout_7.addWidget(self.plainTextEdit_to_interactive)


        self.gridLayout_2.addLayout(self.verticalLayout_7, 1, 3, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 51, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 0, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(114, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_7, 1, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(24, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 1, 0, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(112, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_6, 1, 4, 1, 1)

        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(1, 10)
        self.gridLayout_2.setRowStretch(2, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 10)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.gridLayout_2.setColumnStretch(3, 10)
        self.gridLayout_2.setColumnStretch(4, 1)
        self.stackedWidget.addWidget(self.page_interactive_reliable)

        self.gridLayout.addWidget(self.stackedWidget, 0, 1, 1, 1)

        self.label_progress = QLabel(self.centralwidget)
        self.label_progress.setObjectName(u"label_progress")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_progress.sizePolicy().hasHeightForWidth())
        self.label_progress.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label_progress, 1, 0, 1, 1)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.gridLayout.addWidget(self.progressBar, 1, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.pushButton_translate_files.setDefault(True)
        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"placeholder", None))
        self.pushButton_translate_files.setText(QCoreApplication.translate("MainWindow", u"Translate Files", None))
        self.pushButton_translate_text.setText(QCoreApplication.translate("MainWindow", u"Translate Text", None))
        self.pushButton_menu.setText("")
        self.groupBox_api.setTitle(QCoreApplication.translate("MainWindow", u"API", None))
        self.label_api_logo.setText(QCoreApplication.translate("MainWindow", u"<logo>", None))
        self.label_api_name.setText(QCoreApplication.translate("MainWindow", u"<current api>", None))
        self.pushButton_api_change.setText(QCoreApplication.translate("MainWindow", u"Change", None))
        self.pushButton_api_settings_visibility.setText(QCoreApplication.translate("MainWindow", u"API Settings", None))
        self.groupBox_language.setTitle(QCoreApplication.translate("MainWindow", u"Language", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"From:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"To:", None))
        self.groupBox_files.setTitle(QCoreApplication.translate("MainWindow", u"Translation Settings", None))
        self.checkBox_use_glossary.setText(QCoreApplication.translate("MainWindow", u"Use glossary:", None))
#if QT_CONFIG(tooltip)
        self.label_glossary_info.setToolTip(QCoreApplication.translate("MainWindow", u"<html>\n"
"                    <head/>\n"
"                    <body>\n"
"                        <p> DeepQt uses glossary files to pre-process files before sending them to the API; \n"
"                            this is not the same as DeepL's glossary functions. Therefore, they can be used\n"
"                            with any language and offer special features, which DeepL's glossaries cannot\n"
"                            offer.\n"
"                        </p>\n"
"                        <p>\n"
"                           The format of these glossaries is outlined in the \n"
"                            <a href=\"https://github.com/VoxelCubes/DeepQt/blob/master/docs/glossary_help.md\">\n"
"                                online documentation\n"
"                            </a>\n"
"                            .\n"
"                        </p>\n"
"                    </body>\n"
"                </html>", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_glossary_file.setPlaceholderText(QCoreApplication.translate("MainWindow", u"No glossary selected", None))
#if QT_CONFIG(tooltip)
        self.pushButton_glossary_file_browse.setToolTip(QCoreApplication.translate("MainWindow", u"Browse", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_glossary_file_browse.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Output directory:", None))
#if QT_CONFIG(tooltip)
        self.label_outdir_help.setToolTip(QCoreApplication.translate("MainWindow", u"You can use a relative path to place translations inside a subfolder of the file's original location, or specify an absolute path to place all outputs into the same place.\n"
"\n"
"Leave it blank to have them placed next to the original files.", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_out_dir.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Same as original file", None))
#if QT_CONFIG(tooltip)
        self.pushButton_out_dir_browse.setToolTip(QCoreApplication.translate("MainWindow", u"Browse", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_out_dir_browse.setText("")
        self.checkBox_auto_start.setText(QCoreApplication.translate("MainWindow", u"Automatically translate after", None))
        self.spinBox_auto_start.setSuffix(QCoreApplication.translate("MainWindow", u" seconds", None))
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
        self.label_drop_2.setText(QCoreApplication.translate("MainWindow", u"Drag and Drop Files or Folders Here", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Translate from", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Translate into", None))
        self.label_progress.setText(QCoreApplication.translate("MainWindow", u"<progress>", None))
    # retranslateUi

