#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# 🚀 1-Tap Home Screen Launcher for Malibu Robot Sentinel
# Author: William Hanusiewicz (naudiac) & Antigravity
# ==============================================================================

echo -e "\033[1;36m[+] Initializing Malibu Robot Sentinel...\033[0m"

# 1. Kill any existing instances cleanly
pkill -f malibu_trim_sentinel.py >/dev/null 2>&1
sleep 0.5

# 2. Launch daemon in background
nohup python3 /data/data/com.termux/files/home/utility-scripts/chevy-malibu-trim-sentinel/malibu_trim_sentinel.py >/dev/null 2>&1 &
sleep 1.0

# 3. Open the full-screen standalone dashboard
echo -e "\033[1;32m[✓] Daemon Online! Opening Dashboard on Screen...\033[0m"
termux-open-url http://localhost:8080/

