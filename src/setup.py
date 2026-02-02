
import os
import sys
import PySide6
from cx_Freeze import setup, Executable

# --------------------------------------------------
# Paths
# --------------------------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
pyside6_dir = os.path.dirname(PySide6.__file__)
qt_plugins = os.path.join(pyside6_dir, "Qt", "plugins")

# --------------------------------------------------
# Include files
# --------------------------------------------------
def add_plugin(name):
    path = os.path.join(qt_plugins, name)
    return (path, name) if os.path.isdir(path) else None

include_files = [
    add_plugin("platforms"),
    add_plugin("imageformats"),
    add_plugin("iconengines"),

    # locale für gettext
    ("locale", "locale"),

    # deine App-Dateien
    "icon.svg",
    "create_database.py",
    "create_table.py",
    "HelpWindow.py",
    "MainWindow.py",
    "main_funktions.py",
    "read_xml_file.py",
    "sql_queries.py",
    "table_functions.py",
    "terminal_table_classes.py",
]

# None-Einträge entfernen
include_files = [x for x in include_files if x is not None]

# --------------------------------------------------
# exclude files
# --------------------------------------------------

excludes = [
    # Python-Kram
    "tkinter",
    "unittest",
    "email",
    "http",
    "pydoc",
    "doctest",
    "distutils",
    "setuptools",
    "ensurepip",
    "venv",
    "lib2to3",

    # Qt / PySide6 Module (große Brocken!)
    "PySide6.QtQml",
    "PySide6.QtQuick",
    "PySide6.QtQuickWidgets",
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtWebEngineQuick",
    "PySide6.QtWebChannel",
    "PySide6.QtNetwork",
    "PySide6.QtMultimedia",
    "PySide6.QtMultimediaWidgets",
    "PySide6.QtBluetooth",
    "PySide6.QtPositioning",
    "PySide6.QtSensors",
    "PySide6.QtLocation",
    "PySide6.QtRemoteObjects",
    "PySide6.QtSerialBus",
    "PySide6.QtSerialPort",
    "PySide6.QtSvg",
    "PySide6.QtTextToSpeech",
    "PySide6.Qt3DCore",
    "PySide6.Qt3DExtras",
    "PySide6.Qt3DInput",
    "PySide6.Qt3DLogic",
    "PySide6.Qt3DRender",
    "PySide6.QtCharts",
    "PySide6.QtDataVisualization",
]


# --------------------------------------------------
# Build options
# --------------------------------------------------

build_exe_options = {
    "packages": [
        "os",
        "sys",
        "gettext",
        "sqlite3",
        "datetime",
        "xml.etree.ElementTree",
        "PySide6.QtWidgets",
        "PySide6.QtCore",
        "PySide6.QtGui",
    ],
    "excludes": excludes,
    "include_files": include_files,
    "optimize": 2,
}

# --------------------------------------------------
# Executable
# --------------------------------------------------
executables = [
    Executable(
        script="Main.py",   # 🔴 MUSS dein echter Startpunkt sein
        target_name="TerminalTableApp",
        icon="icon.svg",
        base=None,
    )
]

# --------------------------------------------------
# Setup
# --------------------------------------------------
setup(
    name="TerminalTableApp",
    version="1.0.0",
    description="TerminalTableApp",
    options={"build_exe": build_exe_options},
    executables=executables,
)
