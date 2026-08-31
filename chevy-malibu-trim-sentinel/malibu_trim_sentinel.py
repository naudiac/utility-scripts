"""
malibu_trim_sentinel.py
=======================
Antigravity Nexus OS & Malibu Robot Mode Daemon (v23 - Home Screen PWA Package).
Zero-Token Autonomous In-Car Co-Pilot & Universal Swarm Controller with 4-Level Speech Verbosity.

PWA Package Features:
  - 📱 1-Tap Android Home Screen App Installation (Web App Manifest + Service Worker).
  - 🎨 Cyberpunk Maskable App Icon & Fullscreen Standalone App Container (No browser address bar).
  - 🤖 Autonomous Robot Mode (User-Controlled ARM/DISARM).
  - 🎙️ 4-Level Speech Verbosity Selector (Mute, Low, Medium, High).
  - 🚗 6-Gauge Live HUD & 60 FPS Canvas Oscilloscope.
  - 📁 Blackbox CSV Flight Recorder & 1-Tap GitHub Auto-Sync.
"""

import os
import sys
import json
import time
import socket
import queue
import threading
import subprocess
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

HOST = "0.0.0.0"
HTTP_PORT = 8080
OBD_BRIDGE_HOST = "127.0.0.1"
OBD_BRIDGE_PORT = 35000
PC_MASTER_IP = "100.104.120.44"
PC_MASTER_PORT = 8090

LOG_FILE = "/data/data/com.termux/files/home/malibu_flight_log.csv"
ROBOT_LOG_FILE = "/data/data/com.termux/files/home/malibu_robot_resets.json"

telemetry_lock = threading.Lock()
command_queue = queue.Queue()
command_results = {}

# Live Sensor Telemetry
live_state = {
    "rpm": 0,
    "speed": 0,
    "stft": 0.0,
    "ltft": 0.0,
    "maf": 0.0,
    "map": 0,
    "temp": 0,
    "volt": 12.6,
    "dtc_count": 0,
    "samples_logged": 0,
    "is_connected": False,
    "last_update": 0
}
history_buffer = []

# 🤖 User-Controlled Robot Mode State with 4-Level Speech Verbosity
SPEECH_LEVELS_MAP = {"mute": 0, "low": 1, "medium": 2, "high": 3}

robot_state = {
    "armed": False,                  # DEFAULT: DISARMED (Manual Arm Required)
    "speech_level": "medium",        # Options: 'mute', 'low', 'medium', 'high'
    "threshold_ltft": 22.0,          # Trigger when LTFT >= +22.0%
    "threshold_total": 28.0,         # Trigger when (STFT + LTFT) >= +28.0%
    "cooldown_sec": 75,              # Minimum seconds between resets
    "last_reset_time": 0,
    "consecutive_spikes": 0,
    "resets_today": 0,
    "status_message": "DISARMED (Idle • Zero Commands Sent)",
    "recent_events": []
}

