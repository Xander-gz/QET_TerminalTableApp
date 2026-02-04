# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Help.ui'
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

class Ui_HelpWindow(object):
    def setupUi(self, HelpWindow):
        if not HelpWindow.objectName():
            HelpWindow.setObjectName(u"HelpWindow")
        HelpWindow.resize(430, 330)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HelpWindow.sizePolicy().hasHeightForWidth())
        HelpWindow.setSizePolicy(sizePolicy)
        HelpWindow.setWindowOpacity(1.000000000000000)
        self.verticalLayoutWidget = QWidget(HelpWindow)
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


        self.retranslateUi(HelpWindow)

        QMetaObject.connectSlotsByName(HelpWindow)
    # setupUi

    def retranslateUi(self, HelpWindow):
        HelpWindow.setWindowTitle(QCoreApplication.translate("HelpWindow", u"Hilfe", None))
        self.plainTextEdit.setPlainText(QCoreApplication.translate("HelpWindow", u"Help:\n"
"Attention!\n"
"The programme does not recognise formulas for assigning\n"
"slide numbers (e.g. %id/%total) or equipment codes!\n"
"These must be entered separately!\n"
"\n"
"The equipment code for the terminal strip must begin with\n"
"\u2018-X\u2019.\n"
"\n"
"Any characters can be specified after this.\n"
"The terminal designation is delimited with a\n"
"\u2018:\u2019.\n"
"Here, too, both letters and numbers can follow.\n"
"The terminals are sorted in ascending order, with numbers\n"
"before letters.\n"
"Examples:\n"
"\u2018-XPR:1\u2019, \u2018-X312:21\u2019\n"
"\n"
"The pages are added to the project with the title Terminal diagram + slide name\n"
". Slide name K1, K2,...\n"
"In terms of function, the terminal diagrams are individual elements\n"
"that are also displayed in the component collection under \n"
"Imported elements/Terminal diagrams.\n"
"In addition, accessories are created here under /Accessories,\n"
"which can be subsequently placed over the terminal diagram.\n"
"\n"
"The following req"
                        "uirements must be met for the terminals drawn in the project\n"
":\n"
"- The terminals for terminal points\n"
"  must be given a name (a, b...)\n"
"- The terminals for terminal points\n"
"  must be declared as internal or external.\n"
"- Bridges must be declared as generic.\n"
"  and have no name.\n"
"\n"
"A bridge is recognised as such if the conductor in the text field is declared as \u2018bridge e1\u2019.\n"
"  \u2018e1\u2019 stands for external 1, \u2018i1\u2019 for internal 1.\n"
"The following bridges can be specified: e1, e2, e3, and i3, i2, i1.\n"
"\n"
"\n"
"Be careful when drawing terminal elements yourself.\n"
"If the elements are copied or saved under a new name,\n"
"the \u2018uuid\u2019 of the terminals will not be reassigned. This can\n"
"lead to unexpected behaviour. Therefore, always delete the terminals\n"
"and insert them again.\n"
"The same applies to other elements.\n"
"\n"
"Cables are queried from the XML file. However, they cannot\n"
"currently be specified in Qelectrotech.\n"
"\n"
"It is "
                        "possible to add further elements, such as an image of the\n"
"terminals used or comments.", None))
    # retranslateUi

