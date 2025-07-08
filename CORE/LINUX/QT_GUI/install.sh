#!/bin/bash

set -e
set -o pipefail

APP_NAME="CypherGate"
INSTALL_DIR="/opt/$APP_NAME"
DESKTOP_ENTRY_PATH="/usr/share/applications/$APP_NAME.desktop"
RELEASE_URL="https://github.com/Cypher-Monarch/CypherGate/releases/download/v1.0.0/CypherGate-Linux-v1.0.0.zip"

# Detect root early
if [[ "$EUID" -ne 0 ]]; then
    echo "🚨 Please run this script with sudo: sudo $0"
    exit 1
fi

echo "🌐 Installing $APP_NAME..."

# Detect distro and install dependencies
echo "🔍 Checking required packages (openvpn, curl, unzip)..."

source /etc/os-release
case "$ID" in
    debian|ubuntu|kali)
        apt update
        apt install -y openvpn curl unzip
        ;;
    arch)
        pacman -Sy --noconfirm openvpn curl unzip
        ;;
    fedora)
        dnf install -y openvpn curl unzip
        ;;
    *)
        echo "⚠️ Unsupported distro: $ID"
        echo "Please install openvpn, curl, and unzip manually."
        exit 1
        ;;
esac

mkdir -p "$INSTALL_DIR"

echo "⬇️ Downloading latest release..."
TMP_DIR=$(mktemp -d)
curl -L "$RELEASE_URL" -o "$TMP_DIR/app.zip"

echo "📦 Extracting package..."
unzip "$TMP_DIR/app.zip" -d "$TMP_DIR"

cp "$TMP_DIR/cyphergate" "$INSTALL_DIR/"
cp -r "$TMP_DIR/Assets" "$INSTALL_DIR/"

# Create desktop file
tee "$DESKTOP_ENTRY_PATH" > /dev/null <<EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=CypherGate VPN
Exec=$INSTALL_DIR/cyphergate
Icon=$INSTALL_DIR/Assets/icon.png
Terminal=false
Categories=Network;Utility;
EOL

echo "✅ Installation complete!"
echo "You can now launch $APP_NAME from the app menu 🚀"

read -p "Do you want to launch $APP_NAME now? (y/N): " choice
case "$choice" in
  y|Y ) echo "🚀 Launching $APP_NAME..."; "$INSTALL_DIR/cyphergate" & ;;
  * ) echo "👌 Alright, launch it anytime from the menu." ;;
esac

rm -rf "$TMP_DIR"
