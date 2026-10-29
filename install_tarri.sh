#!/bin/bash
# Install Tarri — one-shot installer (curl -fsSL ... | bash)
set -euo pipefail

echo "[tarri] Installing Tarri via local setup..."

# If running from github raw URL, this runs locally; adjust if needed
cd /home/ubuntu/tarri || { echo "Repo not found at /home/ubuntu/tarri"; exit 1; }

# Clean old caches
find src -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# System-wide install (break-system-packages for Ubuntu 24+)
if command -v pip3 &> /dev/null; then
    pip3 install --break-system-packages -e . 2>/dev/null || pip3 install -e .
else
    python3 -m pip install --break-system-packages -e . 2>/dev/null || python3 -m pip install -e .
fi

echo "[tarri] Done. Try: tarri -v  /  tarri jalankan"