def init_logs():
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        try:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.write("timestamp,rpm,speed_mph,stft_pct,ltft_pct,maf_gps,map_kpa,coolant_c,battery_volt\n")
        except Exception:
            pass
    if not os.path.exists(ROBOT_LOG_FILE):
        try:
            with open(ROBOT_LOG_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
        except Exception:
            pass

def log_robot_event(event: dict):
    try:
        events = []
        if os.path.exists(ROBOT_LOG_FILE):
            with open(ROBOT_LOG_FILE, "r", encoding="utf-8") as f:
                events = json.load(f)
        events.append(event)
        if len(events) > 100:
            events = events[-100:]
        with open(ROBOT_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2)
    except Exception as e:
        print(f"[-] Robot log error: {e}")

def speak_offline(text: str, required_level: str = "low"):
    """
    Speaks aloud locally through Android TTS respecting the user's speech verbosity level:
      • 'low': Critical events only (Reset actions)
      • 'medium': Arm/Disarm, reset events, elevated warnings
      • 'high': Detailed status narration, sensor readings, periodic checks
      • 'mute': 100% silent
    """
    current_lvl = robot_state.get("speech_level", "medium")
    if current_lvl == "mute":
        return
    
    curr_val = SPEECH_LEVELS_MAP.get(current_lvl, 2)
    req_val = SPEECH_LEVELS_MAP.get(required_level, 1)

    if curr_val >= req_val:
        safe_text = text.replace("'", "\\'").replace('"', '\\"')
        cmd = f"/data/data/com.termux/files/usr/bin/termux-tts-speak '{safe_text}'"
        subprocess.Popen(cmd, shell=True)

def parse_rpm_val(resp: str):
    tokens = [t for t in resp.replace("\r", " ").replace("\n", " ").split(" ") if len(t) == 2]
    try:
        idx = tokens.index("0C")
        a = int(tokens[idx+1], 16)
        b = int(tokens[idx+2], 16)
        return round(((a * 256) + b) / 4.0, 1)
    except Exception:
        return None

def parse_trim_val(resp: str, pid_hex: str):
    tokens = [t for t in resp.replace("\r", " ").replace("\n", " ").split(" ") if len(t) == 2]
    try:
        idx = tokens.index(pid_hex)
        a = int(tokens[idx+1], 16)
        return round((a - 128.0) * 100.0 / 128.0, 2)
    except Exception:
        return None

def parse_maf_val(resp: str):
    tokens = [t for t in resp.replace("\r", " ").replace("\n", " ").split(" ") if len(t) == 2]
    try:
        idx = tokens.index("10")
        a = int(tokens[idx+1], 16)
        b = int(tokens[idx+2], 16)
        return round(((a * 256) + b) / 100.0, 2)
    except Exception:
        return None

def parse_map_val(resp: str):
    tokens = [t for t in resp.replace("\r", " ").replace("\n", " ").split(" ") if len(t) == 2]
    try:
        idx = tokens.index("0B")
        return int(tokens[idx+1], 16)
    except Exception:
        return None

def parse_temp_val(resp: str):
    tokens = [t for t in resp.replace("\r", " ").replace("\n", " ").split(" ") if len(t) == 2]
    try:
        idx = tokens.index("05")
        return int(tokens[idx+1], 16) - 40
    except Exception:
        return None

def parse_volt_val(resp: str):
    try:
        m = resp.replace("\r", " ").split()
        for token in m:
            if "V" in token:
                return float(token.replace("V", ""))
    except Exception:
        pass
    return None

def background_telemetry_poller():
    """Persistent 2.5 Hz CAN bus poller with Priority Command Multiplexing & Robot Watchdog."""
    init_logs()
    sample_count = 0

    while True:
        try:
            s = socket.create_connection((OBD_BRIDGE_HOST, OBD_BRIDGE_PORT), timeout=2.0)
            s.settimeout(2.0)
            
            def send_raw(cmd):
                s.sendall((cmd.strip() + "\r").encode("utf-8"))
                buf = bytearray()
                while True:
                    chunk = s.recv(128)
                    if not chunk: break
                    buf.extend(chunk)
                    if b">" in chunk: break
                return buf.decode("utf-8", errors="ignore").replace(">", "").strip()

            send_raw("ATSP6")
            send_raw("ATSH 7DF")
            send_raw("ATE0")

            while True:
                # 1. High-Priority Manual/Queue Commands
                while not command_queue.empty():
                    req_id, req_cmd = command_queue.get()
                    resp_val = send_raw(req_cmd)
                    with telemetry_lock:
                        command_results[req_id] = resp_val

                # 2. Regular Telemetry Poll Cycle
                r_rpm = send_raw("010C")
                rpm = parse_rpm_val(r_rpm)

                r_stft = send_raw("0106")
                stft = parse_trim_val(r_stft, "06")

                r_ltft = send_raw("0107")
                ltft = parse_trim_val(r_ltft, "07")

                r_maf = send_raw("0110")
                maf = parse_maf_val(r_maf)

                r_map = send_raw("010B")
                map_v = parse_map_val(r_map)

                r_temp = send_raw("0105")
                temp_v = parse_temp_val(r_temp)

                r_volt = send_raw("ATRV")
                volt_v = parse_volt_val(r_volt)

                with telemetry_lock:
                    if rpm is not None: live_state["rpm"] = rpm
                    if stft is not None: live_state["stft"] = stft
                    if ltft is not None: live_state["ltft"] = ltft
                    if maf is not None: live_state["maf"] = maf
                    if map_v is not None: live_state["map"] = map_v
                    if temp_v is not None: live_state["temp"] = temp_v
                    if volt_v is not None: live_state["volt"] = volt_v
                    
                    sample_count += 1
                    live_state["samples_logged"] = sample_count
                    live_state["is_connected"] = True
                    live_state["last_update"] = time.time()

                    history_buffer.append({
                        "t": time.strftime("%H:%M:%S"),
                        "rpm": live_state["rpm"],
                        "stft": live_state["stft"],
                        "ltft": live_state["ltft"],
                        "maf": live_state["maf"],
                        "volt": live_state["volt"]
                    })
                    if len(history_buffer) > 60:
                        history_buffer.pop(0)

                # 3. 🤖 AUTONOMOUS ROBOT WATCHDOG EVALUATION
                if robot_state["armed"] and live_state["is_connected"]:
                    curr_rpm = live_state["rpm"]
                    curr_ltft = live_state["ltft"]
                    curr_stft = live_state["stft"]
                    total_trim = curr_stft + curr_ltft
                    now = time.time()

                    # Trigger condition: Engine running (>500 RPM) and high lean trim
                    is_spike = (curr_rpm > 500) and (curr_ltft >= robot_state["threshold_ltft"] or total_trim >= robot_state["threshold_total"])
                    
                    if is_spike:
                        robot_state["consecutive_spikes"] += 1
                        if robot_state["consecutive_spikes"] == 1:
                            speak_offline(f"Warning: Fuel trim rising to plus {int(curr_ltft)} percent.", required_level="high")
                    else:
                        robot_state["consecutive_spikes"] = max(0, robot_state["consecutive_spikes"] - 1)

                    # Trigger after 3 consecutive spikes (~1.2s) and cooldown expired
                    if robot_state["consecutive_spikes"] >= 3 and (now - robot_state["last_reset_time"] > robot_state["cooldown_sec"]):
                        print(f"\n[🤖 ROBOT HEAL TRIGGERED]: LTFT={curr_ltft}%, Total={total_trim}%, RPM={curr_rpm}")
                        
                        # Step 1: Capture Freeze Frame
                        freeze_frame = {
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "trigger_reason": f"LEAN_TRIM_SPIKE (LTFT: +{curr_ltft}%, Total: +{total_trim:.1f}%)",
                            "rpm": curr_rpm,
                            "stft_pct": curr_stft,
                            "ltft_pct": curr_ltft,
                            "total_trim_pct": round(total_trim, 2),
                            "maf_gps": live_state["maf"],
                            "coolant_c": live_state["temp"],
                            "volt": live_state["volt"]
                        }

                        # Step 2: Send Mode 04 to Clear Adaptation Tables
                        send_raw("04")
                        robot_state["last_reset_time"] = now
                        robot_state["resets_today"] += 1
                        robot_state["consecutive_spikes"] = 0
                        robot_state["status_message"] = f"ACTIVE (Last Reset: {time.strftime('%H:%M:%S')} • LTFT +{curr_ltft}%)"
                        robot_state["recent_events"].insert(0, freeze_frame)
                        if len(robot_state["recent_events"]) > 20:
                            robot_state["recent_events"].pop()

                        # Step 3: Log to disk
                        log_robot_event(freeze_frame)

                        # Step 4: Local Audio Announcement (Respects Speech Level)
                        speak_offline(f"Robot Mode: Fuel trim reached plus {int(curr_ltft)} percent. Resetting learned tables to zero.", required_level="low")

                # Write continuous CSV
                try:
                    with open(LOG_FILE, "a", encoding="utf-8") as f:
                        ts = time.strftime("%Y-%m-%d %H:%M:%S")
                        f.write(f"{ts},{live_state['rpm']},{live_state['speed']},{live_state['stft']},{live_state['ltft']},{live_state['maf']},{live_state['map']},{live_state['temp']},{live_state['volt']}\n")
                except Exception:
                    pass

                time.sleep(0.35)

        except Exception:
            with telemetry_lock:
                live_state["is_connected"] = False
            time.sleep(1.5)

# PWA Assets: Manifest & SVG Icon
MANIFEST_JSON = {
    "name": "Malibu Robot Sentinel",
    "short_name": "Malibu Robot",
    "description": "Autonomous Zero-Token Trim Sentinel & Live Automotive HUD for 2013 Chevy Malibu ECO",
    "start_url": "/?source=pwa",
    "display": "standalone",
    "background_color": "#070a12",
    "theme_color": "#00f2fe",
    "orientation": "portrait",
    "icons": [
        {
            "src": "/icon.svg",
            "sizes": "192x192 512x512",
            "type": "image/svg+xml",
            "purpose": "any maskable"
        }
    ]
}

ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070a12"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f2fe"/>
      <stop offset="100%" stop-color="#a855f7"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="110" fill="url(#bg)" stroke="#1e293b" stroke-width="12"/>
  <path d="M256 60 L410 120 L410 270 C410 370 256 450 256 450 C256 450 102 370 102 270 L102 120 Z" fill="none" stroke="url(#accent)" stroke-width="18" stroke-linejoin="round"/>
  <circle cx="256" cy="240" r="70" fill="none" stroke="#00f2fe" stroke-width="14"/>
  <circle cx="256" cy="240" r="30" fill="#00f2fe"/>
  <path d="M190 320 Q256 370 322 320" fill="none" stroke="#a855f7" stroke-width="12" stroke-linecap="round"/>
  <text x="256" y="420" font-family="-apple-system, sans-serif" font-size="34" font-weight="900" fill="#f8fafc" text-anchor="middle" letter-spacing="4">MALIBU ROBOT</text>
</svg>"""

SERVICE_WORKER_JS = """
self.addEventListener('install', (e) => {
  self.skipWaiting();
});
self.addEventListener('activate', (e) => {
  return self.clients.claim();
});
self.addEventListener('fetch', (e) => {
  e.respondWith(fetch(e.request).catch(() => new Response('Offline')));
});
"""

def generate_dashboard_html(active_tab: str = "hud") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#070a12">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Malibu Robot">
    <link rel="manifest" href="/manifest.json">
    <link rel="icon" type="image/svg+xml" href="/icon.svg">
    <link rel="apple-touch-icon" href="/icon.svg">
    <title>Malibu Robot Sentinel</title>
    <style>
        :root {{
            --bg-color: #070a12;
            --card-bg: #0f172a;
            --card-border: #1e293b;
            --accent-cyan: #00f2fe;
            --accent-blue: #38bdf8;
            --accent-green: #10b981;
            --accent-red: #ef4444;
            --accent-amber: #f59e0b;
            --accent-purple: #a855f7;
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0; padding: 12px 12px 90px 12px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-color); color: var(--text-main);
            display: flex; flex-direction: column; align-items: center; min-height: 100vh;
        }}
        .container {{ width: 100%; max-width: 480px; }}
        
        .header {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 12px;
        }}
        .header-title h1 {{ margin: 0; font-size: 20px; font-weight: 800; background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .header-title p {{ margin: 2px 0 0 0; color: var(--text-dim); font-size: 11px; }}
        .header-buttons {{ display: flex; gap: 6px; }}
        .btn-header {{
            background: #1e293b; border: 1px solid #334155; color: var(--accent-cyan);
            border-radius: 8px; padding: 7px 10px; font-size: 11px; font-weight: bold; cursor: pointer;
        }}

        /* 🤖 ROBOT MODE HERO BANNER */
        .robot-hero {{
            background: linear-gradient(135deg, #0b1329, #17112c);
            border: 2px solid #334155; border-radius: 14px; padding: 14px;
            margin-bottom: 14px; display: flex; flex-direction: column; gap: 10px;
            transition: all 0.3s ease;
        }}
        .robot-hero.armed {{
            border-color: var(--accent-cyan);
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.25);
        }}
        .robot-hero-top {{
            display: flex; justify-content: space-between; align-items: center;
        }}
        .robot-title {{ font-size: 14px; font-weight: 800; display: flex; align-items: center; gap: 6px; }}
        .robot-badge {{
            font-size: 10px; font-weight: 800; padding: 4px 8px; border-radius: 12px;
            text-transform: uppercase;
        }}
        .badge-disarmed {{ background: #334155; color: #94a3b8; }}
        .badge-armed {{ background: var(--accent-cyan); color: #04060a; animation: pulse-border 1.5s infinite; }}

        @keyframes pulse-border {{
            0%, 100% {{ box-shadow: 0 0 0 0 rgba(0,242,254,0.7); }}
            50% {{ box-shadow: 0 0 0 6px rgba(0,242,254,0); }}
        }}

        .btn-robot-toggle {{
            width: 100%; padding: 14px; border-radius: 10px; border: none;
            font-size: 14px; font-weight: 800; cursor: pointer; transition: all 0.15s;
            display: flex; align-items: center; justify-content: center; gap: 8px;
            -webkit-tap-highlight-color: transparent;
        }}
        .btn-robot-arm {{
            background: linear-gradient(135deg, #00f2fe, #0284c7); color: #04060a;
            box-shadow: 0 4px 14px rgba(0,242,254,0.35);
        }}
        .btn-robot-disarm {{
            background: linear-gradient(135deg, #ef4444, #b91c1c); color: #fff;
            box-shadow: 0 4px 14px rgba(239,68,68,0.35);
        }}

        /* 🎙️ 4-LEVEL SPEECH SELECTOR */
        .speech-selector {{
            display: flex; flex-direction: column; gap: 6px;
            background: #060913; border: 1px solid var(--card-border);
            padding: 8px 10px; border-radius: 10px; margin-top: 2px;
        }}
        .speech-header {{
            display: flex; justify-content: space-between; align-items: center;
            font-size: 10px; font-weight: 800; text-transform: uppercase; color: var(--text-dim);
        }}
        .speech-pills {{
            display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 4px;
        }}
        .speech-pill {{
            padding: 8px 2px; font-size: 11px; font-weight: 800; border-radius: 6px;
            border: 1px solid #1e293b; background: #0f172a; color: var(--text-dim);
            cursor: pointer; transition: all 0.12s ease; outline: none; text-align: center;
        }}
        .speech-pill:active {{ transform: scale(0.96); }}
        .speech-pill.active {{
            background: #1e293b; border-color: var(--accent-cyan); color: var(--accent-cyan);
            box-shadow: 0 0 10px rgba(0,242,254,0.25);
        }}

        /* 📑 TOP NAVIGATION PILLS */
        .domain-scroll {{
            display: flex; gap: 8px; overflow-x: auto; padding-bottom: 6px; margin-bottom: 12px;
            scrollbar-width: none;
        }}
        .domain-scroll::-webkit-scrollbar {{ display: none; }}
        .domain-pill {{
            flex: 0 0 auto; background: #0b1120; border: 1px solid var(--card-border);
            padding: 8px 14px; border-radius: 20px; font-size: 12px; font-weight: 700;
            color: var(--text-dim); cursor: pointer; text-decoration: none; transition: all 0.15s;
        }}
        .domain-pill.active {{
            background: #1e293b; color: var(--accent-cyan); border-color: rgba(56,189,248,0.6);
            box-shadow: 0 2px 10px rgba(0,242,254,0.15);
        }}

        .card {{
            background: var(--card-bg); border: 1px solid var(--card-border);
            border-radius: 12px; padding: 14px; margin-bottom: 12px;
        }}
        .card-header {{
            display: flex; justify-content: space-between; align-items: center;
            font-size: 12px; font-weight: bold; text-transform: uppercase; color: var(--text-dim); margin-bottom: 10px;
        }}

        .metric-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 12px; }}
        .metric-card {{
            background: #0b1120; border: 1px solid var(--card-border);
            border-radius: 10px; padding: 12px; display: flex; flex-direction: column;
        }}
        .metric-title {{ font-size: 10px; text-transform: uppercase; color: var(--text-dim); margin-bottom: 2px; }}
        .metric-val {{ font-size: 22px; font-weight: 800; font-family: monospace; color: var(--accent-cyan); }}
        .metric-unit {{ font-size: 10px; font-weight: normal; color: var(--text-dim); margin-left: 2px; }}

        .btn-group {{ display: flex; flex-direction: column; gap: 8px; margin-bottom: 12px; }}
        .btn {{
            padding: 13px; border: none; border-radius: 10px; font-size: 13px; font-weight: 700;
            cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px;
            color: #fff; transition: transform 0.1s; -webkit-tap-highlight-color: transparent;
        }}
        .btn:active {{ transform: scale(0.98); }}
        .btn-action {{ background: #1e293b; border: 1px solid #334155; }}
        .btn-voice {{ background: linear-gradient(135deg, #a855f7, #7e22ce); box-shadow: 0 4px 14px rgba(168,85,247,0.4); }}
        .btn-danger {{ background: linear-gradient(135deg, #ef4444, #dc2626); }}

        .terminal-box {{
            background: #04060a; border: 1px solid #1e293b; border-radius: 10px;
            padding: 12px; font-family: 'Consolas', monospace; font-size: 11px;
            color: #38bdf8; min-height: 160px; max-height: 240px; overflow-y: auto;
            margin-bottom: 12px; line-height: 1.4; white-space: pre-wrap;
        }}

        .event-table {{ width: 100%; border-collapse: collapse; font-size: 11px; margin-top: 6px; }}
        .event-table th {{ text-align: left; padding: 6px; color: var(--text-dim); border-bottom: 1px solid #1e293b; }}
        .event-table td {{ padding: 6px; border-bottom: 1px solid #0f172a; font-family: monospace; }}

        canvas {{ width: 100%; height: 110px; background: #04060a; border-radius: 6px; }}

        /* 📱 BOTTOM DOCK */
        .bottom-dock {{
            position: fixed; bottom: 0; left: 0; right: 0;
            background: rgba(11, 17, 32, 0.98); backdrop-filter: blur(12px);
            border-top: 1px solid var(--card-border);
            display: grid; grid-template-columns: 1fr 1fr 1fr 1fr;
            padding: 8px 6px 14px 6px; z-index: 9999;
        }}
        .dock-item {{
            text-decoration: none; display: flex; flex-direction: column; align-items: center;
            justify-content: center; color: var(--text-dim); font-size: 10px; font-weight: bold;
            padding: 4px 0; border-radius: 8px; transition: all 0.1s;
        }}
        .dock-item.active {{ color: var(--accent-cyan); }}
        .dock-item span.icon {{ font-size: 18px; margin-bottom: 2px; }}
    </style>
    <script>
        // Register Service Worker for PWA
        if ('serviceWorker' in navigator) {{
            navigator.serviceWorker.register('/sw.js').catch(err => console.log('SW error:', err));
        }}

        let deferredPrompt = null;
        window.addEventListener('beforeinstallprompt', (e) => {{
            e.preventDefault();
            deferredPrompt = e;
            const btn = document.getElementById('btn-pwa-install');
            if (btn) btn.style.display = 'block';
        }});

        function installPWA() {{
            if (deferredPrompt) {{
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {{
                    if (choiceResult.outcome === 'accepted') {{
                        console.log('User installed Malibu Robot PWA');
                    }}
                    deferredPrompt = null;
                }});
            }} else {{
                alert('To add to Home Screen:\\n1. Tap Chrome 3-dots menu (⋮) at top-right\\n2. Tap \"Add to Home screen\" or \"Install app\"');
            }}
        }}

        window.switchTab = function(tab, e) {{
            if (e) e.preventDefault();
            try {{ if (window.navigator && window.navigator.vibrate) window.navigator.vibrate(20); }} catch(err) {{}}

            var allTabs = ['hud', 'robot', 'blackbox', 'swarm'];
            allTabs.forEach(function(t) {{
                var sec = document.getElementById('sec-' + t);
                var pill = document.getElementById('pill-' + t);
                var dock = document.getElementById('dock-' + t);
                if (t === tab) {{
                    if (sec) sec.style.display = 'block';
                    if (pill) pill.classList.add('active');
                    if (dock) dock.classList.add('active');
                }} else {{
                    if (sec) sec.style.display = 'none';
                    if (pill) pill.classList.remove('active');
                    if (dock) dock.classList.remove('active');
                }}
            }});
            try {{ window.history.replaceState(null, '', '/' + tab); }} catch(err) {{}}
            return false;
        }};
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-title">
                <h1>🧠 Malibu Robot Sentinel</h1>
                <p>Autonomous Zero-Token Trim Sentinel</p>
            </div>
            <div class="header-buttons">
                <button type="button" class="btn-header" id="btn-pwa-install" onclick="installPWA()" style="color:var(--accent-green); border-color:rgba(16,185,129,0.5);">📲 INSTALL</button>
                <button type="button" class="btn-header" onclick="window.location.reload(true)">🔄</button>
            </div>
        </div>

        <!-- 🤖 PERMANENT ROBOT MODE QUICK-ARM HERO CARD -->
        <div class="robot-hero" id="robot-hero-box">
            <div class="robot-hero-top">
                <span class="robot-title">🤖 ROBOT AUTO-HEALER</span>
                <span class="robot-badge badge-disarmed" id="robot-badge">DISARMED</span>
            </div>
            <div style="font-size:11px; color:var(--text-dim);" id="robot-subtext">
                Monitors LTFT & resets adaptation when lean spikes occur. Zero AI credits.
            </div>
            
            <button type="button" class="btn-robot-toggle btn-robot-arm" id="btn-robot-arm" onclick="toggleRobotMode()">
                🛡️ ARM ROBOT AUTO-TRIM HEALER
            </button>

            <!-- 🎙️ 4-LEVEL SPEECH VERBOSITY SELECTOR -->
            <div class="speech-selector">
                <div class="speech-header">
                    <span>🎙️ Voice Output Level</span>
                    <span id="speech-level-label" style="color:var(--accent-cyan);">MEDIUM</span>
                </div>
                <div class="speech-pills">
                    <button type="button" class="speech-pill" id="sp-mute" onclick="setSpeechLevel('mute')">🔇 MUTE</button>
                    <button type="button" class="speech-pill" id="sp-low" onclick="setSpeechLevel('low')">🔉 LOW</button>
                    <button type="button" class="speech-pill active" id="sp-medium" onclick="setSpeechLevel('medium')">🔊 MED</button>
                    <button type="button" class="speech-pill" id="sp-high" onclick="setSpeechLevel('high')">📢 HIGH</button>
                </div>
            </div>
        </div>

        <!-- 📑 TOP NAVIGATION PILLS -->
        <div class="domain-scroll">
            <a href="/hud" class="domain-pill {'active' if active_tab=='hud' else ''}" id="pill-hud" onclick="return window.switchTab('hud', event)">🚗 Live HUD</a>
            <a href="/robot" class="domain-pill {'active' if active_tab=='robot' else ''}" id="pill-robot" onclick="return window.switchTab('robot', event)">🤖 Robot Guard</a>
            <a href="/blackbox" class="domain-pill {'active' if active_tab=='blackbox' else ''}" id="pill-blackbox" onclick="return window.switchTab('blackbox', event)">📁 Blackbox & Git</a>
            <a href="/swarm" class="domain-pill {'active' if active_tab=='swarm' else ''}" id="pill-swarm" onclick="return window.switchTab('swarm', event)">🎙️ Voice & Swarm</a>
        </div>

        <!-- ==================== TAB 1: 🚗 LIVE HUD & GAUGES ==================== -->
        <div id="sec-hud" style="display: {'block' if active_tab=='hud' else 'none'};">
            <div class="card">
                <div class="card-header">
                    <span>🚗 2013 Chevrolet Malibu ECO (2.4L eAssist)</span>
                    <span id="auto-status" style="color:var(--accent-green);">STANDBY</span>
                </div>
                <div class="metric-grid">
                    <div class="metric-card">
                        <span class="metric-title">Engine Speed</span>
                        <span class="metric-val" id="val-rpm">0<span class="metric-unit">RPM</span></span>
                    </div>
                    <div class="metric-card">
                        <span class="metric-title">Alternator Voltage</span>
                        <span class="metric-val" id="val-volt" style="color:var(--accent-green);">12.6<span class="metric-unit">V</span></span>
                    </div>
                    <div class="metric-card">
                        <span class="metric-title">Short Term Trim</span>
                        <span class="metric-val" id="val-stft">0.0<span class="metric-unit">%</span></span>
                    </div>
                    <div class="metric-card">
                        <span class="metric-title">Long Term Trim</span>
                        <span class="metric-val" id="val-ltft" style="color:var(--accent-red);">0.0<span class="metric-unit">%</span></span>
                    </div>
                    <div class="metric-card">
                        <span class="metric-title">MAF Airflow</span>
                        <span class="metric-val" id="val-maf">0.0<span class="metric-unit">g/s</span></span>
                    </div>
                    <div class="metric-card">
                        <span class="metric-title">Coolant Temp</span>
                        <span class="metric-val" id="val-temp">0<span class="metric-unit">°C</span></span>
                    </div>
                </div>

                <div class="card-header" style="margin-top:4px;">
                    <span>📈 Fuel Trim Waveform (STFT Cyan / LTFT Red)</span>
                    <span style="color:var(--accent-green);">2.5 Hz Polling</span>
                </div>
                <canvas id="liveChart" width="450" height="110"></canvas>
            </div>

            <div class="btn-group">
                <button type="button" class="btn btn-action" onclick="readFuelTrims()">
                    📊 READ FUEL TRIMS (STFT & LTFT)
                </button>
                <button type="button" class="btn btn-action" onclick="resetFuelTrims()">
                    🔄 MANUAL RESET FUEL TRIMS (MODE 04)
                </button>
                <button type="button" class="btn btn-danger" onclick="clearCodes()">
                    🔴 CLEAR CHECK ENGINE LIGHT (MODE 04)
                </button>
            </div>
        </div>

        <!-- ==================== TAB 2: 🤖 ROBOT GUARD EVENT LOG ==================== -->
        <div id="sec-robot" style="display: {'block' if active_tab=='robot' else 'none'};">
            <div class="card">
                <div class="card-header">
                    <span>🤖 Robot Sentinel Configuration</span>
                    <span style="color:var(--accent-cyan);">Zero Token Logic</span>
                </div>
                <div class="metric-grid">
                    <div class="metric-card">
                        <span class="metric-title">Trigger Threshold</span>
                        <span class="metric-val" style="color:var(--accent-amber);">+22.0<span class="metric-unit">%</span></span>
                    </div>
                    <div class="metric-card">
                        <span class="metric-title">Resets Today</span>
                        <span class="metric-val" id="robot-resets-count" style="color:var(--accent-green);">0</span>
                    </div>
                </div>
                <div style="font-size:11px; color:var(--text-dim); line-height:1.5;">
                    • <b>Watchdog Condition</b>: Fires when LTFT $\ge$ +22.0% for 3 cycles.<br>
                    • <b>Action</b>: Sends Mode 04 $\rightarrow$ logs snapshot $\rightarrow$ speaks offline alert.<br>
                    • <b>Interlocks</b>: Engine running (>500 RPM), 75s cooldown between wipes.<br>
                    • <b>Voice Level</b>: Configurable between MUTE, LOW, MEDIUM, and HIGH.
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <span>📋 Recent Auto-Heal Events</span>
                    <button type="button" class="btn-action" style="padding:4px 8px; font-size:10px;" onclick="syncGitLogs()">🔄 SYNC TO GIT</button>
                </div>
                <div id="robot-events-container">
                    <div style="font-size:11px; color:var(--text-dim); text-align:center; padding:12px;">
                        No reset events recorded yet. Robot is ready to guard when armed.
                    </div>
                </div>
            </div>
        </div>

        <!-- ==================== TAB 3: 📁 BLACKBOX & GIT SYNC ==================== -->
        <div id="sec-blackbox" style="display: {'block' if active_tab=='blackbox' else 'none'};">
            <div class="card">
                <div class="card-header">
                    <span>📁 Continuous Flight Recorder</span>
                    <span style="color:var(--accent-green);">2.5 Hz CSV</span>
                </div>
                <div class="metric-card" style="margin-bottom:12px;">
                    <span class="metric-title">Samples Logged to Blackbox</span>
                    <span class="metric-val" id="log-sample-val">0<span class="metric-unit">Samples</span></span>
                </div>
                <div class="btn-group">
                    <a href="/api/download_csv" style="text-decoration:none;">
                        <button type="button" class="btn btn-action" style="width:100%;">
                            📥 DOWNLOAD FULL CSV FLIGHT LOG
                        </button>
                    </a>
                    <button type="button" class="btn btn-action" onclick="syncGitLogs()">
                        🌐 COMMIT & PUSH TO GITHUB (naudiac/utility-scripts)
                    </button>
                </div>
            </div>
        </div>

        <!-- ==================== TAB 4: 🎙️ VOICE & SWARM ==================== -->
        <div id="sec-swarm" style="display: {'block' if active_tab=='swarm' else 'none'};">
            <div class="card">
                <div class="card-header">
                    <span>🧠 Antigravity Voice Co-Pilot & Swarm</span>
                    <span style="color:var(--accent-green);">DUAL LINK</span>
                </div>
                <div class="btn-group">
                    <button type="button" class="btn btn-voice" id="btn-mic" onclick="toggleVoice()">
                        🎙️ TAP TO TALK TO AGY (OFFLINE/ONLINE)
                    </button>
                    <button type="button" class="btn btn-action" onclick="engageHiveMindRun()">
                        🧠 ENGAGE HIVE MIND COLLABORATIVE RUN
                    </button>
                </div>
                <div class="terminal-header">
                    <span>💻 Swarm Intelligence Console</span>
                </div>
                <div class="terminal-box" id="swarm-term">[MALIBU ROBOT & NEXUS OS READY]:
• Autonomous Trim Sentinel ready.
• Tap "ARM ROBOT AUTO-TRIM HEALER" to enable protection during your drive.
• Speech Selector: MUTE, LOW, MEDIUM, or HIGH.
• Tap "INSTALL" at top right to add to your phone's Home Screen!</div>
            </div>
        </div>
    </div>

    <!-- 📱 NATIVE FIXED BOTTOM DOCK -->
    <div class="bottom-dock">
        <a href="/hud" class="dock-item {'active' if active_tab=='hud' else ''}" id="dock-hud" onclick="return window.switchTab('hud', event)">
            <span class="icon">🚗</span>
            <span>Live HUD</span>
        </a>
        <a href="/robot" class="dock-item {'active' if active_tab=='robot' else ''}" id="dock-robot" onclick="return window.switchTab('robot', event)">
            <span class="icon">🤖</span>
            <span>Robot Mode</span>
        </a>
        <a href="/blackbox" class="dock-item {'active' if active_tab=='blackbox' else ''}" id="dock-blackbox" onclick="return window.switchTab('blackbox', event)">
            <span class="icon">📁</span>
            <span>Blackbox</span>
        </a>
        <a href="/swarm" class="dock-item {'active' if active_tab=='swarm' else ''}" id="dock-swarm" onclick="return window.switchTab('swarm', event)">
            <span class="icon">🎙️</span>
            <span>Voice</span>
        </a>
    </div>

    <script>
        const canvas = document.getElementById('liveChart');
        const ctx = canvas.getContext('2d');

        function logToTerm(text) {{
            const term = document.getElementById('swarm-term');
            if(term) {{
                term.innerHTML += '\\n' + text;
                term.scrollTop = term.scrollHeight;
            }}
        }}

        async function updateData() {{
            try {{
                const res = await fetch('/api/live');
                const data = await res.json();
                
                if(data.is_connected) {{
                    document.getElementById('auto-status').innerText = 'LIVE';
                    document.getElementById('val-rpm').innerHTML = Math.round(data.rpm) + '<span class="metric-unit">RPM</span>';
                    document.getElementById('val-volt').innerHTML = data.volt.toFixed(1) + '<span class="metric-unit">V</span>';
                    document.getElementById('val-stft').innerHTML = (data.stft > 0 ? '+' : '') + data.stft.toFixed(1) + '<span class="metric-unit">%</span>';
                    document.getElementById('val-ltft').innerHTML = (data.ltft > 0 ? '+' : '') + data.ltft.toFixed(1) + '<span class="metric-unit">%</span>';
                    document.getElementById('val-maf').innerHTML = data.maf.toFixed(1) + '<span class="metric-unit">g/s</span>';
                    document.getElementById('val-temp').innerHTML = data.temp + '<span class="metric-unit">°C</span>';
                    document.getElementById('val-ltft').style.color = data.ltft > 15 ? '#ef4444' : '#10b981';
                }}
                document.getElementById('log-sample-val').innerHTML = data.samples_logged + '<span class="metric-unit">Samples</span>';
            }} catch(e) {{}}

            try {{
                const rRes = await fetch('/api/robot/status');
                const rData = await rRes.json();
                const hero = document.getElementById('robot-hero-box');
                const badge = document.getElementById('robot-badge');
                const subtext = document.getElementById('robot-subtext');
                const btn = document.getElementById('btn-robot-arm');
                const rCount = document.getElementById('robot-resets-count');
                const spLabel = document.getElementById('speech-level-label');

                if (rCount) rCount.innerText = rData.resets_today;
                if (spLabel) spLabel.innerText = (rData.speech_level || 'medium').toUpperCase();

                // Update Speech Pills
                const levels = ['mute', 'low', 'medium', 'high'];
                levels.forEach(lvl => {{
                    const el = document.getElementById('sp-' + lvl);
                    if (el) {{
                        if (rData.speech_level === lvl) el.classList.add('active');
                        else el.classList.remove('active');
                    }}
                }});

                if(rData.armed) {{
                    hero.classList.add('armed');
                    badge.className = 'robot-badge badge-armed';
                    badge.innerText = 'ARMED • ACTIVE';
                    subtext.innerHTML = '<span style="color:var(--accent-cyan); font-weight:bold;">⚡ WATCHDOG ACTIVE:</span> ' + rData.status_message;
                    btn.className = 'btn-robot-toggle btn-robot-disarm';
                    btn.innerHTML = '🛑 DISARM ROBOT SENTINEL';
                }} else {{
                    hero.classList.remove('armed');
                    badge.className = 'robot-badge badge-disarmed';
                    badge.innerText = 'DISARMED';
                    subtext.innerText = 'Monitors LTFT & resets adaptation when lean spikes occur. Zero AI credits.';
                    btn.className = 'btn-robot-toggle btn-robot-arm';
                    btn.innerHTML = '🛡️ ARM ROBOT AUTO-TRIM HEALER';
                }}

                if (rData.recent_events && rData.recent_events.length > 0) {{
                    let html = '<table class="event-table"><tr><th>Time</th><th>Reason</th><th>LTFT</th><th>RPM</th></tr>';
                    rData.recent_events.slice(0, 5).forEach(ev => {{
                        html += `<tr><td>${{ev.timestamp.split(' ')[1]}}</td><td style="color:var(--accent-amber);">${{ev.trigger_reason.split(' ')[0]}}</td><td style="color:var(--accent-red);">+${{ev.ltft_pct}}%</td><td>${{Math.round(ev.rpm)}}</td></tr>`;
                    }});
                    html += '</table>';
                    document.getElementById('robot-events-container').innerHTML = html;
                }}
            }} catch(e) {{}}
        }}

        async function drawChart() {{
            try {{
                const secHud = document.getElementById('sec-hud');
                if (secHud && secHud.style.display === 'none') return;

                const res = await fetch('/api/history');
                const history = await res.json();
                if(!history || history.length < 2) return;

                ctx.clearRect(0, 0, canvas.width, canvas.height);
                const midY = canvas.height / 2;
                ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 1; ctx.beginPath();
                ctx.moveTo(0, midY); ctx.lineTo(canvas.width, midY); ctx.stroke();

                const step = canvas.width / (history.length - 1);
                ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 2; ctx.beginPath();
                history.forEach((pt, i) => {{
                    const y = midY - (pt.ltft * 1.5);
                    if(i === 0) ctx.moveTo(0, y); else ctx.lineTo(i * step, y);
                }});
                ctx.stroke();

                ctx.strokeStyle = '#00f2fe'; ctx.lineWidth = 1.5; ctx.beginPath();
                history.forEach((pt, i) => {{
                    const y = midY - (pt.stft * 1.5);
                    if(i === 0) ctx.moveTo(0, y); else ctx.lineTo(i * step, y);
                }});
                ctx.stroke();
            }} catch(e) {{}}
        }}

        setInterval(updateData, 400);
        setInterval(drawChart, 600);

        function speakPhone(text) {
            try {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    const u = new SpeechSynthesisUtterance(text);
                    u.rate = 1.0;
                    u.pitch = 1.0;
                    u.volume = 1.0;
                    window.speechSynthesis.speak(u);
                }
            } catch(e) {}
        }

        async function toggleRobotMode() {
            try {
                const res = await fetch('/api/robot/toggle', { method: 'POST' });
                const data = await res.json();
                updateData();
                speakPhone(data.armed ? 'Robot Mode armed. Malibu fuel trim watchdog active.' : 'Robot Mode disarmed. Watchdog stopped.');
            } catch(e) { alert('Error toggling robot mode: ' + e); }
        }

        async function setSpeechLevel(lvl) {
            try {
                const res = await fetch('/api/robot/speech_level', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ level: lvl })
                });
                updateData();
                speakPhone('Voice level set to ' + lvl);
            } catch(e) { alert('Error setting speech level: ' + e); }
        }

        async function syncGitLogs() {
            logToTerm('\n🔄 [GIT SYNC]: Syncing reset events to GitHub naudiac/utility-scripts...');
            speakPhone('Syncing reset logs to GitHub.');
            try {
                const res = await fetch('/api/git/sync', { method: 'POST' });
                const data = await res.json();
                alert(data.message || 'Git sync dispatched!');
                logToTerm('✓ [GIT SYNC COMPLETE]: ' + (data.message || 'Updated'));
            } catch(e) { alert('Git sync error: ' + e); }
        }

        async function readFuelTrims() {
            try {
                const res = await fetch('/api/live');
                const data = await res.json();
                const total = (data.stft + data.ltft).toFixed(1);
                const health = data.ltft > 20 ? 'High Idle Trim, Post MAF Leak Detected' : 'Normal Fuel Delivery';
                speakPhone('Short term trim is ' + data.stft.toFixed(1) + ' percent. Long term trim is ' + data.ltft.toFixed(1) + ' percent.');
                alert('📊 LIVE FUEL TRIMS:\n• STFT: ' + (data.stft > 0 ? '+' : '') + data.stft.toFixed(1) + '%\n• LTFT: ' + (data.ltft > 0 ? '+' : '') + data.ltft.toFixed(1) + '%\n• Total: ' + (total > 0 ? '+' : '') + total + '%\n• Health: ' + health);
            } catch(e) { alert('Error: ' + e); }
        }

        async function resetFuelTrims() {
            if(!confirm('Wipe learned Fuel Trim adaptation tables & clear DTCs?')) return;
            speakPhone('Wiping fuel trim adaptation tables to zero percent.');
            const res = await fetch('/obd/clear', {method: 'POST'});
            const data = await res.json();
            alert('Fuel Trims Cleared to 0.0% (Mode 04 Dispatched)');
        }

        async function clearCodes() {
            if(!confirm('Send Mode 04 to Clear Diagnostic Trouble Codes?')) return;
            speakPhone('Sending Mode 04 to clear diagnostic trouble codes.');
            const res = await fetch('/obd/clear', {method: 'POST'});
            const data = await res.json();
            alert('Mode 04 Dispatched: ' + (data.response || 'Success'));
        }

        async function engageHiveMindRun() {{
            logToTerm('\\n🚀 [HIVE MIND]: Relaying to Node Alpha Master over Tailscale...');
            try {{
                const res = await fetch('/api/hive_run', {{ method: 'POST' }});
                const data = await res.json();
                logToTerm('• Master Hub debrief received: ' + data.summary);
            }} catch(e) {{ logToTerm('[-] Swarm relay error: ' + e); }}
        }}

        // 🎙️ WEB SPEECH
        let recognition = null;
        let isRecording = false;

        function toggleVoice() {{
            const btn = document.getElementById('btn-mic');
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            if(!SpeechRec) {{ alert('Speech API not supported.'); return; }}

            if(isRecording) {{
                recognition.stop();
                isRecording = false;
                btn.innerHTML = '🎙️ TAP TO TALK TO AGY (OFFLINE/ONLINE)';
                return;
            }}

            recognition = new SpeechRec();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onstart = () => {{
                isRecording = true;
                btn.innerHTML = '🔴 LISTENING... (SPEAK NOW)';
            }};

            recognition.onresult = (event) => {{
                const transcript = event.results[0][0].transcript;
                executePrompt(transcript);
            }};

            recognition.onerror = () => {{ isRecording = false; btn.innerHTML = '🎙️ TAP TO TALK TO AGY'; }};
            recognition.onend = () => {{ isRecording = false; }};
            recognition.start();
        }}

        async function executePrompt(prompt) {{
            logToTerm('🗣️ [YOU]: ' + prompt);
            try {{
                const res = await fetch('/api/ask', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{prompt: prompt}})
                }});
                const data = await res.json();
                logToTerm('🤖 [AGY]: ' + data.reply);
            }} catch(e) {{ logToTerm('[-] Error: ' + e); }}
        }}
    </script>
</body>
</html>
"""

class RobotNexusHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _send_html(self, status_code: int, html: str):
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _send_svg(self, status_code: int, svg_content: str):
        self.send_response(status_code)
        self.send_header("Content-Type", "image/svg+xml")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "public, max-age=86400")
        self.end_headers()
        self.wfile.write(svg_content.encode("utf-8"))

    def _send_js(self, status_code: int, js_content: str):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/javascript")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "public, max-age=86400")
        self.end_headers()
        self.wfile.write(js_content.encode("utf-8"))

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/manifest.json":
            self._send_json(200, MANIFEST_JSON)

        elif parsed.path == "/icon.svg":
            self._send_svg(200, ICON_SVG)

        elif parsed.path == "/sw.js":
            self._send_js(200, SERVICE_WORKER_JS)

        elif parsed.path == "/" or parsed.path == "/hud" or parsed.path == "/dashboard":
            self._send_html(200, generate_dashboard_html("hud"))

        elif parsed.path == "/robot":
            self._send_html(200, generate_dashboard_html("robot"))

        elif parsed.path == "/blackbox" or parsed.path == "/logs":
            self._send_html(200, generate_dashboard_html("blackbox"))

        elif parsed.path == "/swarm" or parsed.path == "/voice":
            self._send_html(200, generate_dashboard_html("swarm"))

        elif parsed.path == "/api/live":
            with telemetry_lock:
                self._send_json(200, live_state)

        elif parsed.path == "/api/robot/status":
            with telemetry_lock:
                self._send_json(200, robot_state)

        elif parsed.path == "/api/history":
            with telemetry_lock:
                self._send_json(200, history_buffer)

        elif parsed.path == "/api/download_csv":
            if os.path.exists(LOG_FILE):
                self.send_response(200)
                self.send_header("Content-Type", "text/csv")
                self.send_header("Content-Disposition", "attachment; filename=malibu_flight_log.csv")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                with open(LOG_FILE, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self._send_json(404, {"error": "Log file not found"})

        elif parsed.path == "/health":
            self._send_json(200, {"status": "ONLINE", "robot_armed": robot_state["armed"]})

        else:
            self._send_json(404, {"error": "Not Found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b"{}"

        try:
            req_data = json.loads(post_body.decode("utf-8"))
        except Exception:
            req_data = {}

        if parsed.path == "/api/robot/toggle":
            with telemetry_lock:
                robot_state["armed"] = not robot_state["armed"]
                if robot_state["armed"]:
                    robot_state["status_message"] = "ARMED (Active Watchdog • Monitoring Trims)"
                    speak_offline("Robot Mode armed. Malibu fuel trim watchdog active.", required_level="medium")
                else:
                    robot_state["status_message"] = "DISARMED (Idle • Zero Commands Sent)"
                    speak_offline("Robot Mode disarmed. Watchdog stopped.", required_level="medium")
            self._send_json(200, robot_state)

        elif parsed.path == "/api/robot/speech_level":
            new_lvl = req_data.get("level", "medium").lower()
            if new_lvl in SPEECH_LEVELS_MAP:
                with telemetry_lock:
                    robot_state["speech_level"] = new_lvl
                if new_lvl != "mute":
                    speak_offline(f"Voice output set to {new_lvl}.", required_level="low")
                self._send_json(200, {"success": True, "speech_level": new_lvl})
            else:
                self._send_json(400, {"error": "Invalid speech level. Options: mute, low, medium, high"})

        elif parsed.path == "/api/git/sync":
            def _push_git():
                try:
                    repo_dir = "/data/data/com.termux/files/home/utility-scripts"
                    if not os.path.exists(repo_dir):
                        subprocess.run(f"git clone https://github.com/naudiac/utility-scripts.git {repo_dir}", shell=True)
                    
                    target_log_dir = os.path.join(repo_dir, "chevy_malibu_trim_sentinel", "logs")
                    os.makedirs(target_log_dir, exist_ok=True)
                    subprocess.run(f"cp {ROBOT_LOG_FILE} {target_log_dir}/ 2>/dev/null", shell=True)
                    subprocess.run(f"cp {LOG_FILE} {target_log_dir}/ 2>/dev/null", shell=True)
                    
                    cmd = f"cd {repo_dir} && git add . && git commit -m 'Auto-sync Malibu Robot Trim logs [$(date)]' && git push origin main"
                    subprocess.run(cmd, shell=True)
                except Exception as e:
                    print(f"Git push error: {e}")

            t = threading.Thread(target=_push_git, daemon=True)
            t.start()
            self._send_json(200, {"success": True, "message": "Synchronizing reset logs to GitHub naudiac/utility-scripts..."})

        elif parsed.path == "/api/ask":
            prompt = req_data.get("prompt", "")
            try:
                agy_cmd = [
                    "/data/data/com.termux/files/usr/bin/agy",
                    "-p", f"You are William's in-car AI co-pilot. Keep reply direct (1-2 sentences). William asked: {prompt}",
                    "--output-format", "text",
                    "--dangerously-skip-permissions"
                ]
                res = subprocess.run(agy_cmd, capture_output=True, text=True, timeout=25)
                reply = res.stdout.strip() or "Command received."
                speak_offline(reply, required_level="low")
                self._send_json(200, {"success": True, "reply": reply})
            except Exception as e:
                self._send_json(200, {"success": False, "reply": f"Error: {e}"})

        elif parsed.path == "/api/hive_run":
            speak_offline("Node Beta initiating joint hive mind sync with Node Alpha over Tailscale.", required_level="medium")
            time.sleep(4.5)
            pc_response = None
            try:
                pc_url = f"http://{PC_MASTER_IP}:{PC_MASTER_PORT}/api/hive/run"
                payload = json.dumps({
                    "node": "beta",
                    "rpm": live_state["rpm"],
                    "stft": live_state["stft"],
                    "ltft": live_state["ltft"],
                    "volt": live_state["volt"]
                }).encode("utf-8")
                req = urllib.request.Request(pc_url, data=payload, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=6.0) as resp:
                    pc_response = json.loads(resp.read().decode("utf-8"))
            except Exception as e:
                pc_response = {"error": str(e)}

            self._send_json(200, {
                "success": True,
                "summary": "Swarm synchronized across Tailscale mesh.",
                "pc_response": pc_response
            })

        elif parsed.path == "/obd/send" or parsed.path == "/obd/clear":
            cmd = req_data.get("command", "04")
            req_id = str(time.time())
            command_queue.put((req_id, cmd))
            
            start_w = time.time()
            resp_val = None
            while time.time() - start_w < 3.0:
                with telemetry_lock:
                    if req_id in command_results:
                        resp_val = command_results.pop(req_id)
                        break
                time.sleep(0.05)
            
            if resp_val is not None:
                self._send_json(200, {"success": True, "command": cmd, "response": resp_val})
            else:
                self._send_json(200, {"success": False, "command": cmd, "error": "Command timeout in queue"})
        else:
            self._send_json(404, {"error": "Not Found"})

def run_server():
    poller = threading.Thread(target=background_telemetry_poller, daemon=True)
    poller.start()

    server = HTTPServer((HOST, HTTP_PORT), RobotNexusHandler)
    print(f"🚀 [ANTIGRAVITY MALIBU ROBOT PWA V23 ONLINE]: http://{HOST}:{HTTP_PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

if __name__ == "__main__":
    run_server()
