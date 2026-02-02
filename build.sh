#!/bin/bash
set -e

APP=TerminalTableApp
DOMAIN=TerminalTableApp
VERSION=0.3.4
ARCH=x86_64

APPDIR="$APP.AppDir"
DOCDIR="$APPDIR/usr/share/doc/$APP"

echo "🚀 Building $APP AppImage"

# --------------------------------------------------
# 1️⃣ Clean old builds
# --------------------------------------------------
rm -rf build dist "$APPDIR" *.AppImage

# --------------------------------------------------
# 2️⃣ Extract translations (pygettext)
# --------------------------------------------------
echo "🌍 Extracting translation template (.pot)"
mkdir -p locale
pygettext3 -d $DOMAIN -o locale/$DOMAIN.pot $(find src -name "*.py")

# --------------------------------------------------
# 3️⃣ Build Python app (cx_Freeze)
# --------------------------------------------------
echo "🐍 Building Python application"
python3 setup.py build

# --------------------------------------------------
# 4️⃣ Compile translations (.po → .mo)
# --------------------------------------------------
echo "🌍 Compiling translations"
find locale -name "*.po" | while read po; do
    mo="${po%.po}.mo"
    msgfmt "$po" -o "$mo"
done

# --------------------------------------------------
# 5️⃣ Create AppDir structure
# --------------------------------------------------
echo "📦 Creating AppDir structure"

mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/locale"
mkdir -p "$DOCDIR"

# Copy built app
cp -r build/exe.linux-x86_64-3.13/* "$APPDIR/usr/bin/"

# Copy translations
cp -r locale/* "$APPDIR/usr/share/locale/"

# --------------------------------------------------
# 6️⃣ Copy documentation (LICENSE & README)
# --------------------------------------------------
echo "📄 Copying documentation"

[ -f LICENSE ] && cp LICENSE "$DOCDIR/"
[ -f README.md ] && cp README.md "$DOCDIR/"

# --------------------------------------------------
# 7️⃣ Desktop file
# --------------------------------------------------
cat > "$APPDIR/$APP.desktop" << EOF
[Desktop Entry]
Type=Application
Name=TerminalTableApp
Exec=TerminalTableApp
Icon=TerminalTableApp
Categories=Utility;
EOF

# --------------------------------------------------
# 8️⃣ AppRun
# --------------------------------------------------
cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "$0")")"

export APPDIR="$HERE"
export PATH="$HERE/usr/bin:$PATH"
export LD_LIBRARY_PATH="$HERE/usr/lib:$LD_LIBRARY_PATH"

exec "$HERE/usr/bin/TerminalTableApp" "$@"
EOF

chmod +x "$APPDIR/AppRun"

# --------------------------------------------------
# 9️⃣ Icon (optional)
# --------------------------------------------------
if [ -f "icon.png" ]; then
    cp icon.png "$APPDIR/TerminalTableApp.png"
fi

if [ -f "icon.svg" ]; then
    cp icon.png "$APPDIR/TerminalTableApp.svg"
fi

# --------------------------------------------------
# 🔟 Build AppImage
# --------------------------------------------------
echo "🧱 Building AppImage"

if [ ! -f "appimagetool-x86_64.AppImage" ]; then
    wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x appimagetool-x86_64.AppImage
fi

./appimagetool-x86_64.AppImage "$APPDIR" "$APP-$VERSION-$ARCH.AppImage"



echo "✅ Done!"
echo "➡️  $APP-$VERSION-$ARCH.AppImage"



