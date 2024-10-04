# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'api_status_usage.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_APIStatusUsage(object):
    def setupUi(self, APIStatusUsage):
        if not APIStatusUsage.objectName():
            APIStatusUsage.setObjectName(u"APIStatusUsage")
        APIStatusUsage.resize(646, 92)
        self.formLayout = QFormLayout(APIStatusUsage)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(6)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(APIStatusUsage)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_status_good_icon = QLabel(APIStatusUsage)
        self.label_status_good_icon.setObjectName(u"label_status_good_icon")

        self.horizontalLayout_2.addWidget(self.label_status_good_icon)

        self.label_status_good = QLabel(APIStatusUsage)
        self.label_status_good.setObjectName(u"label_status_good")

        self.horizontalLayout_2.addWidget(self.label_status_good)

        self.label_status_bad_icon = QLabel(APIStatusUsage)
        self.label_status_bad_icon.setObjectName(u"label_status_bad_icon")

        self.horizontalLayout_2.addWidget(self.label_status_bad_icon)

        self.label_status_bad = QLabel(APIStatusUsage)
        self.label_status_bad.setObjectName(u"label_status_bad")

        self.horizontalLayout_2.addWidget(self.label_status_bad)

        self.label_status_offline_icon = QLabel(APIStatusUsage)
        self.label_status_offline_icon.setObjectName(u"label_status_offline_icon")

        self.horizontalLayout_2.addWidget(self.label_status_offline_icon)

        self.label_status_offline = QLabel(APIStatusUsage)
        self.label_status_offline.setObjectName(u"label_status_offline")

        self.horizontalLayout_2.addWidget(self.label_status_offline)

        self.horizontalSpacer_2 = QSpacerItem(0, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButton_refresh = QPushButton(APIStatusUsage)
        self.pushButton_refresh.setObjectName(u"pushButton_refresh")
        self.pushButton_refresh.setText(u"")
        icon = QIcon()
        iconThemeName = u"view-refresh"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Mode.Normal, QIcon.State.Off)

        self.pushButton_refresh.setIcon(icon)
        self.pushButton_refresh.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton_refresh)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_usage_label = QLabel(APIStatusUsage)
        self.label_usage_label.setObjectName(u"label_usage_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_usage_label)

        self.widget_usage_field = QWidget(APIStatusUsage)
        self.widget_usage_field.setObjectName(u"widget_usage_field")
        self.horizontalLayout = QHBoxLayout(self.widget_usage_field)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_usage_error_icon = QLabel(self.widget_usage_field)
        self.label_usage_error_icon.setObjectName(u"label_usage_error_icon")

        self.horizontalLayout.addWidget(self.label_usage_error_icon)

        self.label_usage_warn_icon = QLabel(self.widget_usage_field)
        self.label_usage_warn_icon.setObjectName(u"label_usage_warn_icon")

        self.horizontalLayout.addWidget(self.label_usage_warn_icon)

        self.label_usage = QLabel(self.widget_usage_field)
        self.label_usage.setObjectName(u"label_usage")

        self.horizontalLayout.addWidget(self.label_usage)

        self.horizontalSpacer_usage = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_usage)


        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.widget_usage_field)


        self.retranslateUi(APIStatusUsage)

        QMetaObject.connectSlotsByName(APIStatusUsage)
    # setupUi

    def retranslateUi(self, APIStatusUsage):
        APIStatusUsage.setWindowTitle(QCoreApplication.translate("APIStatusUsage", u"Form", None))
        self.label_5.setText(QCoreApplication.translate("APIStatusUsage", u"Status:", None))
        self.label_status_good_icon.setText(QCoreApplication.translate("APIStatusUsage", u"<okay_icon>", None))
        self.label_status_good.setText(QCoreApplication.translate("APIStatusUsage", u"Okay", None))
        self.label_status_bad_icon.setText(QCoreApplication.translate("APIStatusUsage", u"<error_icon>", None))
        self.label_status_bad.setText(QCoreApplication.translate("APIStatusUsage", u"Error", None))
        self.label_status_offline_icon.setText(QCoreApplication.translate("APIStatusUsage", u"<offline_icon>", None))
        self.label_status_offline.setText(QCoreApplication.translate("APIStatusUsage", u"Not Connected", None))
#if QT_CONFIG(tooltip)
        self.pushButton_refresh.setToolTip(QCoreApplication.translate("APIStatusUsage", u"Refresh", None))
#endif // QT_CONFIG(tooltip)
        self.label_usage_label.setText(QCoreApplication.translate("APIStatusUsage", u"Usage:", None))
        self.label_usage_error_icon.setText(QCoreApplication.translate("APIStatusUsage", u"<error_icon>", None))
        self.label_usage_warn_icon.setText(QCoreApplication.translate("APIStatusUsage", u"<warn_icon>", None))
        self.label_usage.setText(QCoreApplication.translate("APIStatusUsage", u"<usage_placeholder>", None))
    # retranslateUi

