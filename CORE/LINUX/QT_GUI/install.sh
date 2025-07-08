#!/bin/bash

set -e
set -o pipefail

APP_NAME="CypherGate"
INSTALL_DIR="/opt/$APP_NAME"
DESKTOP_ENTRY_PATH="/usr/share/applications/$APP_NAME.desktop"
GITHUB_REPO="Cypher-Monarch/CypherGate"

trap 'echo "❌ Installation failed. Exiting." >&2' ERR

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

echo "⬇️ Fetching latest release info..."
API_URL="https://api.github.com/repos/$GITHUB_REPO/releases/latest"
LATEST_RELEASE=$(curl -s "$API_URL")

# Extract download URL (with or without jq)
if command -v jq &> /dev/null; then
    DOWNLOAD_URL=$(echo "$LATEST_RELEASE" | jq -r '.assets[0].browser_download_url')
else
    DOWNLOAD_URL=$(echo "$LATEST_RELEASE" | grep "browser_download_url" | head -n 1 | cut -d '"' -f 4)
fi

echo "📥 Downloading from: $DOWNLOAD_URL"
TMP_DIR=$(mktemp -d)
curl -L "$DOWNLOAD_URL" -o "$TMP_DIR/app.zip"

echo "📦 Extracting package..."
unzip "$TMP_DIR/app.zip" -d "$TMP_DIR"

# Move into extracted folder (fix for nested directory inside ZIP)
cd "$TMP_DIR"/CypherGate-Linux

cp cyphergate.elf "$INSTALL_DIR/"
cp -r Assets "$INSTALL_DIR/"

tee "$DESKTOP_ENTRY_PATH" > /dev/null <<EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=CypherGate VPN
Exec=$INSTALL_DIR/cyphergate.elf
Icon=$INSTALL_DIR/Assets/icon.png
Terminal=false
Categories=Network;Utility;
EOL

echo "✅ Installation complete!"
echo "You can now launch $APP_NAME from the app menu 🚀"

read -p "Do you want to launch $APP_NAME now? (y/N): " choice
case "$choice" in
  y|Y ) echo "🚀 Launching $APP_NAME..."; "$INSTALL_DIR/cyphergate.elf" & ;;
  * ) echo "👌 Alright, launch it anytime from the menu." ;;
esac

rm -rf "$TMP_DIR"

