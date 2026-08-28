#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  DaddySetup.sh — Antigravity Tailscale Bootstrap v2
#  Run inside Termux. One command, Will does the rest remotely.
# ============================================================

TS_AUTH_KEY="tskey-auth-ko5KuV6aJb11CNTRL-5kxWDTSMHZPMrVcRWBMAZPYQ1HMaPQu3"
HOME_PING_URL="https://naudiac.github.io/utility-scripts/daddy-setup/connected.txt"

PC_KEY_1="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCmVfYGeia54jL/nWwJRKc+pK+KtRA1AQd00ps4MOjf2ORBcT4Yd+HnuTfWItakLZyLzxrLuL1yjuzTBANd+DmEzvB4EIX83AZtM5T2UcFZJRfmFdSNZ8auGLudMFVTv6oQ+a6N2H75LG41shbpODZgmtThGqKkDiPQuXoQPqxPbqEXhAlmgWmRXBfUEd6vBoTwr0LzUzQFul6YSTfCk/RH8PpoKVFbT69brhRwodQ9GYRsN5EaO2eUrU71cILeQZiCFIa6YbPFuNfJWf+OWr6Qk205dGF/ZJSivaoUvtprWs7j1ayF0J0aK1Plpyd565OLQ7UdZoCOFmY3EcAGNGtP WITLOGISTICS-PC"

PC_KEY_2="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2tK1nGQVpffjM2K2PZlmgYq6wRXsG5sO+eZU6cOiPVfC4pdhn7gx69NYDpoA8VHxUr/3XMIgarpdPOsqE3GGUviqs1gQy98iK+JMPJT4ukgY9iLdpP1ILE0vmpy5BxKkd4aUiehep+UeG7UpqV/l6NLa0KMUWVg16a51d6hC985VAof7pykaeWJtW4nLQ7vRVmd0/QVdfet1rFg/gm+LsXwRKQISProX+pBPKg31O0Jf1zuwpGCl3gq0aZ/tWK5v2CCwEwYjTsX93NgVKAQYO/H8bV5l+OlKF6DT/BdG7lK2s0BiwZgbnUThtiY7uZYYQ8F4qKNx2Md63P1XtyvGL antigravity-pc"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   Antigravity Family Network Bootstrap   ║"
echo "║            v2 — Auto-Deploy              ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ── Step 1: Packages ────────────────────────────────────────
echo "[1/5] Installing packages..."
pkg update -y -o Dpkg::Options::="--force-confnew" 2>/dev/null
pkg install -y openssh tailscale android-tools 2>/dev/null
echo "    ✓ openssh, tailscale, adb installed"

# ── Step 2: SSH Server ──────────────────────────────────────
echo ""
echo "[2/5] Configuring SSH..."
mkdir -p ~/.ssh
chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

if ! grep -q "WITLOGISTICS-PC" ~/.ssh/authorized_keys 2>/dev/null; then
    echo "$PC_KEY_1" >> ~/.ssh/authorized_keys
fi
if ! grep -q "antigravity-pc" ~/.ssh/authorized_keys 2>/dev/null; then
    echo "$PC_KEY_2" >> ~/.ssh/authorized_keys
fi

pkill sshd 2>/dev/null; sleep 1; sshd
echo "    ✓ SSH server ready on port 8022"

# ── Step 3: Tailscale ───────────────────────────────────────
echo ""
echo "[3/5] Connecting to home network..."
pkill tailscaled 2>/dev/null; sleep 1
tailscaled --state=~/.tailscale/tailscaled.state &
sleep 3
tailscale up \
    --authkey="$TS_AUTH_KEY" \
    --accept-routes \
    --accept-dns \
    --hostname="dads-phone"
echo "    ✓ Joined tailnet as: dads-phone"

# ── Step 4: Enable ADB on Fire TV (via USB or network) ──────
echo ""
echo "[4/5] Scanning for Fire TV Cube on local network..."
# Try to find Fire TV on common hotspot subnet
FIRE_TV_IP=""
for ip in $(seq 2 20); do
    candidate="192.168.43.$ip"
    if adb connect "$candidate:5555" 2>&1 | grep -q "connected"; then
        FIRE_TV_IP="$candidate"
        echo "    ✓ Fire TV found at $candidate"
        # Enable ADB over network for remote access by Will
        adb -s "$candidate:5555" shell setprop service.adb.tcp.port 5555
        break
    fi
done

if [ -z "$FIRE_TV_IP" ]; then
    echo "    ! Fire TV not auto-found (Will can do this remotely)"
fi

# ── Step 5: Report & Signal Home ────────────────────────────
echo ""
echo "[5/5] Signaling home..."
sleep 2
TS_IP=$(tailscale ip -4 2>/dev/null)

# Write a status file Will can poll
mkdir -p ~/antigravity
cat > ~/antigravity/status.json <<EOF
{
  "connected": true,
  "hostname": "dads-phone",
  "tailscale_ip": "$TS_IP",
  "ssh_port": 8022,
  "fire_tv_ip": "$FIRE_TV_IP",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║           ✅ SETUP COMPLETE!             ║"
echo "╠══════════════════════════════════════════╣"
echo "║  Tailscale IP : $TS_IP"
echo "║  SSH Port     : 8022"
echo "║  Hostname     : dads-phone"
echo "╠══════════════════════════════════════════╣"
echo "║  Will is now taking over remotely.       ║"
echo "║  Just keep Termux open — you're done!    ║"
echo "╚══════════════════════════════════════════╝"
echo ""
