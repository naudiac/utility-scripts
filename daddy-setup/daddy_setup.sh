#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
#  daddy_setup.sh — Antigravity Family Network Bootstrap (v2)
#  Bulletproof Termux bootstrap for Dad's Samsung phone.
#  Connects phone to Tailscale network, opens SSH access, and prepares
#  the environment for remote Fire TV Cube deployment.
# ==============================================================================

# Ensure pipefail and defined error traps
set -o pipefail

# Configuration
TS_AUTH_KEY="tskey-auth-ko5KuV6aJb11CNTRL-5kxWDTSMHZPMrVcRWBMAZPYQ1HMaPQu3"
TS_HOSTNAME="dads-phone"
SSH_PORT="8022"
RAW_URL="https://raw.githubusercontent.com/naudiac/utility-scripts/main/daddy-setup/daddy_setup.sh"

STATUS_DIR="$HOME/antigravity"
STATUS_FILE="$STATUS_DIR/status.json"
KEEPALIVE_SCRIPT="$STATUS_DIR/keepalive.sh"

PC_KEY_1="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCmVfYGeia54jL/nWwJRKc+pK+KtRA1AQd00ps4MOjf2ORBcT4Yd+HnuTfWItakLZyLzxrLuL1yjuzTBANd+DmEzvB4EIX83AZtM5T2UcFZJRfmFdSNZ8auGLudMFVTv6oQ+a6N2H75LG41shbpODZgmtThGqKkDiPQuXoQPqxPbqEXhAlmgWmRXBfUEd6vBoTwr0LzUzQFul6YSTfCk/RH8PpoKVFbT69brhRwodQ9GYRsN5EaO2eUrU71cILeQZiCFIa6YbPFuNfJWf+OWr6Qk205dGF/ZJSivaoUvtprWs7j1ayF0J0aK1Plpyd565OLQ7UdZoCOFmY3EcAGNGtP WITLOGISTICS-PC"
PC_KEY_2="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2tK1nGQVpffjM2K2PZlmgYq6wRXsG5sO+eZU6cOiPVfC4pdhn7gx69NYDpoA8VHxUr/3XMIgarpdPOsqE3GGUviqs1gQy98iK+JMPJT4ukgY9iLdpP1ILE0vmpy5BxKkd4aUiehep+UeG7UpqV/l6NLa0KMUWVg16a51d6hC985VAof7pykaeWJtW4nLQ7vRVmd0/QVdfet1rFg/gm+LsXwRKQISProX+pBPKg31O0Jf1zuwpGCl3gq0aZ/tWK5v2CCwEwYjTsX93NgVKAQYO/H8bV5l+OlKF6DT/BdG7lK2s0BiwZgbnUThtiY7uZYYQ8F4qKNx2Md63P1XtyvGL antigravity-pc"

mkdir -p "$STATUS_DIR"

# ------------------------------------------------------------------------------
# Helper: Atomic Status Telemetry Writer
# ------------------------------------------------------------------------------
write_status() {
    mkdir -p "$STATUS_DIR" 2>/dev/null || true
    local connected="$1"
    local stage="$2"
    local ts_ip="$3"
    local err="$4"
    local ts
    ts=$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date)

    local json_ts_ip="null"
    if [ -n "$ts_ip" ]; then
        json_ts_ip="\"$ts_ip\""
    fi

    local json_err="null"
    if [ -n "$err" ]; then
        json_err="\"$err\""
    fi

    cat > "$STATUS_FILE.tmp" <<EOF
{
  "connected": $connected,
  "stage": "$stage",
  "hostname": "$TS_HOSTNAME",
  "tailscale_ip": $json_ts_ip,
  "ssh_port": $SSH_PORT,
  "fire_tv_ip": null,
  "fire_tv_configured": false,
  "error": $json_err,
  "timestamp": "$ts"
}
EOF
    mv "$STATUS_FILE.tmp" "$STATUS_FILE"
}

# ------------------------------------------------------------------------------
# Helper: Error Handler and Abort
# ------------------------------------------------------------------------------
fail() {
    local msg="$1"
    echo ""
    echo "  ❌ [FATAL ERROR] $msg"
    write_status false "error" "" "$msg"
    exit 1
}

# ------------------------------------------------------------------------------
# Helper: Self-Update Check (if executed as local file)
# ------------------------------------------------------------------------------
check_self_update() {
    if [ -n "$DADDY_SKIP_UPDATE" ] || [ "$0" = "bash" ] || [ "$0" = "-bash" ]; then
        return 0
    fi

    if [ -f "$0" ] && command -v curl >/dev/null 2>&1; then
        echo "  ⏳ Checking for latest bootstrap script version..."
        local tmp_file
        tmp_file=$(mktemp 2>/dev/null || echo "/tmp/daddy_setup_latest.sh")
        if curl -fsSL --connect-timeout 5 --max-time 15 "$RAW_URL" -o "$tmp_file" 2>/dev/null; then
            if [ -s "$tmp_file" ] && ! cmp -s "$0" "$tmp_file" 2>/dev/null; then
                echo "  ✓ Newer version detected. Updating and reloading..."
                cp "$tmp_file" "$0"
                chmod +x "$0"
                rm -f "$tmp_file"
                export DADDY_SKIP_UPDATE=1
                exec "${BASH:-bash}" "$0" "$@"
            fi
        fi
        rm -f "$tmp_file"
    fi
}

