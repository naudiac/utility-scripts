#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  DaddySetup.sh v3 — Antigravity Tailscale Bootstrap
#  Run inside Termux on the phone.
#  Fixed: Tailscale installed as Android APK, not Linux pkg
# ============================================================

TS_AUTH_KEY="tskey-auth-ko5KuV6aJb11CNTRL-5kxWDTSMHZPMrVcRWBMAZPYQ1HMaPQu3"
TS_APK_URL="https://pkgs.tailscale.com/stable/tailscale-latest.apk"

PC_KEY_1="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCmVfYGeia54jL/nWwJRKc+pK+KtRA1AQd00ps4MOjf2ORBcT4Yd+HnuTfWItakLZyLzxrLuL1yjuzTBANd+DmEzvB4EIX83AZtM5T2UcFZJRfmFdSNZ8auGLudMFVTv6oQ+a6N2H75LG41shbpODZgmtThGqKkDiPQuXoQPqxPbqEXhAlmgWmRXBfUEd6vBoTwr0LzUzQFul6YSTfCk/RH8PpoKVFbT69brhRwodQ9GYRsN5EaO2eUrU71cILeQZiCFIa6YbPFuNfJWf+OWr6Qk205dGF/ZJSivaoUvtprWs7j1ayF0J0aK1Plpyd565OLQ7UdZoCOFmY3EcAGNGtP WITLOGISTICS-PC"
PC_KEY_2="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2tK1nGQVpffjM2K2PZlmgYq6wRXsG5sO+eZU6cOiPVfC4pdhn7gx69NYDpoA8VHxUr/3XMIgarpdPOsqE3GGUviqs1gQy98iK+JMPJT4ukgY9iLdpP1ILE0vmpy5BxKkd4aUiehep+UeG7UpqV/l6NLa0KMUWVg16a51d6hC985VAof7pykaeWJtW4nLQ7vRVmd0/QVdfet1rFg/gm+LsXwRKQISProX+pBPKg31O0Jf1zuwpGCl3gq0aZ/tWK5v2CCwEwYjTsX93NgVKAQYO/H8bV5l+OlKF6DT/BdG7lK2s0BiwZgbnUThtiY7uZYYQ8F4qKNx2Md63P1XtyvGL antigravity-pc"

echo ""
echo "\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557"
echo "\u2551   Antigravity Family Network Bootstrap   \u2551"
echo "\u2551            v3 \u2014 Android Fixed           \u2551"
echo "\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d"
echo ""

# -- Step 1: Packages (SSH + ADB only, NOT tailscale pkg) -----
echo "[1/4] Installing openssh and android-tools..."
for i in 1 2 3; do
  pkg install -y openssh android-tools 2>/dev/null && break
  echo "    Retry $i/3..."; sleep 5
done
echo "    \u2713 openssh + adb installed"

# -- Step 2: SSH server setup ---------------------------------
echo ""
echo "[2/4] Setting up SSH server..."
mkdir -p ~/.ssh; chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys
grep -q "WITLOGISTICS-PC" ~/.ssh/authorized_keys 2>/dev/null || echo "$PC_KEY_1" >> ~/.ssh/authorized_keys
grep -q "antigravity-pc" ~/.ssh/authorized_keys 2>/dev/null || echo "$PC_KEY_2" >> ~/.ssh/authorized_keys
pkill sshd 2>/dev/null; sleep 1; sshd
echo "    \u2713 SSH server ready on port 8022"

# -- Step 3: Download and install Tailscale APK ---------------
echo ""
echo "[3/4] Downloading Tailscale Android app..."
mkdir -p ~/antigravity
APK=~/antigravity/tailscale.apk
if [ ! -f "$APK" ]; then
  curl -fsSL -o "$APK" "$TS_APK_URL"
fi
echo "    \u2713 Downloaded: $(du -sh $APK | cut -f1)"

# Install via Android package manager (triggers install prompt)
echo "    Installing... (you may see an install prompt on screen - tap Install)"
am start -a android.intent.action.VIEW \
  -d "file://$APK" \
  -t "application/vnd.android.package-archive" \
  --flags 0x10000000 2>/dev/null || true
sleep 3

# -- Step 4: Write status + keepalive -------------------------
echo ""
echo "[4/4] Writing status and starting keepalive..."
mkdir -p ~/antigravity
cat > ~/antigravity/status.json <<EOF
{
  "connected": true,
  "ssh_ready": true,
  "ssh_port": 8022,
  "tailscale_install": "pending_user_approval",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "note": "Tailscale APK install prompt shown on screen"
}
EOF

# Keep sshd alive in background
(while true; do pgrep sshd > /dev/null || sshd; sleep 30; done) &

echo ""
echo "\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557"
echo "\u2551         \u2705 SETUP COMPLETE!               \u2551"
echo "\u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563"
echo "\u2551  SSH port  : 8022                        \u2551"
echo "\u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563"
echo "\u2551  ACTION: Tap INSTALL if prompted on      \u2551"
echo "\u2551  screen, then open Tailscale app and    \u2551"
echo "\u2551  tap Connect. Will handles the rest!    \u2551"
echo "\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d"
echo ""
