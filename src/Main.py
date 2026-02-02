#!/usr/bin/env python

"""
Copyright (C) 2026 xanderhopp; xanderhopp@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""


from PySide6.QtCore import QLocale
import gettext
import os
import sys

APP_NAME = "TerminalTableApp"


def get_locale_dir():
    if "APPDIR" in os.environ:  # AppImage
        return os.path.join(os.environ["APPDIR"], "usr", "share", "locale")

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "locale")

    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "locale"
    )


locale_dir = get_locale_dir()

qt_locale = QLocale.system()
ui_langs = qt_locale.uiLanguages()

primary = ui_langs[0] if ui_langs else qt_locale.name()

languages = [
    primary.replace("-", "_"),
    primary.split("-")[0],
]

try:
    translation = gettext.translation(
        APP_NAME,
        localedir=locale_dir,
        languages=languages
    )
    translation.install()
except FileNotFoundError:
    gettext.install(APP_NAME)



from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QFileDialog,
    QDialog
    )


from MainWindow import Ui_MainWindow
from HelpWindow import Ui_HelpWindow
from aboutWindow import Ui_aboutWindow

import main_funktions

class HelpWindow(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_HelpWindow()
        self.ui.setupUi(self)
        self.ui.plainTextEdit.setPlainText(_("Instruction:\nAttention!\nThe programme does not recognise formulas for assigning\nslide numbers (e.g. %id/%total) or equipment codes!\nThese must be entered separately!\n\nThe equipment code for the terminal strip must begin with\n‘-X’.\n\nAny characters can be specified after this.\nThe terminal designation is delimited with a\n‘:’.\nHere, too, both letters and numbers can follow.\nThe terminals are sorted in ascending order, with numbers\nbefore letters.\nExamples:\n‘-XPR:1’, ‘-X312:21’\n\nThe pages are added to the project with the title Terminal diagram + slide name\n. Slide name K1, K2,...\nIn terms of function, the terminal diagrams are individual elements\nthat are also displayed in the component collection under \nImported elements/Terminal diagrams.\nIn addition, accessories are created here under /Accessories,\nwhich can be subsequently placed over the terminal diagram.\n\nThe following requirements must be met for the terminals drawn in the project\n:\n- The terminals for terminal points\n  must be given a name (a, b...)\n- The terminals for terminal points\n  must be declared as internal or external.\n- Bridges must be declared as generic.\n  and have no name.\n\nA bridge is recognised as such if the conductor in the text field is declared as ‘bridge e1’.\n  ‘e1’ stands for external 1, ‘i1’ for internal 1.\nThe following bridges can be specified: e1, e2, e3, and i3, i2, i1.\n\n\nBe careful when drawing terminal elements yourself.\nIf the elements are copied or saved under a new name,\nthe ‘uuid’ of the terminals will not be reassigned. This can\nlead to unexpected behaviour. Therefore, always delete the terminals\nand insert them again.\nThe same applies to other elements.\n\nCables are queried from the XML file. However, they cannot\ncurrently be specified in Qelectrotech.\n\nIt is possible to add further elements, such as an image of the\nterminals used or comments."))


class aboutWindow(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_aboutWindow()
        self.ui.setupUi(self)
        self.ui.plainTextEdit.setPlainText(_("TerminalTableApp") + "\nVersion 1.0.0\n\n" + _("The app reads a Qelectrotech file, creates a terminal diagram table, appends the table,\nand saves the file under a new name.\n\nProject Name is free open-source software, published under\nthe GNU General Public Licence Version 3 (GPL-3.0).\n\nThis licence permits the use, examination, modification and\nredistribution of the source code, provided that\nderivative works are also licensed under GPL v3.\n\nThe full licence text can be found in the LICENCE file.\n\nCopyright © 2026 xanderhopp"))


class MainWindow(QMainWindow, QFileDialog, QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.originFile = None
        self.setIcon()
        # overwrite the UI-file for translation
        self.setWindowTitle(_("Terminalblock tables for Qelectrotech"))
        self.ui.menuHelp.setTitle(_("help"))
        self.ui.action_anleitung.setText(_("Instruction"))
        self.ui.action_ueber.setText(_("about"))
        self.ui.Infotext.setText(_("With \"Terminalblock tables for Qelectrotech\"\nthe individual terminal elements marked with \"-X??:??\"\nare sorted, assigned to the respective\nterminal strips, and written to a table.\nThe tables are added to the project as new pages\nand saved under the name\nOriginal-file-name_terminals.qet\nin the same folder as the original file. \n\nThe original file remains unchanged."))
        self.ui.fileChooseButton.setText(_("choose\nfile"))
        self.ui.label_2.setText(_("chosen file:"))
        self.ui.choosenFileLineEdit.setText(_("nothing selected"))
        self.ui.createButton.setText(_("create terminlalblock table"))
        self.ui.pushButton.setText(_("clear feedback"))
        self.ui.feedbackTextEdit.setPlainText(_("feedback comments:"))


        # Slots
        self.ui.fileChooseButton.clicked.connect(self.chooseFile)
        self.ui.createButton.clicked.connect(self.createFile)
        
        # Events
        self.ui.action_anleitung.triggered.connect(self.openHelpWindow)
        self.ui.action_ueber.triggered.connect(self.openaboutWindow)

    # def trans(self, lang, text):
    #     trans = gettext.translation("TerminalTableApp", locale, lang)
    #     trans.install()
    #     return
    
    def setIcon(self):
        appIcon = QIcon('icon.svg')
        self.setWindowIcon(appIcon)
        
    def give_feedback(self, feedback):
         print(feedback)
         self.ui.feedbackTextEdit.append(feedback)
        
        # choose a File
    def chooseFile(self):
            fileName, _ = QFileDialog.getOpenFileName(self, "qet-Datei öffnen", "","QET Files (*.qet);;All Files (*)")
            if fileName:
                print(fileName)
                originFile = fileName
                self.ui.choosenFileLineEdit.setText(fileName)
            
        # start the Main funktions and get the feedback to the textEdit
    def createFile(self):
        main_funktions.work_out_the_terminal_diagram(self.ui.choosenFileLineEdit.text(), self.give_feedback)

    def openHelpWindow(self):
        self.hw = HelpWindow()
        self.hw.show()

    def openaboutWindow(self):
        self.aw = aboutWindow()
        self.aw.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    Window = MainWindow()
    Window.show()
    sys.exit(app.exec())