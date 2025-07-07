#!/bin/bash

set -e

APP_NAME="CypherGate"
INSTALL_DIR="/opt/$APP_NAME"
DESKTOP_ENTRY_PATH="/usr/share/applications/$APP_NAME.desktop"

echo "Installing $APP_NAME..."

# Create install directory
sudo mkdir -p "$INSTALL_DIR"
sudo cp ./cyphergate "$INSTALL_DIR/"
sudo cp -r ./Assets "$INSTALL_DIR/"

# Create desktop file
sudo tee "$DESKTOP_ENTRY_PATH" > /dev/null <<EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=CypherGate VPN
Exec=$INSTALL_DIR/cyphergate
Icon=$INSTALL_DIR/Assets/icon.png
Terminal=false
Categories=Network;Utility;
EOL

echo "Installation complete ✅"
echo "You can now launch it from the app menu 🎉"

# Ask if user wants to launch it now
read -p "Do you want to launch $APP_NAME now? (y/N): " choice
case "$choice" in
  y|Y ) echo "Launching $APP_NAME..."; "$INSTALL_DIR/cyphergate" & ;;
  * ) echo "Alright, you can launch it anytime from the menu later 🚀";;
esac

