#!/bin/bash
# Install Tarri v1.0.0 — one-shot installer (curl -fsSL ... | bash)
set -euo pipefail

echo "[tarri] Installing Tarri v1.0.0 ..."

REPO_DIR=""
if [ -d "tarri" ]; then
    REPO_DIR="tarri"
elif [ -d "/home/ubuntu/tarri" ]; then
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

# Upgrade pip, then install package
if command -v pip3 >/dev/null 2>&1; then
    pip3 install --upgrade pip 2>/dev/null || python3 -m pip install --upgrade pip 2>/dev/null || true
fi

pip_install_cmd=""
if command -v pip3 >/dev/null 2>&1; then
    pip_install_cmd="pip3"
else
    pip_install_cmd="python3 -m pip"
fi

# Try editable, fallback normal install
${pip_install_cmd} install --break-system-packages -e "${REPO_DIR}" 2>/dev/null || \
${pip_install_cmd} install --break-system-packages "${REPO_DIR}" 2>/dev/null || \
${pip_install_cmd} install "${REPO_DIR}"

# Create standalone /usr/local/bin/tarri symlink/script for direct access
if command -v tarri >/dev/null 2>&1; then
    echo "[tarri] Command 'tarri' available."
else
    TARRI_CMD=$(python3 -c 'import importlib.util, sys; spec=importlib.util.find_spec("tarri.cli"); print("ok")' 2>/dev/null || echo "")
    if [ -n "${TARRI_CMD}" ]; then
        cat > /tmp/tarri_wrapper << 'WRAPPER'
#!/bin/bash
exec python3 -c 'from tarri.cli import main; import sys; sys.argv=["tarri"]+sys.argv[1:]; main()' "${@}"
WRAPPER
        chmod +x /tmp/tarri_wrapper
        sudo cp /tmp/tarri_wrapper /usr/local/bin/tarri 2>/dev/null || cp /tmp/tarri_wrapper /usr/local/bin/tarri 2>/dev/null || echo "[tarri] Note: add user bin to PATH for 'tarri' command."
        echo "[tarri] Created wrapper at /usr/local/bin/tarri (if writable)."
    fi
fi

echo "[tarri] Done. Try: tarri -v  /  tarri jalankan file.tarri"