# ------------------------------------------------------------------------------
# Step 1: Package Installation with 3x Retry and Backoff
# ------------------------------------------------------------------------------
install_pkg_with_retry() {
    local pkg="$1"
    local bin="$2"
    local max_retries=3
    local attempt=1

    if [ -n "$bin" ] && command -v "$bin" >/dev/null 2>&1; then
        echo "    ✓ $pkg already installed"
        return 0
    fi

    while [ $attempt -le $max_retries ]; do
        echo "    ⏳ Installing $pkg (attempt $attempt/$max_retries)..."
        if pkg install -y -o Dpkg::Options::="--force-confnew" "$pkg" >/dev/null 2>&1; then
            if [ -z "$bin" ] || command -v "$bin" >/dev/null 2>&1; then
                echo "    ✓ $pkg installed successfully"
                return 0
            fi
        fi
        echo "    ⚠️ Attempt $attempt failed for $pkg. Updating repository and retrying..."
        pkg update -y >/dev/null 2>&1 || true
        sleep $((attempt * 2))
        attempt=$((attempt + 1))
    done

    echo "    ❌ ERROR: Failed to install $pkg after $max_retries attempts"
    return 1
}

# ------------------------------------------------------------------------------
# Step 2: SSH Server Configuration
# ------------------------------------------------------------------------------
setup_ssh() {
    echo ""
    echo "[2/5] Configuring SSH Access..."

    mkdir -p "$HOME/.ssh" || fail "Cannot create ~/.ssh directory"
    chmod 700 "$HOME/.ssh"

    touch "$HOME/.ssh/authorized_keys" || fail "Cannot create ~/.ssh/authorized_keys"
    chmod 600 "$HOME/.ssh/authorized_keys"

    # Ensure trailing newline on pre-existing authorized_keys
    if [ -s "$HOME/.ssh/authorized_keys" ] && [ -n "$(tail -c 1 "$HOME/.ssh/authorized_keys" 2>/dev/null)" ]; then
        echo "" >> "$HOME/.ssh/authorized_keys"
    fi

    # Inject keys idempotently
    local keys_added=0
    if ! grep -Fxq "$PC_KEY_1" "$HOME/.ssh/authorized_keys" 2>/dev/null; then
        echo "$PC_KEY_1" >> "$HOME/.ssh/authorized_keys"
        keys_added=$((keys_added + 1))
    fi
    if ! grep -Fxq "$PC_KEY_2" "$HOME/.ssh/authorized_keys" 2>/dev/null; then
        echo "$PC_KEY_2" >> "$HOME/.ssh/authorized_keys"
        keys_added=$((keys_added + 1))
    fi

    echo "    ✓ Authorized keys configured ($keys_added new keys added, 2 active)"

    # Generate host keys if missing
    ssh-keygen -A >/dev/null 2>&1 || true

    # Start / Restart sshd daemon
    pkill -x sshd 2>/dev/null || true
    sleep 1
    sshd || fail "Failed to launch sshd daemon"

    # Verify sshd is running
    if pgrep -x sshd >/dev/null 2>&1; then
        echo "    ✓ SSH daemon running on port $SSH_PORT"
    else
        fail "SSH daemon is not running after startup"
    fi
}

# ------------------------------------------------------------------------------
# Step 3: Userspace Tailscale Setup & Authentication
# ------------------------------------------------------------------------------
setup_tailscale() {
    echo ""
    echo "[3/5] Connecting to Tailscale Network..."

    mkdir -p "$HOME/.tailscale"
    if [ -n "$PREFIX" ]; then
        mkdir -p "$PREFIX/var/run/tailscale" 2>/dev/null || true
    fi

    # Terminate any existing tailscaled daemon
    pkill -x tailscaled 2>/dev/null || true
    sleep 1

    # Start tailscaled in userspace mode
    tailscaled --state="$HOME/.tailscale/tailscaled.state" >/dev/null 2>&1 &

    # Poll socket readiness (up to 10 seconds)
    local ready=0
    for _ in $(seq 1 10); do
        if tailscale status >/dev/null 2>&1 || [ $? -eq 1 ]; then
            ready=1
            break
        fi
        sleep 1
    done

    if [ $ready -ne 1 ]; then
        fail "tailscaled socket failed to become ready within 10 seconds"
    fi
    echo "    ✓ tailscaled daemon ready"

    # Join Tailnet with pre-auth key
    echo "    ⏳ Authenticating with Tailscale network..."
    if ! tailscale up \
        --authkey="$TS_AUTH_KEY" \
        --hostname="$TS_HOSTNAME" \
        --accept-routes \
        --accept-dns=true \
        --reset >/dev/null 2>&1; then
        fail "tailscale up command failed to authenticate"
    fi

    # Poll for valid Tailscale IPv4 address
    echo "    ⏳ Acquiring Tailscale IP address..."
    local raw_ip=""
    local ts_ip=""
    for _ in $(seq 1 15); do
        raw_ip=$(tailscale ip -4 2>/dev/null | tr -d ' \r\n')
        if echo "$raw_ip" | grep -Eq '^100\.[0-9]+\.[0-9]+\.[0-9]+$'; then
            ts_ip="$raw_ip"
            break
        fi
        sleep 1
    done

    if [ -z "$ts_ip" ] || ! echo "$ts_ip" | grep -Eq '^100\.[0-9]+\.[0-9]+\.[0-9]+$'; then
        fail "Failed to obtain a valid Tailscale IPv4 address (100.x.y.z). Received: '${raw_ip:-<empty>}'"
    fi

    echo "    ✓ Joined tailnet as: $TS_HOSTNAME ($ts_ip)"
    export DADDY_TS_IP="$ts_ip"
}

