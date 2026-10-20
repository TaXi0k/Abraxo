#!/bin/sh

printf "\033[1m\033[38;2;255;100;68mWelcome to the Abraxo installer!\n\n\033[0m"

# ===========================
# ==== Installing uv ========
# ===========================

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
User=$USER
WorkingDirectory=$HOME/.local/share/abraxo
ExecStart=$UV_PATH run $HOME/.local/share/abraxo/abraxo.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

printf "* Generated systemd service file succesfully!"
