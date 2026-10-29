#!/bin/bash
# Install Tarri v1.0.0 — one-shot installer (curl -fsSL ... | bash)
set -euo pipefail

echo "[tarri] Installing Tarri v1.0.0 ..."

REPO_DIR=""
if [ -d "tarri" ]; then
    echo "[tarri] Deleting old local clone ..."
    rm -rf tarri
fi
if [ -d "/home/ubuntu/tarri" ]; then
    REPO_DIR="/home/ubuntu/tarri"
else
    echo "[tarri] Cloning repo ..."
    git clone --depth 1 https://github.com/tarri-dev/tarri.git tarri 2>/dev/null || git clone --depth 1 git@github.com:tarri-dev/tarri.git tarri
    REPO_DIR="tarri"
fi

if [ -z "${REPO_DIR}" ]; then
    echo "[tarri] ERROR: Could not find or clone repo."
    exit 1
fi

echo "[tarri] Using repo at: ${REPO_DIR}"
find "${REPO_DIR}/src" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Determine pip command first
pip_install_cmd=""
if command -v pip3 >/dev/null 2>&1; then
    pip_install_cmd="pip3"
else
    pip_install_cmd="python3 -m pip"
fi

# Clean old installation and cache
${pip_install_cmd} uninstall -y tarri 2>/dev/null || true
# Upgrade pip, then install package
if command -v pip3 >/dev/null 2>&1; then
    pip3 install --upgrade pip 2>/dev/null || python3 -m pip install --upgrade pip 2>/dev/null || true
fi

# Try editable, fallback normal install
${pip_install_cmd} install --upgrade --force-reinstall --no-cache-dir --break-system-packages -e "${REPO_DIR}" 2>/dev/null || \
${pip_install_cmd} install --upgrade --force-reinstall --no-cache-dir --break-system-packages "${REPO_DIR}" 2>/dev/null || \
${pip_install_cmd} install --upgrade --force-reinstall --no-cache-dir "${REPO_DIR}"

# Put pip-generated 'tarri' binary into /usr/local/bin (global, no python visible)
if command -v tarri >/dev/null 2>&1; then
    TARRI_BIN=$(command -v tarri)
    echo "[tarri] Command 'tarri' available at: ${TARRI_BIN}"
    # Ensure /usr/local/bin copy exists globally
    sudo cp "${TARRI_BIN}" /usr/local/bin/tarri 2>/dev/null || cp "${TARRI_BIN}" /usr/local/bin/tarri 2>/dev/null || echo "[tarri] Note: ensure /usr/local/bin is in PATH."
else
    echo "[tarri] Note: 'tarri' binary not found; add pip user/bin to PATH."
fi

echo "[tarri] Done. Try: tarri -v  /  tarri jalankan file.tarri"
