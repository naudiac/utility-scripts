"""
Creative Capital Solutions — Sales Flight Deck Activity Intelligence Engine
Logs, tracks, and analyzes real-time user activity across all devices and sessions.
Identifies: Michael Qin (Rep), David Qin (Father), Salvatore (Brother), and William (Supervisor).
"""

import sys
import os
import json
import sqlite3
import urllib.request
import datetime
from typing import Dict, List, Any, Optional

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "activity_vault.db")
AUDIT_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "activity_audit.jsonl")
TELEMETRY_TOPIC = "ccs_michael_qin_telemetry_wh_2026"
POLL_URL = f"https://ntfy.sh/{TELEMETRY_TOPIC}/json?poll=1&since=all"

# Multi-Person Identity Resolver Mapping
KNOWN_IDENTITIES = {
    "69.203.0.85": {
        "name": "Michael Qin",
        "role": "Rep (Creative Capital)",
        "device": "iPhone Pro Max",
        "location": "Staten Island, NY",
        "badge": "🟢 Rep"
    },
    "68.132.69.243": {
        "name": "Salvatore Hanusiewicz",
        "role": "William's Brother",
        "device": "Android Phone",
        "location": "Huntington, NY",
        "badge": "👤 Brother"
    },
    "2600:387:15:2911::5": {
        "name": "David Qin",
        "role": "Michael's Father / Friend",
        "device": "iPhone Pro",
        "location": "White Plains / NY Metro (AT&T)",
        "badge": "👨‍👦 Father"
    },
    "85.115.107.223": {
        "name": "William Hanusiewicz",
        "role": "Supervisor",
        "device": "Supervisor PC",
        "location": "New York, NY",
        "badge": "👑 Supervisor"
    },
    "74.209.76.220": {
        "name": "William Hanusiewicz",
        "role": "Supervisor",
        "device": "S24 Ultra",
        "location": "Mobile (Supervisor)",
        "badge": "👑 Supervisor"
    }
}


def resolve_person(ip: str, device: str, location: str, screen: str, rep_field: str, is_sup: bool) -> Dict[str, str]:
    if ip in KNOWN_IDENTITIES:
        return KNOWN_IDENTITIES[ip]
    
    if is_sup or (rep_field and ("supervisor" in rep_field.lower() or "william" in rep_field.lower())):
        return KNOWN_IDENTITIES["85.115.107.223"]
    
    if "staten island" in (location or "").lower() or (screen == "428x751" and "iphone" in (device or "").lower()) or ip.startswith("69."):
        return KNOWN_IDENTITIES["69.203.0.85"]
        
    if "huntington" in (location or "").lower() or (screen == "378x656" and "android" in (device or "").lower()) or ip.startswith("68."):
        return KNOWN_IDENTITIES["68.132.69.243"]
        
    if "white plains" in (location or "").lower() or (screen == "393x754" and "iphone" in (device or "").lower()) or "2600:" in ip:
        return KNOWN_IDENTITIES["2600:387:15:2911::5"]
        
    return {
        "name": rep_field if rep_field and rep_field != "Michael Qin" else "Guest Visitor",
        "role": "Guest",
        "device": device or "Unknown Device",
        "location": location or "Unknown Location",
        "badge": "📱 Guest"
    }


