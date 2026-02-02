# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(381, 626)
        MainWindow.setIconSize(QSize(32, 32))
        MainWindow.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        MainWindow.setAnimated(False)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(False)
        self.action_anleitung = QAction(MainWindow)
        self.action_anleitung.setObjectName(u"action_anleitung")
        self.action_anleitung.setCheckable(False)
        self.action_ueber = QAction(MainWindow)
        self.action_ueber.setObjectName(u"action_ueber")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.Infotext = QLabel(self.centralwidget)
        self.Infotext.setObjectName(u"Infotext")
        font = QFont()
        font.setFamilies([u"Liberation Sans"])
        font.setPointSize(10)
        self.Infotext.setFont(font)
        self.Infotext.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout.addWidget(self.Infotext)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.fileChooseButton = QPushButton(self.centralwidget)
        self.fileChooseButton.setObjectName(u"fileChooseButton")
        self.fileChooseButton.setFlat(False)

        self.verticalLayout.addWidget(self.fileChooseButton, 0, Qt.AlignHCenter)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 20))
        self.label_2.setMaximumSize(QSize(16777215, 20))
        self.label_2.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.label_2)

        self.choosenFileLineEdit = QLineEdit(self.centralwidget)
        self.choosenFileLineEdit.setObjectName(u"choosenFileLineEdit")

        self.verticalLayout.addWidget(self.choosenFileLineEdit)

        self.createButton = QPushButton(self.centralwidget)
        self.createButton.setObjectName(u"createButton")

        self.verticalLayout.addWidget(self.createButton, 0, Qt.AlignHCenter)

        self.feedbackTextEdit = QTextEdit(self.centralwidget)
        self.feedbackTextEdit.setObjectName(u"feedbackTextEdit")
        self.feedbackTextEdit.setAcceptDrops(False)
        self.feedbackTextEdit.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.feedbackTextEdit)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QSize(200, 0))
        self.pushButton.setMaximumSize(QSize(100, 20))
        self.pushButton.setSizeIncrement(QSize(0, 0))

        self.verticalLayout.addWidget(self.pushButton)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 381, 22))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.addAction(self.action_anleitung)
        self.menuHelp.addAction(self.action_ueber)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.feedbackTextEdit.clear)

        self.fileChooseButton.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Terminalblock tables for Qelectrotech", None))
        self.action_anleitung.setText(QCoreApplication.translate("MainWindow", u"Instruction", None))
        self.action_ueber.setText(QCoreApplication.translate("MainWindow", u"about", None))
#if QT_CONFIG(tooltip)
        self.action_ueber.setToolTip(QCoreApplication.translate("MainWindow", u"\u00dcber", None))
#endif // QT_CONFIG(tooltip)
        self.Infotext.setText(QCoreApplication.translate("MainWindow", u"With \"Terminalblock tables for Qelectrotech\"\n"
"the individual terminal elements marked with \"-X??:??\"\n"
"are sorted, assigned to the respective\n"
"terminal strips, and written to a table.\n"
"The tables are added to the project as new pages\n"
"and saved under the name\n"
"Original-file-name_terminals.qet\n"
"in the same folder as the original file. \n"
"\n"
"The original file remains unchanged.", None))
        self.fileChooseButton.setText(QCoreApplication.translate("MainWindow", u"choose\n"
"file", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"chosen file:", None))
        self.createButton.setText(QCoreApplication.translate("MainWindow", u"create terminalblock table", None))
        self.feedbackTextEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">feedback comments:</p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"clear feedback", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"help", None))
    # retranslateUi

