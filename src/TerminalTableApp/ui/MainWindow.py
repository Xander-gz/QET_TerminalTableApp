# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTabWidget, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(487, 626)
        icon = QIcon()
        icon.addFile(u"../icon.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
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
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
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

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")

        self.verticalLayout.addWidget(self.widget_2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")

        self.verticalLayout.addWidget(self.widget)

        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(0, 50))
        self.horizontalLayoutWidget = QWidget(self.widget_3)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(-1, 0, 381, 42))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.fileChooseButton = QPushButton(self.horizontalLayoutWidget)
        self.fileChooseButton.setObjectName(u"fileChooseButton")
        self.fileChooseButton.setEnabled(True)
        self.fileChooseButton.setMinimumSize(QSize(150, 40))
        self.fileChooseButton.setMaximumSize(QSize(40, 150))
        self.fileChooseButton.setFlat(False)

        self.horizontalLayout_4.addWidget(self.fileChooseButton)


        self.verticalLayout.addWidget(self.widget_3)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 20))
        self.label_2.setMaximumSize(QSize(16777215, 20))
        self.label_2.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.label_2)

        self.choosenFileLineEdit = QLineEdit(self.centralwidget)
        self.choosenFileLineEdit.setObjectName(u"choosenFileLineEdit")

        self.verticalLayout.addWidget(self.choosenFileLineEdit)

        self.widget_4 = QWidget(self.centralwidget)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setMinimumSize(QSize(0, 50))
        self.createButton = QPushButton(self.widget_4)
        self.createButton.setObjectName(u"createButton")
        self.createButton.setGeometry(QRect(10, 0, 155, 40))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.createButton.sizePolicy().hasHeightForWidth())
        self.createButton.setSizePolicy(sizePolicy1)
        self.createButton.setMinimumSize(QSize(0, 40))
        self.layoutWidget = QWidget(self.widget_4)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(190, 0, 281, 54))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.checkbox_protection_notice = QCheckBox(self.layoutWidget)
        self.checkbox_protection_notice.setObjectName(u"checkbox_protection_notice")
        self.checkbox_protection_notice.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkbox_protection_notice)

        self.checkBox_accesoiries = QCheckBox(self.layoutWidget)
        self.checkBox_accesoiries.setObjectName(u"checkBox_accesoiries")
        self.checkBox_accesoiries.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_accesoiries)


        self.verticalLayout.addWidget(self.widget_4)

        self.feedbackTextEdit = QTextEdit(self.centralwidget)
        self.feedbackTextEdit.setObjectName(u"feedbackTextEdit")
        self.feedbackTextEdit.setAcceptDrops(False)
        self.feedbackTextEdit.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.feedbackTextEdit)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy2)
        self.pushButton.setMinimumSize(QSize(200, 0))
        self.pushButton.setMaximumSize(QSize(100, 20))
        self.pushButton.setSizeIncrement(QSize(0, 0))

        self.verticalLayout.addWidget(self.pushButton)


        self.horizontalLayout.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 487, 22))
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
        self.checkbox_protection_notice.setText(QCoreApplication.translate("MainWindow", u"insert protection notice", None))
        self.checkBox_accesoiries.setText(QCoreApplication.translate("MainWindow", u"Add accessories", None))
        self.feedbackTextEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">feedback comments:</p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"clear feedback", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"help", None))
    # retranslateUi

