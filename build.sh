#!/usr/bin/env bash
set -e

APP_NAME="TerminalTableApp"
ARCH="x86_64"

PROJECT_ROOT="$(pwd)"
APPDIR="$PROJECT_ROOT/AppDir"
APPIMAGETOOL="$PROJECT_ROOT/AppImagetool/appimagetool-x86_64.AppImage"

# --------------------------------------------------
# 📦 Version automatisch aus pyproject.toml lesen
# --------------------------------------------------
VERSION=$(python - <<EOF
import tomllib
with open("pyproject.toml","rb") as f:
    print(tomllib.load(f)["project"]["version"])
EOF
)

echo "📌 Version: $VERSION"

# --------------------------------------------------
# 🧹 Clean
# --------------------------------------------------
rm -rf build dist AppDir *.AppImage

# --------------------------------------------------
# 🐍 venv
# --------------------------------------------------
source venv/bin/activate

pip install -U pip
pip install pyinstaller .

# --------------------------------------------------
# 🔨 Build Binary
# --------------------------------------------------


SEP=":"
[[ "$OS" == "Windows_NT" ]] && SEP=";"


pyinstaller \
  --name "$APP_NAME" \
  --onefile \
  --clean \
  --paths src \
  --add-data "src/TerminalTableApp/locale${SEP}locale" \
  --add-data "src/TerminalTableApp/icons${SEP}icons" \
  src/TerminalTableApp/run.py


# --------------------------------------------------
# 📁 AppDir
# --------------------------------------------------


if [[ "$OSTYPE" == "linux-gnu"* ]]; then

mkdir -p "$APPDIR/usr/bin"

# nur die Binary!
install -Dm755 "dist/$APP_NAME" "$APPDIR/usr/bin/$APP_NAME"

install -Dm644 icon.png "$APPDIR/$APP_NAME.png"
install -Dm644 icon.svg "$APPDIR/$APP_NAME.svg"



cat > "$APPDIR/AppRun" << EOF
#!/bin/sh
HERE="$(dirname "$(readlink -f "$0")")"

exec "$APPDIR/usr/bin/TerminalTableApp" "$@"

EOF

chmod +x "$APPDIR/AppRun"



cat > "$APPDIR/$APP_NAME.desktop" <<EOF
[Desktop Entry]
Name=$APP_NAME
Exec=$APP_NAME
Icon=$APP_NAME
Type=Application
Categories=Utility;
Terminal=true
EOF

# --------------------------------------------------
# 🚀 AppImage bauen
# --------------------------------------------------
chmod +x "$APPIMAGETOOL"

"$APPIMAGETOOL" "$APPDIR" "$APP_NAME-$VERSION-$ARCH.AppImage"

echo
echo "✅ Fertig:"
echo "$APP_NAME-$VERSION-$ARCH.AppImage"

fi


