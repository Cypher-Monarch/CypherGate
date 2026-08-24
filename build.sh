#!/usr/bin/env bash

set -euo pipefail

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

VERSION="${1:-}"

if [[ -z "$VERSION" ]]; then
  echo "Usage: $0 <version>"
  echo "Example: $0 v2.0.3"
  exit 1
fi

PROJECT="CypherGate-Linux-${VERSION}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="${ROOT_DIR}/src"
BUILD_DIR="${SRC_DIR}/build"
RELEASE_DIR="${ROOT_DIR}/${PROJECT}"
DIST_DIR="${ROOT_DIR}/dist"

VENV_DIR="${ROOT_DIR}/.venv"

# ─────────────────────────────────────────────
# Cleanup
# ─────────────────────────────────────────────

echo "==> Cleaning previous build..."

rm -rf "$BUILD_DIR"
rm -rf "$RELEASE_DIR"

mkdir -p "$DIST_DIR"

# ─────────────────────────────────────────────
# Virtual environment
# ─────────────────────────────────────────────

if [[ ! -d "$VENV_DIR" ]]; then
  echo "==> Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

echo "==> Activating virtual environment..."

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# ─────────────────────────────────────────────
# Dependencies
# ─────────────────────────────────────────────

echo "==> Installing dependencies..."

python -m pip install --upgrade pip
python -m pip install -r "$SRC_DIR/requirements.txt"

echo "==> Installing PyInstaller..."

python3 -m pip install pyinstaller==6.22.0 --break-system-packages

# ─────────────────────────────────────────────
# Build binaries
# ─────────────────────────────────────────────

echo "==> Building cyphergate..."

pyinstaller \
  --onefile \
  --hidden-import=plyer.platforms.linux.notification \
  --distpath "$BUILD_DIR" \
  "$SRC_DIR/cyphergate.py"

echo "==> Building cyphergated..."

pyinstaller \
  --onefile \
  --distpath "$BUILD_DIR" \
  "$SRC_DIR/cyphergated.py"

# ─────────────────────────────────────────────
# Validate binaries
# ─────────────────────────────────────────────

echo "==> Validating binaries..."

[[ -f "$BUILD_DIR/cyphergate" ]] ||
  {
    echo "ERROR: cyphergate binary was not produced"
    exit 1
  }

[[ -f "$BUILD_DIR/cyphergated" ]] ||
  {
    echo "ERROR: cyphergated binary was not produced"
    exit 1
  }

# ─────────────────────────────────────────────
# Assemble release
# ─────────────────────────────────────────────

echo "==> Creating release directory..."

mkdir -p "$RELEASE_DIR"

echo "==> Copying assets..."

cp -r "$SRC_DIR/Assets" "$RELEASE_DIR/"

echo "==> Copying binaries..."

cp "$BUILD_DIR/cyphergate" "$RELEASE_DIR/cyphergate.elf"
cp "$BUILD_DIR/cyphergated" "$RELEASE_DIR/cyphergated.elf"

# ─────────────────────────────────────────────
# Create archive
# ─────────────────────────────────────────────

ARCHIVE="${DIST_DIR}/${PROJECT}.tar.xz"

echo "==> Creating archive..."

tar -cJvf "$ARCHIVE" \
  -C "$ROOT_DIR" \
  "$PROJECT"

# ─────────────────────────────────────────────
# Done
# ─────────────────────────────────────────────

echo
echo "==> Release built successfully!"
echo
echo "Artifact:"
echo "    $ARCHIVE"
