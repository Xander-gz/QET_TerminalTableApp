## TerminalTableApp

**TerminalTableApp** (KlemmenplanApp)ist eine grafische Desktop-Anwendung zur Erstellung von
Klemmen- bzw. Terminaltabellen für **QElectroTech-Dateien**.

Die Anwendung wurde mit **Python** und **PySide6 (Qt 6)** entwickelt und
unterstützt **mehrsprachige Oberflächen** via gettext. 

---
<img width="1060" height="708" alt="Bildschirmfoto vom 2026-02-14 16-28-24" src="https://github.com/user-attachments/assets/212be986-00e0-4067-9bca-dbc0b74c5544" />

## ✨ Funktionen

- Grafische Benutzeroberfläche (Qt / PySide6)
- Einlesen und Verarbeiten von XML-Dateien
- Nutzung einer SQLite-Datenbank
- Erstellen und Verwalten von Klemmentabellen
- Export / Weiterverarbeitung für QElectroTech
- AppImage (Linux)
- Windows-Executable

---

## 🖥️ Systemvoraussetzungen (Nutzer)

- Linux (getestet unter **Linux Mint**)
- Keine Python-Installation erforderlich (AppImage)

---

## Download

https://github.com/Xander-gz/QET_TerminalTableApp/releases

---

## ▶️ Anwendung starten

1. Datei ausführbar machen:
   ```bash
   chmod +x KlemmenplanApp-x86_64.AppImage

2. Starten:
   ./TerminalTableApp-X.X.X-x86_64.AppImage
   oder per Doppelklick im Dateimanager.

**Windows**

Die .exe aus den Releases herunterladen

Direkt starten (keine Installation notwendig)


---

## Entwicklung


**Voraussetzungen**

-Python ≥ 3.10

-PySide6

-gettext

-Qt6

**Lokaler Start**

python3 Main.py


**Build**

Der Build-Prozess ist im Skript build.sh dokumentiert.

Damit werden u. a. erzeugt:

Linux AppImage


---

## Lizense

Dieses Projekt steht unter 
GNU GENERAL PUBLIC LICENSE.

Details siehe LICENSE->.

