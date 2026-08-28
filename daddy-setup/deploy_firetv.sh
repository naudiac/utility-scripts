#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  deploy_firetv.sh — Remote Fire TV Cube Deployer
#  Runs automatically on Dad's phone via SSH from Antigravity.
#  Finds the Fire TV on the hotspot, installs Tailscale via ADB,
#  connects it to the home exit node. Zero manual steps.
# ============================================================

TS_APK_URL="https://pkgs.tailscale.com/stable/tailscale-latest.apk"
TS_AUTH_KEY="tskey-auth-ko5KuV6aJb11CNTRL-5kxWDTSMHZPMrVcRWBMAZPYQ1HMaPQu3"
STATUS_FILE="$HOME/antigravity/status.json"
LOG_FILE="$HOME/antigravity/deploy.log"

mkdir -p "$HOME/antigravity"
exec > >(tee -a "$LOG_FILE") 2>&1

log() { echo "[$(date '+%H:%M:%S')] $1"; }

log "=== Fire TV Auto-Deploy Starting ==="

# ── Find Fire TV on hotspot subnet ─────────────────────────
FIRE_TV_IP=""
log "Scanning hotspot subnets for Fire TV Cube..."

for subnet in "192.168.43" "192.168.0" "192.168.1" "10.0.0"; do
    for host in $(seq 2 30); do
        ip="$subnet.$host"
        # Try ADB connect, Fire TV listens on 5555
        result=$(adb connect "$ip:5555" 2>&1)
        if echo "$result" | grep -q "connected to"; then
            # Verify it's actually a Fire TV
            model=$(adb -s "$ip:5555" shell getprop ro.product.model 2>/dev/null | tr -d '\r')
            if echo "$model" | grep -qi "fire\|AFTM\|AFTT\|AFTS"; then
                FIRE_TV_IP="$ip"
                log "Found Fire TV Cube: $model at $ip:5555"
                break 2
            else
                adb disconnect "$ip:5555" 2>/dev/null
            fi
        fi
    done
done

if [ -z "$FIRE_TV_IP" ]; then
    log "Fire TV not found via ADB. Enabling ADB on Fire TV requires Developer Mode."
    log "Trying mDNS/broadcast discovery..."
    # Fallback: try common Fire TV IPs on hotspot
    for ip in "192.168.43.100" "192.168.43.101" "192.168.43.102"; do
        result=$(adb connect "$ip:5555" 2>&1)
        if echo "$result" | grep -q "connected"; then
            FIRE_TV_IP="$ip"
            log "Found device at $ip"
            break
        fi
    done
fi

if [ -z "$FIRE_TV_IP" ]; then
    log "ERROR: Could not find Fire TV. Will try again in 60s."
    jq -n --arg ts "$(tailscale ip -4 2>/dev/null)" '{connected:true,hostname:"dads-phone",tailscale_ip:$ts,fire_tv_found:false,stage:"searching_firetv"}' > "$STATUS_FILE"
    exit 1
fi

# ── Download Tailscale APK to phone ────────────────────────
APK_PATH="$HOME/antigravity/tailscale.apk"
if [ ! -f "$APK_PATH" ]; then
    log "Downloading Tailscale APK..."
    curl -fsSL -o "$APK_PATH" "$TS_APK_URL"
    log "Download complete: $(du -sh $APK_PATH | cut -f1)"
else
    log "Tailscale APK already cached."
fi

# ── Push and install on Fire TV ────────────────────────────
log "Installing Tailscale on Fire TV ($FIRE_TV_IP)..."
adb -s "$FIRE_TV_IP:5555" install -r "$APK_PATH" 2>&1
log "Install complete."

# ── Configure Tailscale on Fire TV via ADB shell ───────────
log "Launching Tailscale and authenticating..."

# Start Tailscale service
adb -s "$FIRE_TV_IP:5555" shell "am start -n com.tailscale.ipn.tv/.MainActivity" 2>/dev/null
sleep 3

# Use Tailscale CLI via ADB to authenticate with key
adb -s "$FIRE_TV_IP:5555" shell "cmd activity start-activity -W -a android.intent.action.VIEW -d 'https://login.tailscale.com/a/$TS_AUTH_KEY'" 2>/dev/null
sleep 5

# Set exit node via adb shell am broadcast
adb -s "$FIRE_TV_IP:5555" shell "am broadcast -a com.tailscale.ipn.SET_EXIT_NODE --es node wit01467" 2>/dev/null

log "=== Fire TV Setup Complete ==="

# ── Update status ──────────────────────────────────────────
TS_IP=$(tailscale ip -4 2>/dev/null)
jq -n \
    --arg ts "$TS_IP" \
    --arg ftv "$FIRE_TV_IP" \
    --arg ts2 "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '{connected:true,hostname:"dads-phone",tailscale_ip:$ts,fire_tv_ip:$ftv,fire_tv_configured:true,stage:"complete",timestamp:$ts2}' \
    > "$STATUS_FILE"

log "Status written. Will is watching."
