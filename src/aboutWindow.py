# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'About.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QLayout, QPlainTextEdit,
    QScrollArea, QSizePolicy, QVBoxLayout, QWidget)

class Ui_aboutWindow(object):
    def setupUi(self, aboutWindow):
        if not aboutWindow.objectName():
            aboutWindow.setObjectName(u"aboutWindow")
        aboutWindow.resize(430, 330)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(aboutWindow.sizePolicy().hasHeightForWidth())
        aboutWindow.setSizePolicy(sizePolicy)
        aboutWindow.setWindowOpacity(1.000000000000000)
        self.verticalLayoutWidget = QWidget(aboutWindow)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 441, 341))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.scrollArea = QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 429, 329))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy1)
        self.plainTextEdit = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(0, 0, 421, 321))
        self.plainTextEdit.setAcceptDrops(False)
        self.plainTextEdit.setLocale(QLocale(QLocale.German, QLocale.Germany))
        self.plainTextEdit.setInputMethodHints(Qt.ImhNone)
        self.plainTextEdit.setUndoRedoEnabled(False)
        self.plainTextEdit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(aboutWindow)

        QMetaObject.connectSlotsByName(aboutWindow)
    # setupUi

    def retranslateUi(self, aboutWindow):
        aboutWindow.setWindowTitle(QCoreApplication.translate("aboutWindow", u"about KlemmenplanApp", None))
        self.plainTextEdit.setPlainText(QCoreApplication.translate("aboutWindow", u"Terminal Diagram App\n"
"Version 0.3.4\n"
"\n"
"The app reads a Qelectrotech file, creates a terminal diagram table, appends the table,\n"
"and saves the file under a new name.\n"
"\n"
"Project Name is free open-source software, published under\n"
"the GNU General Public Licence Version 3 (GPL-3.0).\n"
"\n"
"This licence permits the use, examination, modification and\n"
"redistribution of the source code, provided that\n"
"derivative works are also licensed under GPL v3.\n"
"\n"
"The full licence text can be found in the LICENCE file.\n"
"\n"
"Copyright \u00a9 2026 xanderhopp", None))
    # retranslateUi

