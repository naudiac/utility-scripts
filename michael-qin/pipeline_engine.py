#!/usr/bin/env python3
"""
Antigravity IDE - Michael Qin's Merchant Statement & Sales Mastery Flight Deck
Balanced Twilight Slate Edition (Zero Glare, Easy on the Eyes) + 1-Click Theme Switcher.
"""

import os
import sys
import json
import subprocess
import shutil
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class PipelineStage:
    number: int
    title: str
    phase_name: str
    objective: str
    duration: str
    key_actions: List[str]
    scripts_and_templates: Dict[str, str]
    metrics_and_kpis: List[str]
    common_pitfalls: List[str]


@dataclass
class ObjectionHandler:
    objection: str
    trigger_stage: str
    rebuttal_script: str
    tactical_principle: str


@dataclass
class SalesPipelineSystem:
    rep_name: str = "Michael Qin"
    title: str = "Merchant Statement & Sales Mastery Flight Deck"
    industry: str = "Commercial Debt Placement & Working Capital Advisory"
    core_thesis: str = "Dismantle merchant hesitation, extract bank statements on-call, and unlock maximum debt savings using proven Wall Street negotiation psychology."
    stages: List[PipelineStage] = field(default_factory=list)
    objections: List[ObjectionHandler] = field(default_factory=list)

    def render_portal_html(self) -> str:
        stages_json = json.dumps([{
            "number": s.number,
            "title": s.title,
            "phase": s.phase_name,
            "objective": s.objective,
            "duration": s.duration,
            "actions": s.key_actions,
            "scripts": s.scripts_and_templates,
            "metrics": s.metrics_and_kpis,
            "pitfalls": s.common_pitfalls
        } for s in self.stages])

        objections_json = json.dumps([{
            "objection": o.objection,
            "stage": o.trigger_stage,
            "rebuttal": o.rebuttal_script,
            "principle": o.tactical_principle
        } for o in self.objections])

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>{self.rep_name} | Sales Flight Deck</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;700;800&display=swap" rel="stylesheet">
<style>
    /* Default: Twilight Slate Theme (Balanced, soothing, zero-glare) */
    :root {{
        --bg-base: #131720;
        --bg-surface: #1a202c;
        --bg-card: #222938;
        --bg-input: #0f131a;
        
        --border: #2d3748;
        --border-light: #3f4d66;
        --border-focus: #38bdf8;

        --text-heading: #f8fafc;
        --text-body: #cbd5e1;
        --text-muted: #94a3b8;

        --c-blue: #38bdf8;
        --c-blue-bg: rgba(56, 189, 248, 0.12);
        --c-blue-border: #0284c7;

        --c-green: #34d399;
        --c-green-bg: rgba(52, 211, 153, 0.12);
        --c-green-border: #059669;

        --c-red: #f87171;
        --c-red-bg: rgba(248, 113, 113, 0.12);
        --c-red-border: #dc2626;

        --c-yellow: #fbbf24;
        --c-yellow-bg: rgba(251, 191, 36, 0.12);
        --c-yellow-border: #d97706;

        --c-purple: #c084fc;
        --c-purple-bg: rgba(192, 132, 252, 0.12);
        --c-purple-border: #9333ea;

        --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }}

    /* Light Theme Variation (Soft Off-White) */
    body.theme-light {{
        --bg-base: #f1f5f9;
        --bg-surface: #ffffff;
        --bg-card: #e2e8f0;
        --bg-input: #ffffff;
        
        --border: #cbd5e1;
        --border-light: #94a3b8;
        --border-focus: #2563eb;

        --text-heading: #0f172a;
        --text-body: #334155;
        --text-muted: #64748b;

        --c-blue: #2563eb;
        --c-blue-bg: #eff6ff;
        --c-blue-border: #93c5fd;

        --c-green: #059669;
        --c-green-bg: #ecfdf5;
        --c-green-border: #6ee7b7;

        --c-red: #dc2626;
        --c-red-bg: #fef2f2;
        --c-red-border: #fca5a5;

        --c-yellow: #d97706;
        --c-yellow-bg: #fffbeb;
        --c-yellow-border: #fcd34d;

        --c-purple: #7c3aed;
        --c-purple-bg: #f5f3ff;
        --c-purple-border: #c4b5fd;
    }}

    /* OLED Pure Dark Theme Variation */
    body.theme-oled {{
        --bg-base: #060709;
        --bg-surface: #0e1015;
        --bg-card: #151820;
        --bg-input: #000000;
        --border: #1e222d;
        --border-light: #2c3242;
    }}

    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        -webkit-tap-highlight-color: transparent;
    }}

    body {{
        background-color: var(--bg-base);
        color: var(--text-body);
        font-family: var(--font-sans);
        font-size: 14px;
        line-height: 1.5;
        padding-bottom: env(safe-area-inset-bottom, 30px);
        min-height: 100vh;
        transition: background-color 0.15s, color 0.15s;
    }}

    /* Header */
    header {{
        background: var(--bg-surface);
        border-bottom: 1px solid var(--border);
        padding: 10px 16px;
        position: sticky;
        top: 0;
        z-index: 50;
    }}
    .header-inner {{
        max-width: 980px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .brand-wrap {{
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .brand-tag {{
        background: var(--c-blue);
        color: #000;
        font-size: 11px;
        font-weight: 900;
        padding: 3px 8px;
        border-radius: 6px;
        font-family: var(--font-mono);
        text-transform: uppercase;
    }}
    .rep-name {{
        font-size: 15px;
        font-weight: 800;
        color: var(--text-heading);
    }}
    .header-actions {{
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .btn-hdr {{
        background: var(--bg-card);
        border: 1px solid var(--border);
        color: var(--text-heading);
        padding: 6px 11px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}
    .btn-hdr:hover {{ border-color: var(--c-blue); }}

    /* Quick Lead Input Bar */
    .lead-bar {{
        background: var(--bg-surface);
        border-bottom: 1px solid var(--border);
        padding: 10px 16px;
    }}
    .lead-inner {{
        max-width: 980px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)) auto;
        gap: 8px;
        align-items: center;
    }}
    .lead-input-group {{
        display: flex;
        flex-direction: column;
    }}
    .lead-label {{
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 2px;
        letter-spacing: 0.3px;
    }}
    .lead-input {{
        background: var(--bg-input);
        border: 1px solid var(--border);
        color: var(--text-heading);
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
        outline: none;
    }}
    .lead-input:focus {{
        border-color: var(--c-blue);
    }}
    .btn-clear {{
        background: var(--bg-card);
        border: 1px solid var(--border);
        color: var(--text-muted);
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        cursor: pointer;
        align-self: flex-end;
        height: 31px;
    }}
    .btn-clear:hover {{ color: var(--text-heading); }}

    /* Tabs Navigation */
    .nav-tabs {{
        max-width: 980px;
        margin: 0 auto;
        display: flex;
        gap: 6px;
        padding: 12px 16px 0;
        overflow-x: auto;
        scrollbar-width: none;
    }}
    .nav-tabs::-webkit-scrollbar {{ display: none; }}
    
    .tab-btn {{
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-bottom: none;
        color: var(--text-muted);
        font-size: 12.5px;
        font-weight: 700;
        padding: 9px 14px;
        border-radius: 8px 8px 0 0;
        cursor: pointer;
        white-space: nowrap;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .tab-btn:hover {{ color: var(--text-heading); }}
    .tab-btn.active {{
        background: var(--bg-surface);
        color: var(--c-blue);
        border-color: var(--border);
        border-top: 2px solid var(--c-blue);
        border-bottom: 2px solid var(--bg-surface);
    }}

    /* Main Container */
    main {{
        max-width: 980px;
        margin: 0 auto;
        padding: 14px 16px;
    }}

    .tab-pane {{ display: none; }}
    .tab-pane.active {{ display: block; }}

    /* =========================================================================
       DIALER COPILOT HUD (TWILIGHT SLATE)
       ========================================================================= */
    .hud-box {{
        background: var(--bg-surface);
        border: 1px solid var(--border-light);
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 14px;
    }}
    @media (min-width: 640px) {{
        .hud-box {{ padding: 22px; }}
    }}

    .hud-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--border);
    }}
    .stage-badge {{
        background: var(--c-blue-bg);
        border: 1px solid var(--c-blue-border);
        color: var(--c-blue);
        font-size: 11px;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 4px;
        font-family: var(--font-mono);
        text-transform: uppercase;
    }}
    .step-counter {{
        font-family: var(--font-mono);
        font-size: 11px;
        color: var(--text-muted);
    }}

    /* What You Say Out Loud */
    .say-box {{
        background: var(--bg-input);
        border: 2px solid var(--c-blue-border);
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 16px;
        position: relative;
    }}
    .say-label {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: var(--c-blue);
        color: #000;
        font-size: 10.5px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 2px 8px;
        border-radius: 4px;
        margin-bottom: 10px;
    }}
    .say-text {{
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.5;
        white-space: pre-wrap;
    }}
    body.theme-light .say-text {{ color: #0f172a; }}
    @media (max-width: 600px) {{
        .say-text {{ font-size: 15px; line-height: 1.4; }}
    }}
    .say-text .token-highlight {{
        background: #fef08a;
        color: #854d0e;
        padding: 1px 5px;
        border-radius: 4px;
        font-weight: 800;
    }}

    /* Tactical Tip */
    .tactical-bar {{
        background: var(--c-purple-bg);
        border-left: 4px solid var(--c-purple);
        border-radius: 0 4px 4px 0;
        padding: 7px 12px;
        margin-top: 12px;
        font-size: 12px;
        color: var(--c-purple);
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }}

    /* Reaction Options Grid */
    .options-label {{
        font-size: 11.5px;
        font-weight: 800;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
    }}

    .options-grid {{
        display: grid;
        grid-template-columns: 1fr;
        gap: 8px;
        margin-bottom: 16px;
    }}
    @media (min-width: 640px) {{
        .options-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}

    .opt-btn {{
        background: var(--bg-card);
        border: 2px solid var(--border);
        padding: 12px 14px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 700;
        text-align: left;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.05s;
    }}
    .opt-btn:active {{ transform: scale(0.98); }}

    /* Colors */
    .opt-btn.pos {{
        background: var(--c-green-bg);
        border-color: var(--c-green-border);
        color: var(--c-green);
    }}
    .opt-btn.pos .key-pill {{
        background: var(--c-green);
        color: #000;
    }}

    .opt-btn.neg {{
        background: var(--c-red-bg);
        border-color: var(--c-red-border);
        color: var(--c-red);
    }}
    .opt-btn.neg .key-pill {{
        background: var(--c-red);
        color: #000;
    }}

    .opt-btn.amber {{
        background: var(--c-yellow-bg);
        border-color: var(--c-yellow-border);
        color: var(--c-yellow);
    }}
    .opt-btn.amber .key-pill {{
        background: var(--c-yellow);
        color: #000;
    }}

    .key-pill {{
        font-family: var(--font-mono);
        font-size: 11px;
        font-weight: 900;
        padding: 2px 7px;
        border-radius: 4px;
        margin-left: 8px;
        flex-shrink: 0;
    }}

    /* Bottom HUD Foot */
    .hud-foot {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 12px;
        border-top: 1px solid var(--border);
    }}
    .btn-nav {{
        background: var(--bg-card);
        border: 1px solid var(--border-light);
        color: var(--text-heading);
        padding: 7px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
    }}
    .btn-nav:hover {{ border-color: var(--c-blue); }}

    /* =========================================================================
       CARDS & UTILITIES
       ========================================================================= */
    .card {{
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 14px;
    }}
    .card-title {{
        font-size: 14px;
        font-weight: 800;
        color: var(--text-heading);
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }}

    .bank-chips {{
        display: flex;
        gap: 6px;
        margin-bottom: 12px;
        overflow-x: auto;
    }}
    .bank-chip {{
        background: var(--bg-card);
        border: 1.5px solid var(--border);
        color: var(--text-muted);
        padding: 7px 14px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
    }}
    .bank-chip.active.chase {{
        background: #1e40af;
        border-color: #3b82f6;
        color: #ffffff;
    }}
    .bank-chip.active.boa {{
        background: #991b1b;
        border-color: #ef4444;
        color: #ffffff;
    }}
    .bank-chip.active.wells {{
        background: #92400e;
        border-color: #f59e0b;
        color: #ffffff;
    }}
    .bank-chip.active.universal {{
        background: #5b21b6;
        border-color: #a855f7;
        color: #ffffff;
    }}

    .copy-box {{
        background: var(--bg-input);
        border: 1px solid var(--border);
        border-left: 4px solid var(--c-blue);
        border-radius: 6px;
        padding: 14px;
        margin: 8px 0;
        position: relative;
    }}
    .copy-box.green-box {{ border-left-color: var(--c-green); background: var(--c-green-bg); }}
    .copy-box.red-box {{ border-left-color: var(--c-red); background: var(--c-red-bg); }}
    .copy-box.yellow-box {{ border-left-color: var(--c-yellow); background: var(--c-yellow-bg); }}

    .copy-text {{
        font-size: 13px;
        color: var(--text-heading);
        white-space: pre-wrap;
        line-height: 1.55;
    }}
    .btn-copy {{
        position: absolute;
        top: 8px;
        right: 8px;
        background: var(--bg-card);
        border: 1px solid var(--border-light);
        color: var(--text-muted);
        font-size: 11px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        cursor: pointer;
    }}
    .btn-copy:hover {{ color: var(--text-heading); border-color: var(--c-blue); }}

    /* Calculator */
    .calc-inputs {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 10px;
        margin-bottom: 14px;
    }}
    .calc-box label {{
        display: block;
        font-size: 11px;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        margin-bottom: 4px;
    }}
    .calc-box input {{
        width: 100%;
        background: var(--bg-input);
        border: 1.5px solid var(--border);
        color: var(--text-heading);
        padding: 8px 10px;
        border-radius: 6px;
        font-family: var(--font-mono);
        font-size: 14px;
        font-weight: 700;
    }}
    .calc-box input:focus {{ outline: none; border-color: var(--c-blue); }}

    .calc-metrics {{
        background: var(--bg-input);
        border: 1.5px solid var(--border);
        border-radius: 8px;
        padding: 16px;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        text-align: center;
    }}
    .metric-val {{
        font-size: 20px;
        font-weight: 900;
        font-family: var(--font-mono);
    }}
    .metric-lbl {{
        font-size: 10px;
        font-weight: 800;
        color: var(--text-muted);
        text-transform: uppercase;
        margin-top: 2px;
    }}

    /* =========================================================================
       SHARE / ADD TO DEVICE MODAL
       ========================================================================= */
    .modal-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.75);
        backdrop-filter: blur(4px);
        z-index: 1000;
        display: none;
        align-items: center;
        justify-content: center;
        padding: 16px;
    }}
    .modal-overlay.open {{ display: flex; }}
    
    .modal-content {{
        background: var(--bg-surface);
        border: 1px solid var(--border-light);
        border-radius: 12px;
        max-width: 480px;
        width: 100%;
        padding: 24px;
        position: relative;
    }}
    .modal-close {{
        position: absolute;
        top: 14px;
        right: 14px;
        background: var(--bg-card);
        border: none;
        font-size: 16px;
        font-weight: 700;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        cursor: pointer;
        color: var(--text-muted);
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .modal-close:hover {{ color: var(--text-heading); }}
    .modal-title {{
        font-size: 16px;
        font-weight: 800;
        color: var(--text-heading);
        margin-bottom: 4px;
    }}
    .modal-sub {{
        font-size: 12px;
        color: var(--text-muted);
        margin-bottom: 16px;
    }}

    .qr-container {{
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        margin-bottom: 16px;
    }}
    .qr-img {{
        width: 160px;
        height: 160px;
        border-radius: 6px;
    }}

    .link-copy-group {{
        display: flex;
        gap: 6px;
        margin-bottom: 16px;
    }}
    .link-input {{
        flex: 1;
        background: var(--bg-input);
        border: 1px solid var(--border);
        color: var(--text-heading);
        padding: 8px 12px;
        border-radius: 6px;
        font-family: var(--font-mono);
        font-size: 12px;
        outline: none;
    }}
    .btn-copy-url {{
        background: var(--c-blue);
        color: #000;
        border: none;
        padding: 8px 14px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 800;
        cursor: pointer;
        white-space: nowrap;
    }}

    .device-guide-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
    }}
    .device-guide-item {{
        background: var(--bg-card);
        border: 1px solid var(--border);
        padding: 10px;
        border-radius: 6px;
        font-size: 11.5px;
    }}
    .guide-title {{
        font-weight: 800;
        color: var(--text-heading);
        margin-bottom: 3px;
        display: flex;
        align-items: center;
        gap: 4px;
    }}
    .guide-desc {{
        color: var(--text-muted);
        line-height: 1.35;
    }}

    /* Toast */
    .toast {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--c-green);
        color: #000;
        font-weight: 800;
        font-size: 12px;
        padding: 7px 16px;
        border-radius: 6px;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.15s ease;
        z-index: 2000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }}
    .toast.show {{ opacity: 1; }}

    @media print {{
        header, .lead-bar, .nav-tabs, .btn-nav, .btn-copy, .btn-clear, .btn-hdr, .modal-overlay {{ display: none !important; }}
        body {{ background: #fff; color: #000; }}
        .hud-box, .card {{ border: 1px solid #ccc; background: #fff; box-shadow: none; }}
        .say-box, .copy-box {{ background: #fafafa; border: 1px solid #ddd; }}
        .say-text, .copy-text {{ color: #000; }}
    }}
</style>
</head>
<body>

<header>
    <div class="header-inner">
        <div class="brand-wrap">
            <span class="brand-tag">MICHAEL QIN</span>
            <span class="rep-name">Sales Closer Flight Deck</span>
        </div>
        <div class="header-actions">
            <button class="btn-hdr" onclick="cycleTheme()" id="theme-btn">🎨 Theme: Slate</button>
            <button class="btn-hdr" onclick="openShareModal()">🔗 Create Link</button>
        </div>
    </div>
</header>

<!-- Quick Lead Personalization Bar -->
<div class="lead-bar">
    <div class="lead-inner">
        <div class="lead-input-group">
            <span class="lead-label">Contact / Owner Name</span>
            <input type="text" id="lead-name" class="lead-input" placeholder="e.g. John" oninput="updatePersonalization()">
        </div>
        <div class="lead-input-group">
            <span class="lead-label">Company / Merchant Name</span>
            <input type="text" id="lead-company" class="lead-input" placeholder="e.g. Apex Logistics" oninput="updatePersonalization()">
        </div>
        <div class="lead-input-group">
            <span class="lead-label">Industry / Niche</span>
            <input type="text" id="lead-industry" class="lead-input" placeholder="e.g. Trucking / Logistics" oninput="updatePersonalization()">
        </div>
        <button class="btn-clear" onclick="clearLeadInputs()">Clear</button>
    </div>
</div>

<div class="nav-tabs">
    <button class="tab-btn active" onclick="switchTab('tab-hud')">🎙️ Dialer Copilot</button>
    <button class="tab-btn" onclick="switchTab('tab-statement')">📄 Statement Extraction</button>
    <button class="tab-btn" onclick="switchTab('tab-calc')">💰 Savings Calc</button>
    <button class="tab-btn" onclick="switchTab('tab-objections')">🛡️ Pushbacks</button>
    <button class="tab-btn" onclick="switchTab('tab-cadence')">📬 SMS Follow-Ups</button>
    <button class="tab-btn" onclick="switchTab('tab-pipeline')">🚀 7-Stage Pipeline</button>
</div>

<main>

    <!-- TAB 1: DIALER COPILOT -->
    <div id="tab-hud" class="tab-pane active">
        <div class="hud-box">
            <div class="hud-header">
                <span class="stage-badge" id="hud-stage">Stage 1: Opening (0-5s)</span>
                <span class="step-counter" id="hud-step">Step 1 of 4</span>
            </div>

            <!-- What You Say -->
            <div class="say-box">
                <div class="say-label">🗣️ WHAT YOU SAY OUT LOUD</div>
                <div class="say-text" id="hud-verbatim">"Hey [Name], I will be brief. I know I am calling out of the blue.

I work on the commercial capital placement side, and the reason for the call is simple: we are working with merchants in [Industry] right now to lower their daily/weekly debits and clean up expensive debt."</div>
                <div class="tactical-bar" id="hud-bar">
                    <span>💡</span>
                    <span id="hud-tactical">Speak with calm authority, like an underwriting auditor checking figures.</span>
                </div>
            </div>

            <!-- What They Say -->
            <div class="options-label">
                <span>👉 WHAT DID THE PROSPECT SAY?</span>
                <span>(Press Number Key or Tap)</span>
            </div>

            <div class="options-grid" id="hud-options">
                <!-- Dynamically Injected -->
            </div>

            <div class="hud-foot">
                <button class="btn-nav" onclick="goBack()" id="btn-back" style="display:none;">⬅ Previous Cue</button>
                <div style="display: flex; gap: 6px; margin-left: auto;">
                    <button class="btn-nav" onclick="copyText(getCleanScriptText())">📋 Copy Line (Space)</button>
                    <button class="btn-nav" onclick="resetFlow()">🔄 Reset Call (R)</button>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 2: STATEMENT EXTRACTION -->
    <div id="tab-statement" class="tab-pane">
        <div class="card">
            <div class="card-title">🚀 45-Second On-Call Statement Extraction Protocol</div>
            <p style="font-size: 12.5px; color: var(--text-muted); margin-bottom: 12px;">
                Never let an interested merchant hang up with a vague "I'll do it later." Walk them through exporting their 3 PDF statements while on the phone.
            </p>

            <div class="copy-box green-box">
                <div style="font-size: 11px; font-weight: 800; color: var(--c-green); text-transform: uppercase; margin-bottom: 4px;">The Live Phone Walkthrough Line</div>
                <div class="copy-text" id="stmt-walkthrough-text">"John, are you in front of your computer or looking at your phone right now?

Stay on with me for literally 45 seconds while you export your last 3 monthly statements as PDFs. I will confirm receipt while we're on the line so this isn't hanging over your head tonight.

Which bank do you use for operations—Chase, Bank of America, or Wells?"</div>
                <button class="btn-copy" onclick="copySnippet(this)">Copy</button>
            </div>

            <div style="margin: 14px 0 6px; font-size: 11px; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">
                Select Merchant Bank for Exact 2-Click Steps:
            </div>
            <div class="bank-chips">
                <button class="bank-chip active chase" onclick="selectBank('chase', this)">🔵 Chase</button>
                <button class="bank-chip boa" onclick="selectBank('boa', this)">🔴 Bank of America</button>
                <button class="bank-chip wells" onclick="selectBank('wells', this)">🟡 Wells Fargo</button>
                <button class="bank-chip universal" onclick="selectBank('universal', this)">🟣 Universal App</button>
            </div>

            <div class="copy-box">
                <div class="copy-text" id="bank-guide-text">1. Tell merchant: "Log into Chase.com and click your business checking account."
2. "Click 'Statements & Documents' right below the balance."
3. "Download the last 3 monthly PDFs and forward directly to my email."</div>
                <button class="btn-copy" onclick="copySnippet(this)">Copy</button>
            </div>
        </div>

        <div class="card">
            <div class="card-title">🛡️ The "Loss Aversion" Rebuttal (Chris Voss)</div>
            <div class="copy-box yellow-box">
                <div class="copy-text" id="loss-aversion-text">"John, I don't want you wasting your evening downloading statements if this doesn't put money back into your business.

If our review shows your current setup is already optimal, I will tell you to keep it. But if you're leaking $2,500 a month in excessive factor fees or daily debits, wouldn't you want to know by tomorrow morning?

Let me send you a secure request link right now. What's the best email?"</div>
                <button class="btn-copy" onclick="copySnippet(this)">Copy</button>
            </div>
        </div>
    </div>

    <!-- TAB 3: SAVINGS CALCULATOR -->
    <div id="tab-calc" class="tab-pane">
        <div class="card">
            <div class="card-title">💰 Live Merchant Debt Restructuring & Cash Flow Calculator</div>
            <div class="calc-inputs">
                <div class="calc-box">
                    <label>Monthly Revenue ($)</label>
                    <input type="number" id="calc-rev" value="120000" step="5000" oninput="runCalc()">
                </div>
                <div class="calc-box">
                    <label>Current Debits ($/Month)</label>
                    <input type="number" id="calc-debit" value="18000" step="1000" oninput="runCalc()">
                </div>
                <div class="calc-box">
                    <label>Proposed New Payment ($/Mo)</label>
                    <input type="number" id="calc-new-pay" value="7500" step="500" oninput="runCalc()">
                </div>
                <div class="calc-box">
                    <label>New Capital ($)</label>
                    <input type="number" id="calc-advance" value="150000" step="10000" oninput="runCalc()">
                </div>
            </div>

            <div class="calc-metrics">
                <div>
                    <div class="metric-val" id="res-monthly" style="color: var(--c-green);">+$10,500</div>
                    <div class="metric-lbl">Monthly Cash Freed</div>
                </div>
                <div>
                    <div class="metric-val" id="res-annual" style="color: var(--c-blue);">$126,000</div>
                    <div class="metric-lbl">Annual Savings</div>
                </div>
                <div>
                    <div class="metric-val" id="res-capital" style="color: var(--c-purple);">$150,000</div>
                    <div class="metric-lbl">Liquidity Unlocked</div>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 4: PUSHBACK MATRIX -->
    <div id="tab-objections" class="tab-pane">
        <div class="card">
            <div class="card-title">🛡️ Pushback & Objection Matrix</div>
            <div id="objections-list"></div>
        </div>
    </div>

    <!-- TAB 5: CADENCE -->
    <div id="tab-cadence" class="tab-pane">
        <div class="card">
            <div class="card-title">📬 10-Day Multi-Touch SMS & Email Cadence</div>
            
            <div style="font-size: 11px; font-weight: 800; color: var(--c-green); text-transform: uppercase; margin-top: 10px;">Day 1: Instant Post-Call SMS</div>
            <div class="copy-box green-box">
                <div class="copy-text" id="cadence-sms1">"Hi [Name], Michael Qin here from Capital Advisory. Great speaking with you briefly. To run your debt consolidation and statement audit for [Company], just email your last 3 monthly business bank PDFs to michael@capitaladvisory.com. Once received, I will have your approved numbers back within 24 hours."</div>
                <button class="btn-copy" onclick="copySnippet(this)">Copy</button>
            </div>

            <div style="font-size: 11px; font-weight: 800; color: var(--c-yellow); text-transform: uppercase; margin-top: 14px;">Day 3: Midday Leakage Check-In</div>
            <div class="copy-box yellow-box">
                <div class="copy-text" id="cadence-email1">Subject: Quick question regarding [Company] cash flow

Hi [Name],

Following up on our conversation regarding restructuring your operating debt for [Company]. 

Our underwriting desk locks weekly merchant placement tiers every Thursday at 4 PM. If you shoot over your 3 bank statements today, I can have your term sheet approved before the weekend.

Let me know if you need help pulling the PDFs from Chase/BoA.

Best,
Michael Qin</div>
                <button class="btn-copy" onclick="copySnippet(this)">Copy</button>
            </div>

            <div style="font-size: 11px; font-weight: 800; color: var(--c-red); text-transform: uppercase; margin-top: 14px;">Day 8: Permission-to-Close Breakup</div>
            <div class="copy-box red-box">
                <div class="copy-text" id="cadence-email2">Subject: Closing your file / [Company]

Hi [Name],

I assume restructuring your working capital isn't a priority right now, so I will close out your file for [Company].

If daily debits ever start squeezing your cash flow down the road, feel free to reach out anytime.

Best regards,
Michael Qin</div>
                <button class="btn-copy" onclick="copySnippet(this)">Copy</button>
            </div>
        </div>
    </div>

    <!-- TAB 6: PIPELINE STAGES -->
    <div id="tab-pipeline" class="tab-pane">
        <div class="card">
            <div class="card-title">🚀 Complete 7-Stage Pipeline</div>
            <div id="pipeline-list"></div>
        </div>
    </div>

</main>

<!-- SHARE / CREATE LINK MODAL -->
<div id="share-modal" class="modal-overlay" onclick="closeShareModal(event)">
    <div class="modal-content" onclick="event.stopPropagation()">
        <button class="modal-close" onclick="closeShareModal()">✕</button>
        <div class="modal-title">📲 Add to Any Device / Create Link</div>
        <div class="modal-sub">Open this flight deck instantly on your phone or work computer.</div>

        <div class="qr-container">
            <img class="qr-img" id="qr-code-img" alt="QR Code" src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=https://naudiac.github.io/utility-scripts/michael-qin/">
            <span style="font-size: 11.5px; font-weight: 800; color: #000;">📷 Scan with Phone Camera to Open</span>
        </div>

        <div class="link-copy-group">
            <input type="text" id="share-url-box" class="link-input" readonly value="https://naudiac.github.io/utility-scripts/michael-qin/">
            <button class="btn-copy-url" onclick="copyToolUrl()">📋 Copy Link</button>
        </div>

        <div class="device-guide-grid">
            <div class="device-guide-item">
                <div class="guide-title">📱 iPhone / Safari</div>
                <div class="guide-desc">Tap <strong>Share ➔ 'Add to Home Screen'</strong> to run as a full-screen app.</div>
            </div>
            <div class="device-guide-item">
                <div class="guide-title">🤖 Android / Chrome</div>
                <div class="guide-desc">Tap <strong>3-Dots ➔ 'Add to Home Screen'</strong> or 'Install App'.</div>
            </div>
            <div class="device-guide-item">
                <div class="guide-title">💻 Windows / Dialer</div>
                <div class="guide-desc">Press <strong>Ctrl+D</strong> to bookmark next to your autodialer window.</div>
            </div>
            <div class="device-guide-item">
                <div class="guide-title">⚡ Native Share</div>
                <div class="guide-desc"><a href="javascript:void(0)" onclick="triggerNativeShare()" style="color:var(--c-blue); font-weight:700; text-decoration:none;">Tap to AirDrop / SMS Link →</a></div>
            </div>
        </div>
    </div>
</div>

<div id="toast" class="toast">Copied to clipboard</div>

<script>
const STAGES = {stages_json};
const OBJECTIONS = {objections_json};

/* =========================================================================
   THEME SWITCHER (SLATE -> OLED -> LIGHT)
   ========================================================================= */
const THEMES = ["slate", "oled", "light"];
let currentThemeIdx = 0;

function cycleTheme() {{
    currentThemeIdx = (currentThemeIdx + 1) % THEMES.length;
    applyTheme(THEMES[currentThemeIdx]);
}}

function applyTheme(name) {{
    document.body.classList.remove('theme-light', 'theme-oled');
    const btn = document.getElementById('theme-btn');
    if (name === 'light') {{
        document.body.classList.add('theme-light');
        btn.innerText = "☀️ Theme: Daylight";
    }} else if (name === 'oled') {{
        document.body.classList.add('theme-oled');
        btn.innerText = "🌙 Theme: OLED Dark";
    }} else {{
        btn.innerText = "🎨 Theme: Slate";
    }}
    localStorage.setItem('mq_theme', name);
}}

/* =========================================================================
   SHARE MODAL LOGIC
   ========================================================================= */
function openShareModal() {{
    const modal = document.getElementById('share-modal');
    if (modal) modal.classList.add('open');
}}

function closeShareModal(e) {{
    const modal = document.getElementById('share-modal');
    if (modal) modal.classList.remove('open');
}}

function copyToolUrl() {{
    const box = document.getElementById('share-url-box');
    copyText(box.value);
}}

function triggerNativeShare() {{
    const url = "https://naudiac.github.io/utility-scripts/michael-qin/";
    if (navigator.share) {{
        navigator.share({{
            title: "Michael Qin - Sales Flight Deck",
            text: "Real-time autodialer copilot & merchant statement extraction tool.",
            url: url
        }}).catch(() => {{}});
    }} else {{
        copyToolUrl();
    }}
}}

/* =========================================================================
   DYNAMIC LEAD PERSONALIZATION
   ========================================================================= */
let leadState = {{
    name: "",
    company: "",
    industry: ""
}};

function getEffectiveTokens() {{
    return {{
        name: leadState.name.trim() || "John",
        company: leadState.company.trim() || "your company",
        industry: leadState.industry.trim() || "your industry"
    }};
}}

function formatWithTokens(templateStr, highlight = false) {{
    const t = getEffectiveTokens();
    let res = templateStr;

    if (highlight && leadState.name.trim()) {{
        res = res.replaceAll("[Name]", `<span class="token-highlight">${{t.name}}</span>`);
    }} else {{
        res = res.replaceAll("[Name]", t.name);
    }}

    if (highlight && leadState.company.trim()) {{
        res = res.replaceAll("[Company]", `<span class="token-highlight">${{t.company}}</span>`);
    }} else {{
        res = res.replaceAll("[Company]", t.company);
    }}

    if (highlight && leadState.industry.trim()) {{
        res = res.replaceAll("[Industry]", `<span class="token-highlight">${{t.industry}}</span>`);
    }} else {{
        res = res.replaceAll("[Industry]", t.industry);
    }}

    return res;
}}

function updatePersonalization() {{
    leadState.name = document.getElementById('lead-name').value;
    leadState.company = document.getElementById('lead-company').value;
    leadState.industry = document.getElementById('lead-industry').value;

    renderCurrentNode();
    updateCadenceSnippets();
}}

function clearLeadInputs() {{
    document.getElementById('lead-name').value = "";
    document.getElementById('lead-company').value = "";
    document.getElementById('lead-industry').value = "";
    leadState = {{ name: "", company: "", industry: "" }};
    updatePersonalization();
}}

function updateCadenceSnippets() {{
    const t = getEffectiveTokens();
    const sms1 = `"Hi ${{t.name}}, Michael Qin here from Capital Advisory. Great speaking with you briefly. To run your debt consolidation and statement audit for ${{t.company}}, just email your last 3 monthly business bank PDFs to michael@capitaladvisory.com. Once received, I will have your approved numbers back within 24 hours."`;
    const email1 = `Subject: Quick question regarding ${{t.company}} cash flow\n\nHi ${{t.name}},\n\nFollowing up on our conversation regarding restructuring your operating debt for ${{t.company}}.\n\nOur underwriting desk locks weekly merchant placement tiers every Thursday at 4 PM. If you shoot over your 3 bank statements today, I can have your term sheet approved before the weekend.\n\nLet me know if you need help pulling the PDFs from Chase/BoA.\n\nBest,\nMichael Qin`;
    const email2 = `Subject: Closing your file / ${{t.company}}\n\nHi ${{t.name}},\n\nI assume restructuring your working capital isn't a priority right now, so I will close out your file for ${{t.company}}.\n\nIf daily debits ever start squeezing your cash flow down the road, feel free to reach out anytime.\n\nBest regards,\nMichael Qin`;
    const stmtWalk = `"${{t.name}}, are you in front of your computer or looking at your phone right now?\n\nStay on with me for literally 45 seconds while you export your last 3 monthly statements as PDFs. I will confirm receipt while we're on the line so this isn't hanging over your head tonight.\n\nWhich bank do you use for operations—Chase, Bank of America, or Wells?"`;
    const lossAv = `"${{t.name}}, I don't want you wasting your evening downloading statements if this doesn't put money back into your business.\n\nIf our review shows your current setup is already optimal, I will tell you to keep it. But if you're leaking $2,500 a month in excessive factor fees or daily debits, wouldn't you want to know by tomorrow morning?\n\nLet me send you a secure request link right now. What's the best email?"`;

    const el1 = document.getElementById('cadence-sms1'); if(el1) el1.innerText = sms1;
    const el2 = document.getElementById('cadence-email1'); if(el2) el2.innerText = email1;
    const el3 = document.getElementById('cadence-email2'); if(el3) el3.innerText = email2;
    const el4 = document.getElementById('stmt-walkthrough-text'); if(el4) el4.innerText = stmtWalk;
    const el5 = document.getElementById('loss-aversion-text'); if(el5) el5.innerText = lossAv;
}}

/* =========================================================================
   CALL FLOW TREE (WITH TEMPLATE TOKENS)
   ========================================================================= */
const CALL_FLOW = {{
    "root": {{
        stage: "Stage 1: Opening (0-5s)",
        verbatim: `"Hey [Name], I will be brief. I know I am calling out of the blue.

I work on the commercial capital placement side, and the reason for the call is simple: we are working with merchants in [Industry] right now to lower their daily/weekly debits and clean up expensive debt."`,
        tactical: "Speak with calm authority, like an underwriting auditor checking figures.",
        options: [
            {{ text: `"Who is this / What company?"`, key: "1", next: "who_is_this", type: "pos" }},
            {{ text: `[Listened / Silence / "Okay..."]`, key: "2", next: "aligned_hook", type: "pos" }},
            {{ text: `"We don't need money / We're all set"`, key: "3", next: "dont_need_money", type: "neg" }},
            {{ text: `"Just email me info / I'm busy"`, key: "4", next: "just_email_me", type: "amber" }},
            {{ text: `"What are your rates / factor rates?"`, key: "5", next: "what_rates", type: "amber" }},
            {{ text: `"I don't send bank statements"`, key: "6", next: "statement_pushback", type: "neg" }}
        ]
    }},

    "who_is_this": {{
        stage: "Stage 2: Identity & Disarm (6-15s)",
        verbatim: `"I'm Michael Qin with Capital Placement Advisory. We specialize in commercial working capital and restructuring high-cost merchant debt.

The reason I reached out directly to [Company] is because we just restructured financing for a business in [Industry], cutting their monthly debt payment by 40%.

I'm not asking for your business today—I just want to run a free debt audit against your last 3 statements to show you what you could save.

Where should I email the benchmark sheet?"`,
        tactical: "State your niche, reference peer results, and close for their direct email.",
        options: [
            {{ text: `"Sure, send to [Email]"`, key: "1", next: "win_extract_statements", type: "pos" }},
            {{ text: `"We don't need any funding"`, key: "2", next: "dont_need_money", type: "neg" }},
            {{ text: `"What are your rates?"`, key: "3", next: "what_rates", type: "amber" }}
        ]
    }},

    "aligned_hook": {{
        stage: "Stage 2: Core Value & Risk Reversal",
        verbatim: `"I'm not asking you to commit to anything today. My model is simple: I only get paid if we actually deliver terms and lower payments that beat what you currently have at [Company].

If you shoot over your last 3 monthly statements, I will run a side-by-side comparison within 24 hours showing your exact monthly cash flow savings.

What is the best email to send that breakdown to?"`,
        tactical: "Highlight zero downside risk for the business owner.",
        options: [
            {{ text: `Merchant gave email address`, key: "1", next: "win_extract_statements", type: "pos" }},
            {{ text: `"We already have a lender"`, key: "2", next: "dont_need_money", type: "neg" }},
            {{ text: `"I don't have time right now"`, key: "3", next: "just_email_me", type: "amber" }}
        ]
    }},

    "dont_need_money": {{
        stage: "Pivot: No Borrowing Needed",
        verbatim: `"Completely understand [Name], and I'm glad [Company] is running strong. I'm actually not calling to sell you new debt.

Most successful operators we work with aren't looking to borrow—they just want to stop getting squeezed by high fees and daily debits on existing positions.

If our audit shows your current setup is optimal, at least you keep your lenders honest. If we find \$2,000 a month in leakage, you keep the cash.

What's the best email for that 1-page check?"`,
        tactical: "Reframe from borrowing to expense reduction and cash recovery.",
        options: [
            {{ text: `"Fair enough, send to [Email]"`, key: "1", next: "win_extract_statements", type: "pos" }},
            {{ text: `"Not interested / Hard No"`, key: "2", next: "hard_no", type: "neg" }}
        ]
    }},

    "just_email_me": {{
        stage: "Pivot: 'Send Info' Deflection",
        verbatim: `"Happy to do that [Name]. Rather than sending a generic PDF deck that will sit in your spam, are you in front of your computer or on your phone right now?

Stay with me for 45 seconds while you click 'Download Statements' on your bank portal. I will confirm receipt on the line so you don't have this on your to-do list tonight.

Which bank do you use for [Company]—Chase, BoA, or Wells?"`,
        tactical: "Never let them off the phone without asking for the 45-second on-call download.",
        options: [
            {{ text: `"I'm on my computer now / Exporting"`, key: "1", next: "win_on_call_download", type: "pos" }},
            {{ text: `"I'm driving / really busy"`, key: "2", next: "send_sms_link", type: "amber" }}
        ]
    }},

    "what_rates": {{
        stage: "Pricing Hook & Trade-Off",
        verbatim: `"Rates depend entirely on monthly revenue and cash flow for [Company], but we are consistently placing capital at terms that cut daily debits in half.

To give you an exact rate card rather than a misleading ballpark, shoot over your last 3 monthly statements and I'll deliver your exact terms in 3 hours.

What address should I send the doc request to?"`,
        tactical: "Never quote a blind number; trade rate clarity for statements.",
        options: [
            {{ text: `Merchant agreed / gave email`, key: "1", next: "win_extract_statements", type: "pos" }},
            {{ text: `"Why do you need statements?"`, key: "2", next: "statement_pushback", type: "neg" }}
        ]
    }},

    "statement_pushback": {{
        stage: "Statement Hesitation Rebuttal",
        verbatim: `"Totally understand the caution [Name]—your company financials are sensitive. 

We do not shop your file to 20 brokers. We do a direct, in-house preliminary audit to confirm your true monthly volume so we can negotiate institutional terms on behalf of [Company].

You can redact your account numbers if you prefer. What is the best email to send the secure link to?"`,
        tactical: "Offer account number redaction to instantly eliminate security friction.",
        options: [
            {{ text: `"Okay, send the email"`, key: "1", next: "win_extract_statements", type: "pos" }}
        ]
    }},

    "win_extract_statements": {{
        stage: "🎉 Win: Email Captured & Live Statement Ask",
        verbatim: `"Got that down. I just sent the direct link to [Email].

While I have you for 30 seconds [Name], are you able to click 'Forward' on your last 3 monthly PDFs right now so I can prioritize [Company] for tomorrow morning's underwriting committee?"`,
        tactical: "Strike immediately while you have their attention on the phone.",
        options: [
            {{ text: `"Doing it right now on the phone"`, key: "1", next: "win_on_call_download", type: "pos" }},
            {{ text: `"I'll do it by 4 PM today"`, key: "2", next: "win_deadline_set", type: "amber" }}
        ]
    }},

    "win_on_call_download": {{
        stage: "🏆 Complete Win: Statements Received Live",
        verbatim: `"Boom, I see the 3 PDFs for [Company] in my inbox right now.

I will personally run the cash flow model and have your benchmark savings breakdown in your inbox by tomorrow morning.

Thank you [Name], speak tomorrow!"`,
        tactical: "Confirm receipt and close the call on a high note.",
        options: [
            {{ text: `Reset for Next Call (R)`, key: "1", next: "root", type: "pos" }}
        ]
    }},

    "win_deadline_set": {{
        stage: "⏰ Win: 4 PM Underwriting Deadline Locked",
        verbatim: `"Perfect [Name]. I will hold a spot with our credit desk for 4 PM today. As soon as you email those 3 PDFs, I will get [Company] to the front of the queue.

Look out for my text message with the direct upload email. Have a great day!"`,
        tactical: "Send Day 1 SMS within 60 seconds.",
        options: [
            {{ text: `Reset for Next Call (R)`, key: "1", next: "root", type: "pos" }}
        ]
    }},

    "send_sms_link": {{
        stage: "Mobile Fallback: Direct 1-Click SMS",
        verbatim: `"Understood [Name], drive safe. I am texting my direct email and a 2-click statement link to this mobile number right now.

Reply with the 3 PDFs when you're back at your desk and I'll jump on it immediately."`,
        tactical: "Send SMS immediately while your voice is fresh in their head.",
        options: [
            {{ text: `Reset for Next Call (R)`, key: "1", next: "root", type: "pos" }}
        ]
    }},

    "hard_no": {{
        stage: "Graceful Exit & Long-Term Seed",
        verbatim: `"Totally respect that [Name]. I'll leave you to your day. If cash flow ever gets tight down the road, you have my number. Have a great week!"`,
        tactical: "Never show frustration. Elite closers always leave the door wide open.",
        options: [
            {{ text: `Reset for Next Call (R)`, key: "1", next: "root", type: "pos" }}
        ]
    }}
}};

let historyStack = ["root"];

function renderCurrentNode() {{
    const key = historyStack[historyStack.length - 1];
    const node = CALL_FLOW[key] || CALL_FLOW["root"];

    document.getElementById('hud-stage').innerText = node.stage;
    document.getElementById('hud-verbatim').innerHTML = formatWithTokens(node.verbatim, true);
    document.getElementById('hud-tactical').innerText = node.tactical;
    document.getElementById('hud-step').innerText = `Step ${{historyStack.length}}`;

    const btnGrid = document.getElementById('hud-options');
    btnGrid.innerHTML = node.options.map(opt => `
        <button class="opt-btn ${{opt.type}}" onclick="pickNext('${{opt.next}}')">
            <span>${{formatWithTokens(opt.text)}}</span>
            <span class="key-pill">${{opt.key}}</span>
        </button>
    `).join('');

    document.getElementById('btn-back').style.display = historyStack.length > 1 ? 'inline-block' : 'none';
}}

function getCleanScriptText() {{
    const key = historyStack[historyStack.length - 1];
    const node = CALL_FLOW[key] || CALL_FLOW["root"];
    return formatWithTokens(node.verbatim, false);
}}

function pickNext(key) {{
    historyStack.push(key);
    renderCurrentNode();
}}

function goBack() {{
    if (historyStack.length > 1) {{
        historyStack.pop();
        renderCurrentNode();
    }}
}}

function resetFlow() {{
    historyStack = ["root"];
    renderCurrentNode();
}}

// Keyboard Listener
window.addEventListener('keydown', (e) => {{
    const hudTab = document.getElementById('tab-hud');
    if (!hudTab.classList.contains('active')) return;
    if (e.target.tagName === 'INPUT') return;

    if (e.key >= '1' && e.key <= '6') {{
        const key = historyStack[historyStack.length - 1];
        const node = CALL_FLOW[key] || CALL_FLOW["root"];
        const opt = node.options.find(o => o.key === e.key);
        if (opt) pickNext(opt.next);
    }} else if (e.key === 'Backspace') {{
        goBack();
    }} else if (e.key === 'r' || e.key === 'R' || e.key === 'Escape') {{
        resetFlow();
    }} else if (e.key === ' ') {{
        e.preventDefault();
        copyText(getCleanScriptText());
    }}
}});

/* =========================================================================
   BANK SELECTION
   ========================================================================= */
const BANK_SCRIPTS = {{
    "chase": `1. Tell merchant: "Log into Chase.com and click your business checking account."
2. "Click 'Statements & Documents' right below the balance."
3. "Download the last 3 monthly PDFs and forward directly to my email."`,
    "boa": `1. Tell merchant: "Log into Bank of America and click 'Statements & Documents'."
2. "Under Statement Period, download the last 3 closed monthly PDFs."
3. "Forward directly to my email."`,
    "wells": `1. Tell merchant: "Log into Wells Fargo and click 'Statements & Disclosures'."
2. "Download the last 3 monthly PDF statements for your operating account."
3. "Send to my email."`,
    "universal": `1. Tell merchant: "Open your mobile banking app or web portal."
2. "Tap your primary checking account and select 'Statements'."
3. "Export the last 3 monthly PDFs and share to my email."`
}};

function selectBank(bankKey, btn) {{
    document.querySelectorAll('.bank-chip').forEach(el => el.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('bank-guide-text').innerText = BANK_SCRIPTS[bankKey];
}}

/* =========================================================================
   UTILITIES
   ========================================================================= */
function switchTab(tabId) {{
    document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    const target = document.getElementById(tabId);
    if (target) target.classList.add('active');
    const btn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabId));
    if (btn) btn.classList.add('active');
}}

function copyText(text) {{
    navigator.clipboard.writeText(text.trim()).then(() => {{
        const toast = document.getElementById('toast');
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 1500);
    }});
}}

function copySnippet(btn) {{
    const content = btn.parentElement.querySelector('.copy-text').innerText;
    copyText(content);
}}

function runCalc() {{
    const debit = parseFloat(document.getElementById('calc-debit').value) || 0;
    const newPay = parseFloat(document.getElementById('calc-new-pay').value) || 0;
    const advance = parseFloat(document.getElementById('calc-advance').value) || 0;

    const monthlyFreed = Math.max(0, debit - newPay);
    const annualSaved = monthlyFreed * 12;

    document.getElementById('res-monthly').innerText = '+$' + Math.round(monthlyFreed).toLocaleString();
    document.getElementById('res-annual').innerText = '$' + Math.round(annualSaved).toLocaleString();
    document.getElementById('res-capital').innerText = '$' + Math.round(advance).toLocaleString();
}}

function renderObjections() {{
    const container = document.getElementById('objections-list');
    container.innerHTML = OBJECTIONS.map(o => `
        <div style="margin-bottom: 14px; border-bottom: 1px solid var(--border); padding-bottom: 12px;">
            <div style="font-size: 13px; font-weight: 800; color: var(--c-red); margin-bottom: 4px;">⚠️ "${{o.objection}}"</div>
            <div class="copy-box red-box">
                <div class="copy-text">"${{o.rebuttal}}"</div>
                <button class="btn-copy" onclick="copySnippet(this)">Copy</button>
            </div>
            <div style="font-size: 11.5px; color: var(--text-muted); margin-top: 4px;"><strong>Principle:</strong> ${{o.principle}}</div>
        </div>
    `).join('');
}}

function renderPipeline() {{
    const container = document.getElementById('pipeline-list');
    container.innerHTML = STAGES.map(s => `
        <div style="margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 12px;">
            <div style="font-size: 13.5px; font-weight: 800; color: var(--c-blue); margin-bottom: 4px;">Stage ${{s.number}}: ${{s.title}}</div>
            <div style="font-size: 12px; color: var(--text-body); margin-bottom: 8px;"><strong>Goal:</strong> ${{s.objective}}</div>
            <div style="font-size: 11.5px; color: var(--text-muted); margin-bottom: 6px;"><strong>Key Actions:</strong></div>
            <ul style="padding-left: 16px; font-size: 12px; color: var(--text-body);">
                ${{s.actions.map(a => `<li>${{a}}</li>`).join('')}}
            </ul>
        </div>
    `).join('');
}}

window.addEventListener('DOMContentLoaded', () => {{
    const savedTheme = localStorage.getItem('mq_theme') || 'slate';
    applyTheme(savedTheme);
    renderCurrentNode();
    renderObjections();
    renderPipeline();
    runCalc();
    updateCadenceSnippets();
}});
</script>
</body>
</html>"""


def build_complete_pipeline() -> SalesPipelineSystem:
    return SalesPipelineSystem(
        rep_name="Michael Qin",
        title="Merchant Statement & Sales Mastery Flight Deck",
        industry="Commercial Debt Placement & Working Capital Advisory",
        core_thesis="Extract merchant statements on-call, dismantle hesitation with Chris Voss loss-aversion psychology, and run frictionless high-speed closings.",
        stages=[
            PipelineStage(
                number=1,
                title="Lead Sourcing & Merchant Discovery",
                phase_name="Targeting & Enrichment",
                objective="Identify active commercial operators with daily/weekly MCA positions, high processing volume, or upcoming refinancing events.",
                duration="Daily Continuous",
                key_actions=[
                    "Target merchants doing $50K+/month in revenue with active daily debits or merchant processing statements.",
                    "Verify direct owner cell number to bypass gatekeeper loops.",
                    "Score leads on 3 points: Monthly Volume ($50K+), Active Debt/Debits present, Owner reachability."
                ],
                scripts_and_templates={
                    "Pre-Call Sourcing Rule": "Always verify business name, state of filing, and approximate monthly volume before dialing."
                },
                metrics_and_kpis=["50+ direct dials per hour", "15%+ live connection rate"],
                common_pitfalls=["Calling generic landlines instead of verified owner direct lines."]
            ),
            PipelineStage(
                number=2,
                title="The 30-Second Disarm & Hook",
                phase_name="First Touch & Framing",
                objective="Disarm the merchant in 5 seconds, frame call as expense reduction, and establish high-status authority.",
                duration="Days 1–5",
                key_actions=[
                    "Execute the 30-second verbatim opening.",
                    "Pitch debt expense reduction, not new borrowing.",
                    "Position yourself as an institutional diagnostic auditor."
                ],
                scripts_and_templates={
                    "30-Second Opener": "Hey [Name], I will be brief. I know I am calling out of the blue. I work on the commercial capital side, and the reason for the call is simple: we are working with merchants in your industry right now to lower their daily/weekly debits and clean up expensive debt."
                },
                metrics_and_kpis=["35%+ engagement rate on live connections"],
                common_pitfalls=["Sounding like a telemarketer asking for a favor instead of an institutional auditor."]
            ),
            PipelineStage(
                number=3,
                title="45-Second On-Call Statement Extraction",
                phase_name="Intake & Statement Capture",
                objective="Keep merchant on the line and walk them through downloading 3 months of bank statements right now.",
                duration="On-Call (45 Seconds)",
                key_actions=[
                    "Ask: 'Are you in front of your computer or looking at your phone right now?'",
                    "Walk them step-by-step through their bank portal (Chase/BoA/Wells).",
                    "Confirm receipt in your inbox while they are still on the line."
                ],
                scripts_and_templates={
                    "Live Walkthrough": "Stay on the line with me for literally 45 seconds while you export your last 3 monthly statements as PDFs. I will confirm receipt while we're speaking so this isn't hanging over your head after hours."
                },
                metrics_and_kpis=["70%+ on-call statement capture rate from engaged prospects"],
                common_pitfalls=["Accepting 'I'll email it tonight' without attempting the 45-second on-call download."]
            ),
            PipelineStage(
                number=4,
                title="Cash Flow Underwriting & Consolidation Modeling",
                phase_name="Analysis & Term Sheet",
                objective="Model the consolidated cash flow savings showing exact monthly dollars freed up.",
                duration="Under 24 Hours",
                key_actions=[
                    "Calculate total daily/weekly debits vs proposed single monthly payment.",
                    "Calculate net annual cash flow savings.",
                    "Format into a clean 1-page executive benchmark sheet."
                ],
                scripts_and_templates={
                    "Benchmark Summary": "We completed the debt analysis for [Business Name]. By consolidating your daily debits, we free up +$10,500/month in net cash flow, saving $126,000 this year."
                },
                metrics_and_kpis=["100% of benchmark models delivered within 24 hours of statements"],
                common_pitfalls=["Sending complex rate spreadsheets instead of bottom-line monthly cash savings."]
            ),
            PipelineStage(
                number=5,
                title="Term Sheet Presentation & Agreement Lock-In",
                phase_name="Presentation & Closing",
                objective="Walk through the numbers on a 10-minute call, address prepayment/fee questions, and get signed acceptance.",
                duration="24–48 Hours",
                key_actions=[
                    "Lead with net monthly cash freed up.",
                    "Highlight contingent success representation.",
                    "Secure signed placement agreement."
                ],
                scripts_and_templates={
                    "10-Minute Closing Call": "1. Recap merchant's stated cash crunch\n2. Show the net monthly savings delta (+$10,500/mo)\n3. Outline the 48-hour funding timeline\n4. Ask: 'Based on these numbers, does it make sense to lock this in today?'"
                },
                metrics_and_kpis=["50%+ term sheet signature rate"],
                common_pitfalls=["Letting the merchant sit on the term sheet for a week without a scheduled review call."]
            ),
            PipelineStage(
                number=6,
                title="Final Verification & Closing Disbursement",
                phase_name="Processing & Funding",
                objective="Clear stipulations, coordinate closing call, and confirm wire disbursement into merchant account.",
                duration="24–72 Hours",
                key_actions=[
                    "Verify driver's license, voided check, and landlord/utility verification.",
                    "Conduct closing verification call with lender underwriting.",
                    "Track wire confirmation and confirm receipt with merchant."
                ],
                scripts_and_templates={
                    "Closing Update": "All stipulations cleared. Wire has been released and will reflect in your checking account within 2 hours."
                },
                metrics_and_kpis=["Zero last-minute stipulation dropouts"],
                common_pitfalls=["Failing to prepare the merchant for the lender's final verification call."]
            ),
            PipelineStage(
                number=7,
                title="Post-Funding Celebration & Referral Engine",
                phase_name="Retention & Referrals",
                objective="Solidify lifetime advisory relationship and collect 2 peer merchant introductions.",
                duration="Day +1 Post-Funding",
                key_actions=[
                    "Call merchant 30 minutes after wire lands to celebrate.",
                    "Schedule 6-month debt review on calendar.",
                    "Ask for 2 business owner introductions while gratitude is at peak."
                ],
                scripts_and_templates={
                    "Referral Ask": "Hey John, congratulations again on funding! We freed up $10,500/month for you. Who are 1 or 2 other business owners in your network who are getting squeezed by high fees and could use a quick cash flow check like this?"
                },
                metrics_and_kpis=["1.5+ peer referrals per funded transaction"],
                common_pitfalls=["Disappearing after funding and missing the highest-probability referral window."]
            )
        ],
        objections=[
            ObjectionHandler(
                objection="We already have a lender / We don't need money.",
                trigger_stage="Stage 2: Outbound Call",
                rebuttal_script="Completely understand, and I'm glad business is running strong. I'm actually not calling to sell you new debt. Most successful operators we work with aren't looking to borrow—they just want to stop getting squeezed by daily/weekly debits on existing positions. If our audit shows your setup is optimal, at least you keep your lenders honest. If we find $2,000/month in leakage, you keep the cash. What's the best email for that 1-page check?",
                tactical_principle="Reframe from 'borrowing money' to 'stopping expense leakage' and 'keeping incumbent lenders honest'."
            ),
            ObjectionHandler(
                objection="Just email me some information / I'm busy.",
                trigger_stage="Stage 2: Outbound Call",
                rebuttal_script="Happy to do that. Rather than blasting you with generic marketing decks you'll never read, are you in front of your computer or looking at your phone right now? Stay with me for 45 seconds while you click 'Download Statements' on your bank portal. I will confirm receipt on the line so you don't have this on your to-do list tonight. Which bank do you use—Chase, BoA, or Wells?",
                tactical_principle="Do not accept passive brush-offs; immediately invite them to execute the 45-second on-call download."
            ),
            ObjectionHandler(
                objection="Why do you need my bank statements? / Is this secure?",
                trigger_stage="Stage 3: Intake",
                rebuttal_script="Totally understand the caution—your financials are sensitive. We do not shop your file to 20 brokers. We do a direct, in-house preliminary audit to confirm your true monthly volume so we can negotiate institutional terms on your behalf. You can redact your account numbers if you prefer. What is the best email to send the secure link to?",
                tactical_principle="Dissolve security fear by offering account number redaction and highlighting zero-shopping guarantee."
            ),
            ObjectionHandler(
                objection="What are your rates / factor rates?",
                trigger_stage="Stage 2: Outbound Call",
                rebuttal_script="Rates depend entirely on monthly revenue and cash flow, but we are consistently placing capital at terms that cut daily debits in half. To give you an exact rate card rather than a misleading ballpark, shoot over your last 3 monthly statements and I'll deliver your exact terms in 3 hours. What address should I send the doc request to?",
                tactical_principle="Never quote a blind number; trade rate clarity for statements."
            ),
            ObjectionHandler(
                objection="I don't pay broker fees / What is your fee?",
                trigger_stage="Stage 5: Presentation",
                rebuttal_script="Our advisory fee is 100% contingent on success—you pay zero dollars unless we deliver financing on terms you approve that beat your existing alternatives. The monthly cash savings we negotiate in year one alone more than covers the placement, putting net profit in your pocket from day one.",
                tactical_principle="Emphasize zero upfront risk and immediate cash-flow payback."
            )
        ]
    )


def main():
    pipeline_sys = build_complete_pipeline()
    html_content = pipeline_sys.render_portal_html()

    portal_html_path = "index.html"
    with open(portal_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] Successfully generated Twilight Slate portal: {portal_html_path}")

    # Generate PDF
    pdf_out = "michael_qin_sales_pipeline.pdf"
    abs_html = os.path.abspath(portal_html_path)
    abs_pdf = os.path.abspath(pdf_out)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    browser_bin = edge_path if os.path.exists(edge_path) else (chrome_path if os.path.exists(chrome_path) else shutil.which("msedge") or shutil.which("chrome"))

    if browser_bin:
        cmd = [
            browser_bin,
            "--headless",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            f"--print-to-pdf={abs_pdf}",
            f"file:///{abs_html.replace(os.sep, '/')}"
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"[+] Rendered PDF: {pdf_out}")
        except Exception as e:
            print(f"[-] PDF render error: {e}")


if __name__ == "__main__":
    main()