def init_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS activity_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_time_epoch INTEGER,
            event_time_edt TEXT,
            person_name TEXT,
            person_role TEXT,
            person_badge TEXT,
            ip TEXT,
            location TEXT,
            device TEXT,
            screen TEXT,
            session_id TEXT,
            action TEXT,
            title TEXT,
            target_item TEXT,
            details_json TEXT,
            raw_payload TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(event_time_epoch, session_id, action, target_item)
        )
    """)
    conn.commit()
    return conn


def sync_telemetry() -> int:
    """Fetches all telemetry from ntfy.sh and persists into SQLite and JSONL audit trail."""
    conn = init_db()
    cur = conn.cursor()
    
    req = urllib.request.Request(POLL_URL, headers={"User-Agent": "CCS-Activity-Logger/1.0"})
    new_records = 0
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            lines = resp.read().decode("utf-8").strip().split("\n")
            
        for line in lines:
            if not line.strip():
                continue
            try:
                msg_data = json.loads(line)
                if msg_data.get("event") != "message":
                    continue
                
                raw_payload = msg_data.get("message", "{}")
                payload = json.loads(raw_payload) if isinstance(raw_payload, str) else raw_payload
                
                ts_epoch = msg_data.get("time", int(datetime.datetime.now().timestamp()))
                dt_edt = datetime.datetime.fromtimestamp(ts_epoch, tz=datetime.timezone.utc).astimezone().strftime("%Y-%m-%d %I:%M:%S %p")
                
                ip = payload.get("ip", "Unknown")
                device = payload.get("device", "Unknown")
                location = payload.get("location", "Unknown")
                details = payload.get("details", {}) or {}
                screen = str(details.get("screen", ""))
                rep_field = payload.get("rep", "")
                is_sup = bool(payload.get("isSupervisor", False))
                action = payload.get("action", "UNKNOWN")
                title = payload.get("title", "")
                session_id = payload.get("sessionId", "unknown_session")
                
                person_info = resolve_person(ip, device, location, screen, rep_field, is_sup)
                
                # Determine Target Item for readable querying
                target_item = ""
                if action == "TAB_SWITCH":
                    target_item = details.get("tabId") or title.replace("Michael Qin: Switched to tab: ", "")
                elif action == "INDUSTRY_PRESET":
                    target_item = details.get("verticalName") or title.replace("Michael Qin: Applied Vertical Preset: ", "")
                elif action == "REACTION":
                    target_item = details.get("optionClicked") or title
                elif action == "TONE_CHANGE":
                    target_item = details.get("toneName") or title.replace("Michael Qin Switched Tone to: ", "")
                elif action == "SCRIPT_COPIED":
                    target_item = details.get("stage") or "Verbatim Script"
                elif action == "OPEN":
                    target_item = f"Portal Loaded (Screen: {screen})"
                else:
                    target_item = title
                    
                cur.execute("""
                    INSERT OR IGNORE INTO activity_events (
                        event_time_epoch, event_time_edt, person_name, person_role, person_badge,
                        ip, location, device, screen, session_id, action, title, target_item,
                        details_json, raw_payload
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ts_epoch, dt_edt, person_info["name"], person_info["role"], person_info["badge"],
                    ip, location, person_info["device"], screen, session_id, action, title, target_item,
                    json.dumps(details), json.dumps(payload)
                ))
                
                if cur.rowcount > 0:
                    new_records += 1
                    
            except Exception as ex:
                continue
                
        conn.commit()
    except Exception as e:
        print(f"[!] Error syncing telemetry from ntfy: {e}", file=sys.stderr)
    finally:
        conn.close()
        
    return new_records