# ------------------------------------------------------------------------------
# Step 4: Keepalive Daemon & Android Wake Lock Setup
# ------------------------------------------------------------------------------
setup_keepalive() {
    echo ""
    echo "[4/5] Establishing Persistence & Keepalive..."

    # Request wake lock if Termux API / wake lock binary exists
    if command -v termux-wake-lock >/dev/null 2>&1; then
        termux-wake-lock 2>/dev/null || true
        echo "    ✓ Termux wake lock acquired"
    fi

    # Create standalone watchdog script
    cat > "$KEEPALIVE_SCRIPT" <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  keepalive.sh — Antigravity Phone Daemon Watchdog
# ============================================================
while true; do
    if ! pgrep -x sshd >/dev/null 2>&1; then
        sshd 2>/dev/null || true
    fi
    if ! pgrep -x tailscaled >/dev/null 2>&1; then
        tailscaled --state="$HOME/.tailscale/tailscaled.state" >/dev/null 2>&1 &
    fi
    sleep 20
done
EOF
    chmod +x "$KEEPALIVE_SCRIPT"

    # Spawn background watchdog if not already running
    if ! pgrep -f "antigravity/keepalive.sh" >/dev/null 2>&1; then
        nohup "$KEEPALIVE_SCRIPT" >/dev/null 2>&1 &
        echo "    ✓ Background watchdog daemon launched"
    else
        echo "    ✓ Background watchdog daemon already running"
    fi
}

# ------------------------------------------------------------------------------
# Step 5: Write Telemetry & Completion Banner
# ------------------------------------------------------------------------------
finalize_setup() {
    echo ""
    echo "[5/5] Emitting Status Telemetry..."

    write_status true "phone_online" "$DADDY_TS_IP" ""
    echo "    ✓ Telemetry written to $STATUS_FILE"

    echo ""
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║              ✅ SETUP COMPLETE!                      ║"
    echo "╠══════════════════════════════════════════════════════╣"
    printf "║  Tailscale IP : %-36s ║\n" "$DADDY_TS_IP"
    printf "║  SSH Port     : %-36s ║\n" "$SSH_PORT"
    printf "║  Hostname     : %-36s ║\n" "$TS_HOSTNAME"
    printf "║  Stage        : %-36s ║\n" "phone_online"
    echo "╠══════════════════════════════════════════════════════╣"
    echo "║  William & Antigravity are now connected remotely.   ║"
    echo "║  Keep Termux running in the background.              ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo ""

    # If running interactively, stay open with heartbeat
    if [ -t 0 ] && [ -z "$DADDY_NON_INTERACTIVE" ]; then
        echo "  [Keepalive loop active — Press Ctrl+C to exit shell]"
        while true; do
            sleep 60
        done
    fi
}

# ------------------------------------------------------------------------------
# Main Execution Flow
# ------------------------------------------------------------------------------
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║        Antigravity Family Network Bootstrap          ║"
    echo "║               v2.0 — Production Grade                ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo ""

    # Self-update check
    check_self_update "$@"

    # Step 1: Packages
    echo "[1/5] Installing Required Packages..."
    install_pkg_with_retry "curl" "curl" || fail "Failed to install curl"
    install_pkg_with_retry "openssh" "sshd" || fail "Failed to install openssh"
    install_pkg_with_retry "tailscale" "tailscale" || fail "Failed to install tailscale"
    install_pkg_with_retry "android-tools" "adb" || fail "Failed to install android-tools"

    # Step 2: SSH
    setup_ssh

    # Step 3: Tailscale
    setup_tailscale

    # Step 4: Keepalive
    setup_keepalive

    # Step 5: Finalize
    finalize_setup
}

# Invoke main entrypoint
main "$@"
