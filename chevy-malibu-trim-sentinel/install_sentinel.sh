#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# install_sentinel.sh
# ==============================================================================
# Universal 1-Click Bootstrap Installer for In-Car Robot Sentinel on Android.
# Configures Termux environment, auto-wake-lock, remote SSH guardian keys,
# hands-free voice engine, and local PWA telemetry server.
#
# Author: William Hanusiewicz (naudiac) & Antigravity
# Repository: https://github.com/naudiac/utility-scripts
# ==============================================================================

set -e

echo ""
echo "======================================================="
echo "🚗 IN-CAR AUTONOMOUS SENTINEL - BOOTSTRAP INSTALLER 🚗"
echo "======================================================="
echo ""

# 1. Update Package Repositories & Install Dependencies
echo "[1/5] 📦 Installing core dependencies (Python, OpenSSH, Termux API)..."
pkg update -y >/dev/null 2>&1 || true
pkg install -y python git curl openssh termux-api net-tools >/dev/null 2>&1

# 2. Acquire Termux Wakelock
echo "[2/5] ⚡ Setting up background wakelock (prevents battery sleep)..."
termux-wake-lock || true

# 3. Setup Remote Guardian SSH Access for William
echo "[3/5] 🔑 Setting up secure SSH access for William/Antigravity..."
mkdir -p ~/.ssh
chmod 700 ~/.ssh
AUTH_KEYS="$HOME/.ssh/authorized_keys"
WILLIAM_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2tK1nGQVpffjM2K2PZlmgYq6wRXsG5sO+eZU6cOiPVfC4pdhn7gx69NYDpoA8VHxUr/3XMIgarpdPOsqE3GGUviqs1gQy98iK+JMPJT4ukgY9iLdpP1ILE0vmpy5BxKkd4aUiehep+UeG7UpqV/l6NLa0KMUWVg16a51d6hC985VAof7pykaeWJtW4nLQ7vRVmd0/QVdfet1rFg/gm+LsXwRKQISProX+pBPKg31O0Jf1zuwpGCl3gq0aZ/tWK5v2CCwEwYjTsX93NgVKAQYO/H8bV5l+OlKF6DT/BdG7lK2s0BiwZgbnUThtiY7uZYYQ8F4qKNx2Md63P1XtyvGL antigravity@pc"

if ! grep -q "antigravity@pc" "$AUTH_KEYS" 2>/dev/null; then
    echo "$WILLIAM_KEY" >> "$AUTH_KEYS"
    chmod 600 "$AUTH_KEYS"
    echo "    ✓ Guardian key added to authorized_keys."
fi

# Ensure sshd is running
pkill -f sshd || true
sshd

# 4. Download Master Sentinel Daemon
echo "[4/5] 🛰️ Downloading latest Sentinel Daemon from GitHub..."
SENTINEL_URL="https://raw.githubusercontent.com/naudiac/utility-scripts/main/chevy-malibu-trim-sentinel/malibu_trim_sentinel.py"
curl -sSL "$SENTINEL_URL" > "$HOME/mobile_edge_node.py"
chmod +x "$HOME/mobile_edge_node.py"

# 5. Create Auto-Launcher & Start
echo "[5/5] 🚀 Starting In-Car Sentinel Daemon..."
pkill -f mobile_edge_node.py || true
nohup python3 "$HOME/mobile_edge_node.py" > "$HOME/sentinel.log" 2>&1 &

# Set volume and speak welcome announcement
termux-volume music 15 >/dev/null 2>&1 || true
termux-tts-speak "In-car Sentinel successfully installed and active! Open Chrome at localhost 8080 to view your live dashboard." >/dev/null 2>&1 || true

echo ""
echo "======================================================="
echo "🎉 INSTALLATION COMPLETE! SENTINEL IS LIVE!"
echo "======================================================="
echo "📱 Local HUD URL : http://localhost:8080"
echo "🔌 BT Bridge Port: 35001 (or 35000)"
echo "🔑 SSH Status    : Port 8022 (Active for Remote Support)"
echo "======================================================="
echo ""
