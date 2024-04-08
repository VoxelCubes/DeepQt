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
    QSizePolicy, QWidget)

class Ui_ChangeBackend(object):
    def setupUi(self, ChangeBackend):
        if not ChangeBackend.objectName():
            ChangeBackend.setObjectName(u"ChangeBackend")
        ChangeBackend.resize(777, 430)
        self.buttonBox = QDialogButtonBox(ChangeBackend)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(400, 380, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.retranslateUi(ChangeBackend)
        self.buttonBox.accepted.connect(ChangeBackend.accept)
        self.buttonBox.rejected.connect(ChangeBackend.reject)

        QMetaObject.connectSlotsByName(ChangeBackend)
    # setupUi

    def retranslateUi(self, ChangeBackend):
        ChangeBackend.setWindowTitle(QCoreApplication.translate("ChangeBackend", u"Translation Services", None))
    # retranslateUi

