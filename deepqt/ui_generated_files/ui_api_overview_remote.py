# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'api_overview_remote.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_api_overview_deepl(object):
    def setupUi(self, api_overview_deepl):
        if not api_overview_deepl.objectName():
            api_overview_deepl.setObjectName(u"api_overview_deepl")
        api_overview_deepl.resize(405, 66)
        self.verticalLayout = QVBoxLayout(api_overview_deepl)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_5 = QLabel(api_overview_deepl)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_api_status_good_icon = QLabel(api_overview_deepl)
        self.label_api_status_good_icon.setObjectName(u"label_api_status_good_icon")

        self.horizontalLayout_2.addWidget(self.label_api_status_good_icon)

        self.label_api_status_good = QLabel(api_overview_deepl)
        self.label_api_status_good.setObjectName(u"label_api_status_good")

        self.horizontalLayout_2.addWidget(self.label_api_status_good)

        self.label_api_status_bad_icon = QLabel(api_overview_deepl)
        self.label_api_status_bad_icon.setObjectName(u"label_api_status_bad_icon")

        self.horizontalLayout_2.addWidget(self.label_api_status_bad_icon)

        self.label_api_status_bad = QLabel(api_overview_deepl)
        self.label_api_status_bad.setObjectName(u"label_api_status_bad")

        self.horizontalLayout_2.addWidget(self.label_api_status_bad)

        self.horizontalSpacer_2 = QSpacerItem(0, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButton_refresh = QPushButton(api_overview_deepl)
        self.pushButton_refresh.setObjectName(u"pushButton_refresh")
        self.pushButton_refresh.setText(u"")
        icon = QIcon()
        iconThemeName = u"view-refresh"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButton_refresh.setIcon(icon)
        self.pushButton_refresh.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton_refresh)


        self.formLayout_2.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_6 = QLabel(api_overview_deepl)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_6)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_api_usage_error_icon = QLabel(api_overview_deepl)
        self.label_api_usage_error_icon.setObjectName(u"label_api_usage_error_icon")

        self.horizontalLayout_10.addWidget(self.label_api_usage_error_icon)

        self.label_api_usage_warn_icon = QLabel(api_overview_deepl)
        self.label_api_usage_warn_icon.setObjectName(u"label_api_usage_warn_icon")

        self.horizontalLayout_10.addWidget(self.label_api_usage_warn_icon)

        self.label_api_usage = QLabel(api_overview_deepl)
        self.label_api_usage.setObjectName(u"label_api_usage")

        self.horizontalLayout_10.addWidget(self.label_api_usage)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_3)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_10)


        self.verticalLayout.addLayout(self.formLayout_2)


        self.retranslateUi(api_overview_deepl)

        QMetaObject.connectSlotsByName(api_overview_deepl)
    # setupUi

    def retranslateUi(self, api_overview_deepl):
        api_overview_deepl.setWindowTitle(QCoreApplication.translate("api_overview_deepl", u"Form", None))
        self.label_5.setText(QCoreApplication.translate("api_overview_deepl", u"Status:", None))
        self.label_api_status_good_icon.setText(QCoreApplication.translate("api_overview_deepl", u"<okay_icon>", None))
        self.label_api_status_good.setText(QCoreApplication.translate("api_overview_deepl", u"Okay", None))
        self.label_api_status_bad_icon.setText(QCoreApplication.translate("api_overview_deepl", u"<error_icon>", None))
        self.label_api_status_bad.setText(QCoreApplication.translate("api_overview_deepl", u"Error", None))
#if QT_CONFIG(tooltip)
        self.pushButton_refresh.setToolTip(QCoreApplication.translate("api_overview_deepl", u"Refresh", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("api_overview_deepl", u"Usage:", None))
        self.label_api_usage_error_icon.setText(QCoreApplication.translate("api_overview_deepl", u"<error_icon>", None))
        self.label_api_usage_warn_icon.setText(QCoreApplication.translate("api_overview_deepl", u"<warn_icon>", None))
        self.label_api_usage.setText(QCoreApplication.translate("api_overview_deepl", u"<usage_placeholder>", None))
    # retranslateUi

