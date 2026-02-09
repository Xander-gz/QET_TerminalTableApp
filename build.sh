#!/usr/bin/env bash
set -e

APP_NAME="TerminalTableApp"
APP_ID="terminaltable"
PYTHON_VERSION="3.12"
ARCH=$(uname -m)

ROOT="$(pwd)"
APPDIR="$ROOT/AppDir"

echo "📦 Read version from pyproject.toml"
VERSION=$(grep -E '^version\s*=' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')
echo "➡ Version: $VERSION"

# echo "🧹 Clean"
# rm -rf "$APPDIR" *.AppImage

echo "📁 Create AppDir"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

echo "🐍 Activate venv"
source venv/bin/activate

echo "📦 Install app into AppDir"
pip install . --prefix="$APPDIR/usr" --no-compile

echo "🚀 Launcher"
cat > "$APPDIR/usr/bin/$APP_ID" << EOF
#!/usr/bin/env bash
HERE=\$(dirname "\$(readlink -f "\$0")")

export PYTHONPATH="\$HERE/../lib/python$PYTHON_VERSION/site-packages"
export QT_QPA_PLATFORM_PLUGIN_PATH="\$PYTHONPATH/PySide6/plugins/platforms"
export QT_PLUGIN_PATH="\$PYTHONPATH/PySide6/plugins"

exec "\$HERE/python3" -m TerminalTableApp "\$@"
EOF

chmod +x "$APPDIR/usr/bin/$APP_ID"

echo "🖥 Desktop file"
cat > "$APPDIR/$APP_ID.desktop" << EOF
[Desktop Entry]
Type=Application
Name=$APP_NAME
Exec=$APP_ID
Icon=$APP_ID
Categories=Utility;
Terminal=false
EOF

echo "🖼 Icon"
cp icon.png "$APPDIR/$APP_ID.png"

echo "📦 Copy Python runtime"
cp -r venv/bin "$APPDIR/usr/"
cp -r venv/lib "$APPDIR/usr/"

echo "🧼 Qt plugin optimization"

QT_PLUGINS="$APPDIR/usr/lib/python$PYTHON_VERSION/site-packages/PySide6/plugins"

# Nur das nötigste behalten
KEEP_PLUGINS=(
  platforms
  imageformats
  styles
)

for dir in "$QT_PLUGINS"/*; do
  name=$(basename "$dir")
  if [[ ! " ${KEEP_PLUGINS[@]} " =~ " $name " ]]; then
    echo "  ❌ removing Qt plugin: $name"
    rm -rf "$dir"
  fi
done

echo "🧼 Remove unused Qt platform plugins"
PLATFORMS="$QT_PLUGINS/platforms"
rm -f "$PLATFORMS"/libqwayland*
rm -f "$PLATFORMS"/libqxcb.so.debug

echo "🧼 Remove PySide tests & cache"
find "$APPDIR/usr" -type d -name "__pycache__" -exec rm -rf {} +
find "$APPDIR/usr" -type d -name "tests" -exec rm -rf {} +

# --------------------------------------------------
# 🔟 Build AppImage
# --------------------------------------------------


#if ! command -v appimagetool &> /dev/null; then
#  echo "❌ appimagetool not installed"
#  exit 1
#fi

#appimagetool "$APPDIR" "$APP_NAME-$VERSION-$ARCH.AppImage"


 echo "🧱 Building AppImage"
 



./appimagetool-x86_64.AppImage "$APPDIR" "$APP_NAME-$VERSION-$ARCH.AppImage"



echo "✅ Done!"
echo "➡️  $APP_NAME-$VERSION-$ARCH.AppImage"


