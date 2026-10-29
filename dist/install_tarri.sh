#!/bin/bash
# Install Tarri — one-shot installer (curl -fsSL ... | bash)
set -euo pipefail

echo "[tarri] Installing Tarri v1.0.0..."

# Find repo or clone it
REPO_DIR=""
if [ -d "tarri" ]; then
    REPO_DIR="tarri"
elif [ -d "/home/ubuntu/tarri" ]; then
    REPO_DIR="/home/ubuntu/tarri"
else
    echo "[tarri] Cloning repo..."
    git clone --depth 1 https://github.com/tarri-dev/tarri.git tarri 2>/dev/null || git clone --depth 1 git@github.com:tarri-dev/tarri.git tarri
    REPO_DIR="tarri"
fi

if [ -z "$REPO_DIR" ]; then
    echo "[tarri] ERROR: Could not find or clone repo."
    exit 1
fi

echo "[tarri] Using repo at: $REPO_DIR"

# Find repo or clone it
REPO_DIR=""
if [ -d "tarri" ]; then
    REPO_DIR="tarri"
elif [ -d "/home/ubuntu/tarri" ]; then
    REPO_DIR="/home/ubuntu/tarri"
else
    echo "[tarri] Cloning repo..."
    git clone --depth 1 https://github.com/tarri-dev/tarri.git tarri 2>/dev/null || git clone --depth 1 git@github.com:tarri-dev/tarri.git tarri
    REPO_DIR="tarri"
fi

if [ -z "$REPO_DIR" ]; then
    echo "[tarri] ERROR: Could not find or clone repo."
    exit 1
fi

echo "[tarri] Using repo at: $REPO_DIR"

# Clean caches
find "$REPO_DIR/src" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Install (editable if possible, else normal install)
if command -v pip3 &> /dev/null; then
    pip3 install --upgrade pip 2>/dev/null || true
    pip3 install --break-system-packages -e "$REPO_DIR" 2>/dev/null || pip3 install --break-system-packages "$REPO_DIR" || pip3 install "$REPO_DIR"
else
    python3 -m pip install --upgrade pip 2>/dev/null || true
    python3 -m pip install --break-system-packages -e "$REPO_DIR" 2>/dev/null || python3 -m pip install --break-system-packages "$REPO_DIR" || python3 -m pip install "$REPO_DIR"
fi

echo "[tarri] Done. Try: tarri -v  /  tarri jalankan"