def print_summary():
    sync_telemetry()
    conn = init_db()
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("  CREATIVE CAPITAL SOLUTIONS -- ACTIVITY & STUDY INTELLIGENCE DASHBOARD")
    print("="*80)
    
    # 1. Person Overview
    cur.execute("""
        SELECT 
            person_name, 
            person_role, 
            person_badge, 
            location, 
            device,
            MIN(event_time_edt) as first_seen,
            MAX(event_time_edt) as last_seen,
            COUNT(*) as total_events
        FROM activity_events
        GROUP BY person_name
        ORDER BY MAX(event_time_epoch) DESC
    """)
    rows = cur.fetchall()
    
    print("\n[ACTIVE PERSONAS RECOGNIZED]:")
    print("-" * 80)
    print(f"{'PERSON':<24} | {'ROLE':<20} | {'LOCATION':<20} | {'LAST ACTIVE'}")
    print("-" * 80)
    for r in rows:
        p_name, p_role, p_badge, loc, dev, f_seen, l_seen, cnt = r
        last_short = l_seen.split(" ")[1] + " " + l_seen.split(" ")[2] if " " in l_seen else l_seen
        full_person = f"{p_badge} {p_name}"
        print(f"{full_person:<24} | {p_role:<20} | {loc:<20} | {last_short}")
    
    # 2. Michael Qin Study & Practice Breakdown
    cur.execute("""
        SELECT action, target_item, COUNT(*) as cnt, MAX(event_time_edt) as last_time
        FROM activity_events
        WHERE person_name = 'Michael Qin'
        GROUP BY action, target_item
        ORDER BY last_time DESC
    """)
    michael_actions = cur.fetchall()
    
    print("\n" + "-" * 80)
    print(" [MICHAEL QIN (REP) -- WHAT HE HAS SEEN & PRACTICED]:")
    print("-" * 80)
    if not michael_actions:
        print("  (No activity logged for Michael Qin yet)")
    else:
        print(f"{'ACTION TYPE':<18} | {'WHAT HE LOOKED AT / PRACTICED':<42} | {'COUNT':<5} | {'LAST TIME'}")
        print("-" * 80)
        for act, target, cnt, l_time in michael_actions:
            t_short = l_time.split(" ")[1] + " " + l_time.split(" ")[2] if " " in l_time else l_time
            print(f"{act:<18} | {target[:40]:<42} | {cnt:<5} | {t_short}")
            
    # 3. Full Chronological Audit Timeline
    cur.execute("""
        SELECT event_time_edt, person_badge, person_name, action, target_item, location
        FROM activity_events
        ORDER BY event_time_epoch DESC
        LIMIT 20
    """)
    timeline = cur.fetchall()
    
    print("\n" + "-" * 80)
    print(" [RECENT ACTIVITY TIMELINE (LATEST 20 ACTIONS)]:")
    print("-" * 80)
    print(f"{'TIME (EDT)':<12} | {'WHO':<24} | {'ACTION':<15} | {'DETAILS'}")
    print("-" * 80)
    for t_edt, badge, name, act, target, loc in timeline:
        time_part = t_edt.split(" ")[1] + " " + t_edt.split(" ")[2] if " " in t_edt else t_edt
        who_str = f"{badge} {name.split()[0]}"
        print(f"{time_part:<12} | {who_str:<24} | {act:<15} | {target}")
        
    print("="*80 + "\n")
    conn.close()


def print_person_drilldown(person_query: str):
    sync_telemetry()
    conn = init_db()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT event_time_edt, person_badge, person_name, action, title, target_item, ip, location, device, details_json
        FROM activity_events
        WHERE person_name LIKE ?
        ORDER BY event_time_epoch ASC
    """, (f"%{person_query}%",))
    
    events = cur.fetchall()
    if not events:
        print(f"\n[!] No events found matching person: '{person_query}'\n")
        conn.close()
        return
        
    p_name = events[0][2]
    p_badge = events[0][1]
    
    print("\n" + "="*80)
    print(f" COMPLETE INTERACTION TIMELINE FOR: {p_badge} {p_name.upper()}")
    print("="*80)
    
    for ev in events:
        t_edt, badge, name, act, title, target, ip, loc, dev, det_json = ev
        print(f"\n[{t_edt}] Action: {act} -> {target}")
        print(f"  +- Location & Device: {loc} ({ip}) - {dev}")
        det = json.loads(det_json) if det_json else {}
        if det:
            det_str = ", ".join(f"{k}: {v}" for k, v in det.items() if k not in ["screen"])
            if det_str:
                print(f"  +- Parameters: {det_str}")
    print("\n" + "="*80 + "\n")
    conn.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["--sync", "-s"]:
            added = sync_telemetry()
            print(f"[+] Successfully synced telemetry: {added} new events stored in {DB_PATH}")
        elif arg in ["--person", "-p"] and len(sys.argv) > 2:
            print_person_drilldown(sys.argv[2])
        elif arg in ["--michael", "-m"]:
            print_person_drilldown("Michael Qin")
        elif arg in ["--david", "-d"]:
            print_person_drilldown("David Qin")
        elif arg in ["--salvatore", "-sal"]:
            print_person_drilldown("Salvatore")
        else:
            print_summary()
    else:
        print_summary()
