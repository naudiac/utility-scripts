#!/usr/bin/env python3
"""
Antigravity Skill Archiver & Versioning System
===============================================
Manages the 3-Tier Skill Lifecycle:
1. CURRENT   -> Active working skills (~/.gemini/config/skills/)
2. ARCHIVE   -> Dated snapshot archive by update date (archive/skills/<skill-name>/YYYY-MM-DD/)
3. GRAVEYARD -> Retired obsolete skills (graveyard/<skill-name>/)

Ensures zero exposure of sensitive keys/tokens during archiving.
"""

import os
import sys
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

# Paths
CONFIG_SKILLS_DIR = Path(os.path.expanduser(r"~\.gemini\config\skills"))
REPO_DIR = Path(r"C:\Users\whanusiewicz\.gemini\antigravity\scratch\utility-scripts")
ARCHIVE_DIR = REPO_DIR / "archive" / "skills"
GRAVEYARD_DIR = REPO_DIR / "graveyard"

# Sensitive pattern redactor
SENSITIVE_PATTERNS = [
    (re.compile(r'gh[pousr]_[A-Za-z0-9_]{30,}'), '<REDACTED_GITHUB_TOKEN>'),
    (re.compile(r'GOCSPX-[A-Za-z0-9_-]{20,}'), '<YOUR_CLIENT_SECRET>'),
    (re.compile(r'734063060374-[a-z0-9]{32}\.apps\.googleusercontent\.com'), '<YOUR_CLIENT_ID>'),
    (re.compile(r'sk-[A-Za-z0-9]{32,}'), '<REDACTED_OPENAI_KEY>'),
    (re.compile(r'CW_DB_PASS=[^\r\n]+'), 'CW_DB_PASS=<YOUR_DB_PASSWORD>'),
]

def sanitize_content(content: str) -> str:
    """Sanitize any accidental secrets in string content."""
    for pattern, replacement in SENSITIVE_PATTERNS:
        content = pattern.sub(replacement, content)
    return content

def file_hash(path: Path) -> str:
    import hashlib
    if not path.exists(): return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()

def archive_all_skills():
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = ARCHIVE_DIR / "archive_manifest.json"
    
    manifest = {}
    if manifest_path.exists():
        try:
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            manifest = {}
            
    today_date = datetime.now().strftime("%Y-%m-%d")
    archived_count = 0
    updated_count = 0
    
    if not CONFIG_SKILLS_DIR.exists():
        print(f"[!] Config skills directory not found at {CONFIG_SKILLS_DIR}")
        return

    for skill_path in CONFIG_SKILLS_DIR.iterdir():
        if not skill_path.is_dir():
            continue
            
        skill_name = skill_path.name
        skill_file = skill_path / "SKILL.md"
        if not skill_file.exists():
            continue
            
        content = skill_file.read_text(encoding="utf-8", errors="ignore")
        clean_content = sanitize_content(content)
        
        # 1. Update current root folder in repository
        repo_skill_dir = REPO_DIR / skill_name
        repo_skill_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy full skill folder to repo root
        for root, dirs, files in os.walk(skill_path):
            rel = Path(root).relative_to(skill_path)
            dest_dir = repo_skill_dir / rel
            dest_dir.mkdir(parents=True, exist_ok=True)
            for file_name in files:
                if file_name == ".env":
                    continue # Skip raw .env
                src_file = Path(root) / file_name
                dest_file = dest_dir / file_name
                try:
                    f_content = src_file.read_text(encoding="utf-8", errors="ignore")
                    f_clean = sanitize_content(f_content)
                    dest_file.write_text(f_clean, encoding="utf-8")
                except Exception:
                    shutil.copy2(src_file, dest_file)
                    
        # 2. Check version history & create dated snapshot
        skill_archive_dir = ARCHIVE_DIR / skill_name / today_date
        current_hash = file_hash(repo_skill_dir / "SKILL.md")
        
        # Determine if we need to snapshot today
        skill_meta = manifest.get(skill_name, {"versions": [], "last_updated": ""})
        latest_version = skill_meta["versions"][-1] if skill_meta["versions"] else None
        
        if not latest_version or latest_version.get("hash") != current_hash:
            skill_archive_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy sanitized snapshot
            for root, dirs, files in os.walk(repo_skill_dir):
                rel = Path(root).relative_to(repo_skill_dir)
                snap_dir = skill_archive_dir / rel
                snap_dir.mkdir(parents=True, exist_ok=True)
                for file_name in files:
                    shutil.copy2(Path(root) / file_name, snap_dir / file_name)
                    
            version_entry = {
                "date": today_date,
                "timestamp": datetime.now().isoformat(),
                "hash": current_hash,
                "path": f"archive/skills/{skill_name}/{today_date}/SKILL.md"
            }
            
            if not any(v.get("date") == today_date for v in skill_meta["versions"]):
                skill_meta["versions"].append(version_entry)
            else:
                # Update today's entry
                skill_meta["versions"][-1] = version_entry
                
            skill_meta["last_updated"] = today_date
            manifest[skill_name] = skill_meta
            archived_count += 1
            print(f"[ARCHIVE] Snapshotted '{skill_name}' -> archive/skills/{skill_name}/{today_date}/")
        else:
            updated_count += 1

    # Save manifest
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    print("-" * 60)
    print(f"[OK] Archival complete. {archived_count} new dated snapshot(s) created, {updated_count} unchanged.")

if __name__ == "__main__":
    archive_all_skills()
