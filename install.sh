#!/bin/sh

printf "\033[1m\033[38;2;255;100;68mWelcome to the Abraxo installer!\n\n\033[0m"


# =============================
# ==== Removing leftovers =====
# =============================

systemctl --user stop abraxo 2>/dev/null || true
systemctl --user disable abraxo 2>/dev/null || true
rm -f ~/.local/share/abraxo/abraxo.py
rm -f ~/.config/systemd/user/abraxo.service
systemctl --user daemon-reload


# ========================
# ==== Installing uv =====
# ========================

# Check if uv is installed
if ! command -v uv > /dev/null 2>&1; then
    printf "* uv is not found on your system. Installing it now...\n"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Ensure it's in PATH:
    export PATH="$HOME/.local/bin:$PATH"
fi

# Final verification check
if ! command -v uv > /dev/null 2>&1; then
    printf "Error: uv installation failed or binary not found in PATH.\n"
    printf "Try installing it manually: https://astral.sh/uv/install.sh\n"
    exit 1
fi

echo "* uv is installed!"


# ==============================
# ==== Downloading .py file ====
# ==============================

# Create ~/.local/share/abraxo if doesnt exist
mkdir -p ~/.local/share/abraxo

# Download the file and save it to file
curl -sS https://raw.githubusercontent.com/TaXi0k/Abraxo/refs/heads/master/abraxo.py > ~/.local/share/abraxo/abraxo.py

printf "* Succesfully downloaded abraxo.py\n"


# ===============================
# ==== Creating serivce file ====
# ===============================

# Get path to uv
UV_PATH="$(command -v uv)"

# Check if uv is availbable one more time
if [ -z "$UV_PATH" ]; then
    printf "Error: failed to get uv path, consider reinstalling it"
    exit 1
fi

# Create ~/.config/systemd/user if doesnt exist
mkdir -p ~/.config/systemd/user

cat << EOF > ~/.config/systemd/user/abraxo.service
[Unit]
Description=Abraxo Downloads-Sorting Daemon
After=network.target

[Service]
Type=simple
WorkingDirectory=$HOME/.local/share/abraxo
ExecStart=$UV_PATH run $HOME/.local/share/abraxo/abraxo.py
Restart=on-failure
RestartSec=5s

# Environment=MD_CODE=[true/false]
# Environment=DOWNLOADS_DIRECTORY=[/example/path/to/downloads/directory]

[Install]
WantedBy=default.target
EOF

printf "* Generated systemd service file succesfully!\n"

# ==============================
# ==== Starting the service ====
# ==============================

systemctl --user daemon-reload

systemctl --user enable --now abraxo.service

printf "\n\033[32m✔ Abraxo successfully installed and started!\033[0m\n"