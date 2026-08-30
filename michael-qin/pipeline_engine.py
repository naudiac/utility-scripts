#!/usr/bin/env python3
"""
Antigravity IDE - Michael Qin's Merchant Statement & Sales Mastery Flight Deck
Telemetry Operations Center & Supervisor Cockpit (Revamped Edition).
Features:
- index.html: Rep Flight Deck with queued IP resolution to eliminate false-positive self-events.
- admin.html: Enterprise Live Supervisor Operations Dashboard with dual SSE+Polling sync, audio chimes, test pings, lead cards, and instant filtering.
"""

import os
import sys
import json
import subprocess
import shutil
from dataclasses import dataclass, field
from typing import List, Dict, Any


TELEMETRY_TOPIC = "ccs_michael_qin_telemetry_wh_2026"
TELEMETRY_ENDPOINT = f"https://ntfy.sh/{TELEMETRY_TOPIC}"


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
<title>Creative Capital Solutions — {self.rep_name} Sales Flight Deck</title>
<style>
    :root {{
        /* ThinkAutomation Corporate Navy Palette */
        --corporate-navy: #0f2744;
        --corporate-blue: #1b4b72;
        --corporate-accent: #2563eb;
        
        --text-main: #1e293b;
        --text-muted: #64748b;
        --text-light: #94a3b8;
        
        --bg-page: #f8fafc;
        --bg-card: #ffffff;
        --bg-subtle: #f1f5f9;
        --border-main: #cbd5e1;
        --border-subtle: #e2e8f0;
        
        /* Semantic Accents */
        --color-success: #166534;
        --color-success-bg: #f0fdf4;
        --color-success-border: #bbf7d0;
        
        --color-warning: #92400e;
        --color-warning-bg: #fffbeb;
        --color-warning-border: #fde68a;
        
        --color-danger: #991b1b;
        --color-danger-bg: #fef2f2;
        --color-danger-border: #fecaca;
        
        --color-purple: #6b21a8;
        --color-purple-bg: #faf5ff;
        --color-purple-border: #e9d5ff;

        --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
    }}

    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        -webkit-tap-highlight-color: transparent;
    }}

    html, body {{
        background-color: var(--bg-page);
        color: var(--text-main);
        font-family: var(--font-family);
        line-height: 1.35;
        font-size: 12.5px;
        -webkit-font-smoothing: antialiased;
        min-height: 100vh;
        overflow-x: hidden;
    }}

    .app-container {{
        width: 100%;
        max-width: 1280px;
        margin: 0 auto;
        padding: 6px 8px;
        display: flex;
        flex-direction: column;
    }}

    /* =========================================================================
       HEADER BAR (RESPONSIVE)
       ========================================================================= */
    .top-header {{
        background: var(--bg-card);
        border: 1px solid var(--border-main);
        border-top: 3px solid var(--corporate-navy);
        padding: 6px 8px;
        margin-bottom: 6px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }}

    .header-row-1 {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 6px;
        margin-bottom: 4px;
    }}

    .brand-block {{
        display: flex;
        align-items: center;
        gap: 5px;
        white-space: nowrap;
    }}
    .brand-title {{
        font-size: 14px;
        font-weight: 800;
        color: var(--corporate-navy);
        letter-spacing: -0.2px;
    }}
    .status-tag {{
        font-size: 8.5px;
        font-weight: 700;
        padding: 1px 4px;
        border-radius: 2px;
        text-transform: uppercase;
        background: #dcfce7;
        color: #166534;
        border: 1px solid #bbf7d0;
    }}
    .rep-tag {{
        font-size: 10.5px;
        color: var(--text-muted);
        font-weight: 600;
    }}

    .btn-share-top {{
        background: var(--corporate-navy);
        color: #ffffff;
        border: 1px solid var(--corporate-navy);
        padding: 4px 8px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: 700;
        cursor: pointer;
        white-space: nowrap;
        display: inline-flex;
        align-items: center;
        gap: 3px;
    }}

    /* Lead Inputs Row */
    .lead-inputs-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr auto;
        gap: 4px;
        align-items: center;
    }}
    @media (max-width: 500px) {{
        .lead-inputs-grid {{
            grid-template-columns: 1fr 1fr 1fr auto;
            gap: 3px;
        }}
    }}

    .lead-input-compact {{
        width: 100%;
        background: var(--bg-subtle);
        border: 1px solid var(--border-main);
        color: var(--corporate-navy);
        padding: 4px 6px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: 600;
        outline: none;
    }}
    .lead-input-compact:focus {{
        border-color: var(--corporate-accent);
        background: #ffffff;
    }}
    .btn-clear-compact {{
        background: var(--bg-subtle);
        border: 1px solid var(--border-main);
        color: var(--text-muted);
        padding: 4px 6px;
        border-radius: 3px;
        font-size: 10px;
        font-weight: 700;
        cursor: pointer;
    }}

    /* Tone Selector Row */
    .tone-row {{
        display: flex;
        align-items: center;
        gap: 4px;
        margin-top: 5px;
        padding-top: 4px;
        border-top: 1px solid var(--border-subtle);
        overflow-x: auto;
        scrollbar-width: none;
    }}
    .tone-row::-webkit-scrollbar {{ display: none; }}
    
    .tone-lbl {{
        font-size: 9px;
        font-weight: 800;
        text-transform: uppercase;
        color: var(--text-muted);
        white-space: nowrap;
    }}
    .tone-chips {{
        display: flex;
        gap: 3px;
    }}
    .tone-chip {{
        background: var(--bg-subtle);
        border: 1px solid var(--border-main);
        color: var(--text-muted);
        font-size: 10.5px;
        font-weight: 600;
        padding: 2px 6px;
        border-radius: 3px;
        cursor: pointer;
        white-space: nowrap;
    }}
    .tone-chip:hover {{ color: var(--corporate-navy); border-color: var(--corporate-accent); }}
    .tone-chip.active {{
        background: var(--corporate-navy);
        border-color: var(--corporate-navy);
        color: #ffffff;
        font-weight: 700;
    }}

    .industry-presets-row {{
        display: flex;
        align-items: center;
        gap: 4px;
        margin-bottom: 4px;
        overflow-x: auto;
        padding-bottom: 2px;
        white-space: nowrap;
        scrollbar-width: none;
    }}
    .industry-presets-row::-webkit-scrollbar {{ display: none; }}
    .industry-lbl {{
        font-size: 9.5px;
        font-weight: 800;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.3px;
        flex-shrink: 0;
    }}
    .industry-chips {{
        display: flex;
        gap: 3px;
        flex-wrap: nowrap;
    }}
    .industry-chip {{
        background: #ffffff;
        border: 1px solid var(--border-main);
        color: var(--corporate-navy);
        font-size: 10px;
        font-weight: 600;
        padding: 2px 6px;
        border-radius: 2px;
        cursor: pointer;
        transition: all 0.1s;
        flex-shrink: 0;
        touch-action: manipulation;
    }}
    .industry-chip:hover {{
        background: #f1f5f9;
        border-color: var(--corporate-accent);
    }}
    .industry-chip.active {{
        background: var(--corporate-navy);
        color: #ffffff;
        border-color: var(--corporate-navy);
    }}

    .extra-intel-btn {{
        margin-left: auto;
        background: none;
        border: none;
        color: var(--corporate-accent);
        font-size: 9.5px;
        font-weight: 700;
        cursor: pointer;
        white-space: nowrap;
    }}

    /* Extra Intel Drawer */
    .intel-drawer {{
        display: none;
        margin-top: 4px;
        padding: 6px;
        background: var(--bg-subtle);
        border: 1px solid var(--border-subtle);
        border-radius: 3px;
    }}
    .intel-drawer.open {{ display: block; }}
    .intel-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
        gap: 4px;
    }}
    .intel-cheat-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 4px;
        margin-top: 5px;
        padding-top: 5px;
        border-top: 1px dashed var(--border-subtle);
    }}
    .intel-cheat-card {{
        background: #ffffff;
        border: 1px solid var(--border-subtle);
        border-left: 3px solid var(--corporate-navy);
        padding: 4px 6px;
        border-radius: 2px;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        gap: 1px;
        transition: all 0.1s;
    }}
    .intel-cheat-card:hover {{
        border-left-color: var(--corporate-accent);
        background: #f8fafc;
    }}
    .cheat-title {{
        font-size: 10px;
        font-weight: 700;
        color: var(--corporate-navy);
    }}
    .cheat-cue {{
        font-size: 9px;
        color: var(--text-muted);
    }}
    .cheat-hook {{
        font-size: 9px;
        font-style: italic;
        color: var(--color-success);
    }}

    /* Navigation Tabs */
    .tabs-nav {{
        display: flex;
        gap: 2px;
        border-bottom: 2px solid var(--border-main);
        margin-bottom: 6px;
        overflow-x: auto;
        scrollbar-width: none;
    }}
    .tabs-nav::-webkit-scrollbar {{ display: none; }}
    
    .tab-item {{
        background: var(--bg-subtle);
        border: 1px solid var(--border-main);
        border-bottom: none;
        color: var(--text-muted);
        font-size: 11px;
        font-weight: 600;
        padding: 4px 8px;
        border-radius: 3px 3px 0 0;
        cursor: pointer;
        white-space: nowrap;
    }}
    .tab-item:hover {{ color: var(--corporate-navy); }}
    .tab-item.active {{
        background: #ffffff;
        color: var(--corporate-navy);
        border-top: 2.5px solid var(--corporate-navy);
        border-bottom: 2px solid #ffffff;
        margin-bottom: -2px;
        font-weight: 700;
    }}

    .tab-pane {{ display: none; }}
    .tab-pane.active {{ display: block; }}

    /* =========================================================================
       DIALER COPILOT - ZERO SCROLL LAYOUT
       ========================================================================= */
    .cockpit-grid {{
        display: grid;
        grid-template-columns: 1.15fr 1fr;
        gap: 8px;
    }}
    @media (max-width: 768px) {{
        .cockpit-grid {{
            grid-template-columns: 1fr;
            gap: 6px;
        }}
    }}

    .cockpit-left, .cockpit-right {{
        background: var(--bg-card);
        border: 1px solid var(--border-main);
        padding: 8px 10px;
        display: flex;
        flex-direction: column;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }}

    .cockpit-title-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 5px;
        padding-bottom: 3px;
        border-bottom: 1px solid var(--border-subtle);
    }}
    .cockpit-title {{
        font-size: 11px;
        font-weight: 800;
        color: var(--corporate-navy);
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }}
    .cockpit-meta {{
        font-family: var(--font-mono);
        font-size: 9.5px;
        color: var(--text-muted);
    }}

    /* Verbatim Speech Box */
    .say-box {{
        background: #f8fafc;
        border: 1px solid var(--border-subtle);
        border-left: 3.5px solid var(--corporate-accent);
        padding: 8px 10px;
        border-radius: 2px;
    }}
    .say-header-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
    }}
    .say-lbl {{
        font-size: 9px;
        font-weight: 800;
        text-transform: uppercase;
        color: var(--corporate-accent);
        letter-spacing: 0.5px;
    }}
    .tone-badge {{
        font-size: 9px;
        font-weight: 700;
        color: var(--corporate-navy);
        background: #e2e8f0;
        padding: 1px 4px;
        border-radius: 2px;
        font-family: var(--font-mono);
    }}

    .say-text {{
        font-size: 14.5px;
        font-weight: 600;
        color: var(--corporate-navy);
        line-height: 1.4;
        white-space: pre-wrap;
        margin-bottom: 6px;
    }}
    @media (max-width: 600px) {{
        .say-text {{ font-size: 13.5px; line-height: 1.35; }}
    }}
    .say-text .token-highlight {{
        background: #fef3c7;
        color: #92400e;
        padding: 0 3px;
        border-radius: 2px;
        font-weight: 700;
    }}

    .tactical-bar {{
        background: var(--color-purple-bg);
        border: 1px solid var(--color-purple-border);
        border-left: 3px solid var(--color-purple);
        padding: 4px 6px;
        font-size: 10px;
        color: var(--color-purple);
        border-radius: 2px;
    }}

    /* Action Toolbar */
    .cockpit-action-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 6px;
        padding-top: 4px;
        border-top: 1px solid var(--border-subtle);
    }}
    .btn-ctrl {{
        background: var(--bg-subtle);
        border: 1px solid var(--border-main);
        color: var(--text-main);
        padding: 3px 7px;
        border-radius: 2px;
        font-size: 10px;
        font-weight: 600;
        cursor: pointer;
    }}
    .btn-ctrl:hover {{ background: #e2e8f0; }}

    /* Reaction Options */
    .options-stack {{
        display: flex;
        flex-direction: column;
        gap: 4px;
    }}
    @media (max-width: 768px) {{
        .options-stack {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4px;
        }}
    }}

    .opt-btn {{
        background: #ffffff;
        border: 1px solid var(--border-main);
        padding: 6px 8px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: 600;
        text-align: left;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.05s, box-shadow 0.1s;
        touch-action: manipulation;
        -webkit-tap-highlight-color: transparent;
    }}
    .opt-btn * {{
        pointer-events: none;
    }}
    .opt-btn:hover {{ box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
    .opt-btn:active {{ transform: scale(0.98); background: #f1f5f9; }}

    .opt-btn.pos {{
        background: var(--color-success-bg);
        border-color: var(--color-success-border);
        color: var(--color-success);
    }}
    .opt-btn.pos .key-pill {{ background: var(--color-success); color: #ffffff; }}

    .opt-btn.neg {{
        background: var(--color-danger-bg);
        border-color: var(--color-danger-border);
        color: var(--color-danger);
    }}
    .opt-btn.neg .key-pill {{ background: var(--color-danger); color: #ffffff; }}

    .opt-btn.amber {{
        background: var(--color-warning-bg);
        border-color: var(--color-warning-border);
        color: var(--color-warning);
    }}
    .opt-btn.amber .key-pill {{ background: var(--color-warning); color: #ffffff; }}

    .key-pill {{
        font-family: var(--font-mono);
        font-size: 9.5px;
        font-weight: 800;
        padding: 1px 4px;
        border-radius: 2px;
        margin-left: 4px;
        flex-shrink: 0;
    }}

    /* General Cards for Other Tabs */
    .section-block {{
        background: var(--bg-card);
        border: 1px solid var(--border-main);
        padding: 12px;
        margin-bottom: 8px;
    }}
    .section-header-row {{
        font-size: 12px;
        font-weight: 700;
        color: var(--corporate-navy);
        text-transform: uppercase;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
    }}

    .copy-block {{
        background: #f8fafc;
        border: 1px solid var(--border-subtle);
        border-left: 3.5px solid var(--corporate-accent);
        border-radius: 3px;
        padding: 8px 10px;
        margin: 5px 0 8px 0;
        position: relative;
    }}
    .copy-block.green-box {{ border-left-color: var(--color-success); background: var(--color-success-bg); }}
    .copy-block.red-box {{ border-left-color: var(--color-danger); background: var(--color-danger-bg); }}
    .copy-block.yellow-box {{ border-left-color: var(--color-warning); background: var(--color-warning-bg); }}

    .copy-text {{
        font-size: 11.5px;
        color: var(--text-main);
        white-space: pre-wrap;
        line-height: 1.4;
    }}
    .btn-copy {{
        position: absolute;
        top: 4px;
        right: 4px;
        background: #ffffff;
        border: 1px solid var(--border-main);
        color: var(--text-muted);
        font-size: 9px;
        font-weight: 600;
        padding: 1px 4px;
        border-radius: 2px;
        cursor: pointer;
    }}

    .bank-chips {{
        display: flex;
        gap: 3px;
        margin-bottom: 6px;
        overflow-x: auto;
    }}
    .bank-chip {{
        background: var(--bg-subtle);
        border: 1px solid var(--border-main);
        color: var(--text-muted);
        padding: 3px 7px;
        border-radius: 3px;
        font-size: 10px;
        font-weight: 600;
        cursor: pointer;
    }}
    .bank-chip.active {{
        background: var(--corporate-navy);
        border-color: var(--corporate-navy);
        color: #ffffff;
    }}

    /* Calculator */
    .calc-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 6px;
        margin-bottom: 6px;
    }}
    .calc-cell label {{
        display: block;
        font-size: 9px;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        margin-bottom: 1px;
    }}
    .calc-cell input {{
        width: 100%;
        background: #ffffff;
        border: 1px solid var(--border-main);
        color: var(--corporate-navy);
        padding: 4px 6px;
        border-radius: 3px;
        font-family: var(--font-mono);
        font-size: 11.5px;
        font-weight: 600;
    }}

    .calc-summary {{
        background: var(--bg-subtle);
        border: 1px solid var(--border-main);
        border-radius: 3px;
        padding: 6px;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 4px;
        text-align: center;
    }}
    .calc-val {{
        font-size: 14px;
        font-weight: 800;
        font-family: var(--font-mono);
    }}
    .calc-lbl {{
        font-size: 8.5px;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
    }}

    /* Modal */
    .modal-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(15, 39, 68, 0.65);
        backdrop-filter: blur(3px);
        z-index: 1000;
        display: none;
        align-items: center;
        justify-content: center;
        padding: 10px;
    }}
    .modal-overlay.open {{ display: flex; }}
    .modal-content {{
        background: #ffffff;
        border: 1px solid var(--border-main);
        border-top: 4px solid var(--corporate-navy);
        border-radius: 4px;
        max-width: 380px;
        width: 100%;
        padding: 14px;
        position: relative;
    }}
    .modal-close {{
        position: absolute;
        top: 6px;
        right: 6px;
        background: var(--bg-subtle);
        border: 1px solid var(--border-main);
        font-size: 11px;
        font-weight: 700;
        width: 20px;
        height: 20px;
        border-radius: 3px;
        cursor: pointer;
    }}

    .qr-box {{
        background: #f8fafc;
        border: 1px solid var(--border-subtle);
        padding: 6px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 3px;
        margin: 6px 0;
    }}
    .qr-img {{
        width: 120px;
        height: 120px;
        background: #fff;
        padding: 3px;
        border: 1px solid var(--border-main);
    }}

    /* Toast */
    .toast {{
        position: fixed;
        bottom: 12px;
        right: 12px;
        background: var(--corporate-navy);
        color: #ffffff;
        font-weight: 600;
        font-size: 10.5px;
        padding: 4px 8px;
        border-radius: 2px;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.15s ease;
        z-index: 2000;
    }}
    .toast.show {{ opacity: 1; }}

    @media (max-width: 768px) {{
        .app-container {{
            padding: 4px 2px;
        }}
        .top-header {{
            padding: 6px 8px;
            margin-bottom: 4px;
        }}
        .header-row-1 {{
            margin-bottom: 4px;
        }}
        
        /* Vertical Presets: 3x2 Grid on Mobile */
        .industry-presets-row {{
            flex-direction: column;
            align-items: stretch;
            gap: 2px;
            margin-bottom: 4px;
        }}
        .industry-chips {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 3px;
            width: 100%;
        }}
        .industry-chip {{
            text-align: center;
            padding: 5px 2px;
            font-size: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        /* Lead Inputs: 2x2 Grid on Mobile */
        .lead-inputs-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4px;
            margin-bottom: 4px;
        }}
        .lead-input-compact {{
            padding: 6px 8px;
            font-size: 11.5px;
        }}
        .btn-clear-compact {{
            padding: 6px 8px;
            font-size: 11px;
            font-weight: 700;
        }}

        /* Tone Chips: 3x2 Grid on Mobile */
        .tone-row {{
            flex-direction: column;
            align-items: stretch;
            gap: 3px;
            padding-top: 4px;
            margin-top: 4px;
        }}
        .tone-chips {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
            gap: 3px;
            width: 100%;
        }}
        .tone-chip {{
            text-align: center;
            padding: 5px 2px;
            font-size: 9.5px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .extra-intel-btn {{
            align-self: flex-end;
            margin-top: -2px;
            padding: 2px 4px;
        }}

        /* Navigation Tabs: 2x2 compact grid */
        .tabs-nav {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 3px;
            border-bottom: none;
            margin-bottom: 6px;
        }}
        .tab-item {{
            text-align: center;
            padding: 6px 4px;
            border-radius: 3px;
            border: 1px solid var(--border-main);
            font-size: 10.5px;
            white-space: normal;
        }}
        .tab-item.active {{
            background: var(--corporate-navy);
            color: #ffffff;
            border-color: var(--corporate-navy);
            margin-bottom: 0;
        }}

        /* Reaction Buttons on Mobile */
        .options-stack {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4px;
        }}
        .opt-btn {{
            padding: 7px 6px;
            font-size: 11px;
            line-height: 1.25;
            min-height: 42px;
        }}

        .say-text {{
            font-size: 13.5px;
            line-height: 1.35;
        }}
    }}

    @media print {{
        .tabs-nav, .btn-ctrl, .btn-copy, .btn-clear-compact, .btn-share-top, .modal-overlay, .tone-row {{ display: none !important; }}
        body {{ background: #fff; color: #000; }}
        .cockpit-grid {{ display: block; }}
    }}
</style>
</head>
<body>

<div class="app-container">

    <!-- Compact Executive Header -->
    <div class="top-header">
        <div class="header-row-1">
            <div class="brand-block">
                <span class="brand-title">Creative Capital Solutions</span>
                <span class="status-tag">Live</span>
                <span class="rep-tag">{self.rep_name}</span>
            </div>
            <button class="btn-share-top" onclick="openShareModal()">🔗 Share</button>
        </div>

        <!-- Target Vertical Quick Presets -->
        <div class="industry-presets-row">
            <span class="industry-lbl">⚡ Vertical:</span>
            <div class="industry-chips">
                <button class="industry-chip" onclick="applyIndustryPreset('contractor')">🛠️ Construction</button>
                <button class="industry-chip" onclick="applyIndustryPreset('trucking')">🚛 Trucking</button>
                <button class="industry-chip" onclick="applyIndustryPreset('restaurant')">🍽️ Restaurant</button>
                <button class="industry-chip" onclick="applyIndustryPreset('medical')">🏥 Healthcare</button>
                <button class="industry-chip" onclick="applyIndustryPreset('manufacturing')">🏭 Manufacturing</button>
                <button class="industry-chip" onclick="applyIndustryPreset('retail')">🛒 Auto &amp; Retail</button>
            </div>
        </div>

        <!-- 3 Inline Lead Inputs -->
        <div class="lead-inputs-grid">
            <input type="text" id="lead-name" class="lead-input-compact" placeholder="Contact Name" oninput="updatePersonalization()">
            <input type="text" id="lead-company" class="lead-input-compact" placeholder="Company Name" oninput="updatePersonalization()">
            <input type="text" id="lead-industry" class="lead-input-compact" placeholder="Industry / Niche" oninput="updatePersonalization()">
            <button class="btn-clear-compact" onclick="clearLeadInputs()">✕</button>
        </div>

        <!-- Tone Selector Row -->
        <div class="tone-row">
            <span class="tone-lbl">🎭 Tone:</span>
            <div class="tone-chips" id="tone-chips-container">
                <button class="tone-chip active" onclick="setTone('belfort_straight_line', this)">🐺 Straight Line</button>
                <button class="tone-chip" onclick="setTone('voss_empathy', this)">🕵️ Voss (Empathy)</button>
                <button class="tone-chip" onclick="setTone('klaff_frame', this)">🧠 Klaff (Frames)</button>
                <button class="tone-chip" onclick="setTone('cardone_10x', this)">⚡ Cardone (10X)</button>
                <button class="tone-chip" onclick="setTone('challenger_sale', this)">📊 Challenger</button>
                <button class="tone-chip" onclick="setTone('cialdini_authority', this)">👑 Cialdini</button>
                <button class="tone-chip" onclick="setTone('ziglar_relational', this)">🤠 Ziglar</button>
            </div>
            <button class="extra-intel-btn" onclick="toggleIntelDrawer()">➕ Intel</button>
        </div>

        <!-- Collapsible Intel Drawer -->
        <div class="intel-drawer" id="intel-drawer">
            <div class="intel-grid">
                <input type="text" id="lead-lender" class="lead-input-compact" placeholder="Lender (e.g. OnDeck)" oninput="updatePersonalization()">
                <input type="text" id="lead-rev" class="lead-input-compact" placeholder="Est. Rev (e.g. $120K/mo)" oninput="updatePersonalization()">
                <input type="text" id="lead-debit-str" class="lead-input-compact" placeholder="Debits (e.g. $1,200/day)" oninput="updatePersonalization()">
                <input type="text" id="lead-notes" class="lead-input-compact" placeholder="Sticky Note / Cue" oninput="updatePersonalization()">
            </div>
            <div class="intel-cheat-grid">
                <div class="intel-cheat-card" onclick="applyIndustryPreset('contractor')">
                    <span class="cheat-title">🛠️ Contractors &amp; Trades</span>
                    <span class="cheat-cue">Pain: 60-90 day GC progress draws &amp; material prepayments</span>
                    <span class="cheat-hook">Hook: "Stop daily debits while waiting on the general contractor's check."</span>
                </div>
                <div class="intel-cheat-card" onclick="applyIndustryPreset('trucking')">
                    <span class="cheat-title">🚛 Trucking &amp; Logistics</span>
                    <span class="cheat-cue">Pain: Diesel fuel card debits &amp; 45-day broker payables</span>
                    <span class="cheat-hook">Hook: "Bridge slow broker payables without predatory factoring cuts."</span>
                </div>
                <div class="intel-cheat-card" onclick="applyIndustryPreset('restaurant')">
                    <span class="cheat-title">🍽️ Restaurants &amp; Food Service</span>
                    <span class="cheat-cue">Pain: POS credit card batch holds &amp; inventory lulls</span>
                    <span class="cheat-hook">Hook: "Keep 100% of your busy weekend card receipts."</span>
                </div>
                <div class="intel-cheat-card" onclick="applyIndustryPreset('medical')">
                    <span class="cheat-title">🏥 Healthcare &amp; Dental</span>
                    <span class="cheat-cue">Pain: 60-day insurance reimbursement float</span>
                    <span class="cheat-hook">Hook: "Smooth out insurance claim delays with zero personal collateral."</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs-nav">
        <button class="tab-item active" onclick="switchTab('tab-hud')">🎙️ Dialer Copilot</button>
        <button class="tab-item" onclick="switchTab('tab-custom-decks')">🛠️ Custom Decks</button>
        <button class="tab-item" onclick="switchTab('tab-statement')">📄 Statements (45s)</button>
        <button class="tab-item" onclick="switchTab('tab-calc')">💰 Savings Calc</button>
        <button class="tab-item" onclick="switchTab('tab-objections')">🛡️ Pushbacks</button>
        <button class="tab-item" onclick="switchTab('tab-cadence')">📬 SMS Follow-Ups</button>
        <button class="tab-item" onclick="switchTab('tab-pipeline')">🚀 7-Stage Pipeline</button>
    </div>

    <!-- TAB 1: DIALER COPILOT -->
    <div id="tab-hud" class="tab-pane active">
        <div class="cockpit-grid">
            
            <!-- LEFT PANEL: WHAT YOU SAY -->
            <div class="cockpit-left">
                <div class="cockpit-title-row">
                    <span class="cockpit-title" id="hud-stage">Stage 1: Opening (0-5s)</span>
                    <span class="cockpit-meta" id="hud-step">Step 1 of 4</span>
                </div>

                <!-- Sticky Call Note Banner -->
                <div id="sticky-note-box" style="display:none; background:#fffbeb; border:1px solid #fde68a; padding:3px 5px; font-size:10px; color:#92400e; margin-bottom:4px; border-radius:2px;">
                    <strong>📌 Note:</strong> <span id="sticky-note-text"></span>
                </div>

                <div class="say-box">
                    <div>
                        <div class="say-header-row">
                            <span class="say-lbl">🗣️ What You Say Out Loud (Verbatim)</span>
                            <span class="tone-badge" id="active-tone-label">Wall Street</span>
                        </div>
                        <div class="say-text" id="hud-verbatim"></div>
                    </div>
                    <div class="tactical-bar" id="hud-bar">
                        <strong>Tactical Execution:</strong> <span id="hud-tactical"></span>
                    </div>
                </div>

                <div class="cockpit-action-bar">
                    <button class="btn-ctrl" onclick="goBack()" id="btn-back" style="display:none;">⬅ Back</button>
                    <div style="display: flex; gap: 4px; margin-left: auto;">
                        <button class="btn-ctrl" onclick="copyText(getCleanScriptText())">📋 Copy (Space)</button>
                        <button class="btn-ctrl" onclick="resetFlow()">🔄 Reset Call (R)</button>
                    </div>
                </div>
            </div>

            <!-- RIGHT PANEL: PROSPECT REACTIONS -->
            <div class="cockpit-right">
                <div class="cockpit-title-row">
                    <span class="cockpit-title">👉 Prospect Reactions</span>
                    <span class="cockpit-meta">Press [1-6] or Tap</span>
                </div>

                <div class="options-stack" id="hud-options">
                    <!-- Injected Dynamically -->
                </div>
            </div>

        </div>
    </div>

    <!-- TAB 2: CUSTOM DECK STUDIO -->
    <div id="tab-custom-decks" class="tab-pane">
        <div class="section-block">
            <div class="section-header-row">
                <span>🛠️ Custom Deck Studio &amp; Pitch Builder</span>
            </div>
            <p style="font-size: 11px; color: var(--text-muted); margin-bottom: 6px;">
                Build custom pitch decks saved directly in your browser.
            </p>
            <div style="display:grid; gap:5px;">
                <input type="text" id="new-deck-name" class="lead-input-compact" placeholder="Deck Name (e.g. Florida Contractors Opener)">
                <textarea id="new-deck-opener" style="width:100%; min-height:50px; padding:5px 6px; border:1px solid var(--border-main); font-size:11px;" placeholder="Opener line (Use [Name], [Company], [Industry])"></textarea>
                <textarea id="new-deck-hook" style="width:100%; min-height:40px; padding:5px 6px; border:1px solid var(--border-main); font-size:11px;" placeholder="Hook & Disarm Line"></textarea>
                <input type="text" id="new-deck-note" class="lead-input-compact" placeholder="Delivery Note">
                <button class="btn-share-top" style="justify-content:center; padding:5px;" onclick="saveCustomDeck()">💾 Save Custom Deck</button>
            </div>
            <div style="font-size:11px; font-weight:700; color:var(--corporate-navy); margin:8px 0 3px;">Saved Custom Decks:</div>
            <div id="custom-decks-container"></div>
        </div>
    </div>

    <!-- TAB 3: STATEMENT EXTRACTION -->
    <div id="tab-statement" class="tab-pane">
        <div class="section-block">
            <div class="section-header-row">
                <span>🚀 45-Second On-Call Statement Extraction</span>
            </div>
            <div class="copy-block green-box">
                <div style="font-size: 9.5px; font-weight: 700; color: var(--color-success); text-transform: uppercase; margin-bottom: 2px;">Live Walkthrough Script</div>
                <div class="copy-text" id="stmt-walkthrough-text"></div>
                <button class="btn-copy" onclick="copySnippet(this)">Copy</button>
            </div>

            <div style="font-size: 9.5px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin: 5px 0 2px;">Bank 2-Click Guides:</div>
            <div class="bank-chips">
                <button class="bank-chip active" onclick="selectBank('chase', this)">Chase Business</button>
                <button class="bank-chip" onclick="selectBank('boa', this)">Bank of America</button>
                <button class="bank-chip" onclick="selectBank('wells', this)">Wells Fargo</button>
                <button class="bank-chip" onclick="selectBank('universal', this)">Universal Mobile</button>
            </div>

            <div class="copy-block">
                <div class="copy-text" id="bank-guide-text">1. Tell merchant: "Log into Chase.com and click your business checking account."
2. "Click 'Statements & Documents' right below the balance."
3. "Download the last 3 monthly PDFs and forward directly to my email."</div>
                <button class="btn-copy" onclick="copySnippet(this)">Copy</button>
            </div>

            <div class="copy-block yellow-box">
                <div style="font-size: 9.5px; font-weight: 700; color: var(--color-warning); text-transform: uppercase; margin-bottom: 2px;">Chris Voss Loss-Aversion Rebuttal</div>
                <div class="copy-text" id="loss-aversion-text"></div>
                <button class="btn-copy" onclick="copySnippet(this)">Copy</button>
            </div>
        </div>
    </div>

    <!-- TAB 4: SAVINGS CALCULATOR -->
    <div id="tab-calc" class="tab-pane">
        <div class="section-block">
            <div class="section-header-row">
                <span>💰 Live Debt Restructuring Calculator</span>
            </div>
            <div class="calc-grid">
                <div class="calc-cell">
                    <label>Monthly Revenue ($)</label>
                    <input type="number" id="calc-rev" value="120000" step="5000" oninput="runCalc()">
                </div>
                <div class="calc-cell">
                    <label>Current Debits ($/Mo)</label>
                    <input type="number" id="calc-debit" value="18000" step="1000" oninput="runCalc()">
                </div>
                <div class="calc-cell">
                    <label>New Payment ($/Mo)</label>
                    <input type="number" id="calc-new-pay" value="7500" step="500" oninput="runCalc()">
                </div>
                <div class="calc-cell">
                    <label>New Capital ($)</label>
                    <input type="number" id="calc-advance" value="150000" step="10000" oninput="runCalc()">
                </div>
            </div>

            <div class="calc-summary">
                <div>
                    <div class="calc-val" id="res-monthly" style="color: var(--color-success);">+$10,500</div>
                    <div class="calc-lbl">Monthly Cash Freed</div>
                </div>
                <div>
                    <div class="calc-val" id="res-annual" style="color: var(--corporate-accent);">$126,000</div>
                    <div class="calc-lbl">Annual Savings</div>
                </div>
                <div>
                    <div class="calc-val" id="res-capital" style="color: var(--color-purple);">$150,000</div>
                    <div class="calc-lbl">Liquidity Unlocked</div>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 5: PUSHBACK MATRIX -->
    <div id="tab-objections" class="tab-pane">
        <div class="section-block">
            <div class="section-header-row">
                <span>🛡️ Pushback &amp; Objection Rebuttals</span>
            </div>
            <div id="objections-list"></div>
        </div>
    </div>

    <!-- TAB 6: CADENCE -->
    <div id="tab-cadence" class="tab-pane">
        <div class="section-block">
            <div class="section-header-row">
                <span>📬 Multi-Touch SMS &amp; Email Cadence</span>
            </div>
            <div class="copy-block green-box">
                <div style="font-size: 9px; font-weight: 700; color: var(--color-success); text-transform: uppercase;">Day 1: Instant Post-Call SMS</div>
                <div class="copy-text" id="cadence-sms1"></div>
                <button class="btn-copy" onclick="copySnippet(this)">Copy</button>
            </div>
            <div class="copy-block yellow-box">
                <div style="font-size: 9px; font-weight: 700; color: var(--color-warning); text-transform: uppercase;">Day 3: Midday Leakage Check-In</div>
                <div class="copy-text" id="cadence-email1"></div>
                <button class="btn-copy" onclick="copySnippet(this)">Copy</button>
            </div>
            <div class="copy-block red-box">
                <div style="font-size: 9px; font-weight: 700; color: var(--color-danger); text-transform: uppercase;">Day 8: Permission-to-Close Breakup</div>
                <div class="copy-text" id="cadence-email2"></div>
                <button class="btn-copy" onclick="copySnippet(this)">Copy</button>
            </div>
        </div>
    </div>

    <!-- TAB 7: PIPELINE STAGES -->
    <div id="tab-pipeline" class="tab-pane">
        <div class="section-block">
            <div class="section-header-row">
                <span>🚀 Complete 7-Stage Pipeline Guide</span>
            </div>
            <div id="pipeline-list"></div>
        </div>
    </div>

</div>

<!-- SHARE MODAL -->
<div id="share-modal" class="modal-overlay" onclick="closeShareModal(event)">
    <div class="modal-content" onclick="event.stopPropagation()">
        <button class="modal-close" onclick="closeShareModal()">✕</button>
        <div style="font-size:12.5px; font-weight:800; color:var(--corporate-navy); margin-bottom:2px;">📲 Add to Any Device / Create Link</div>
        <div style="font-size:10.5px; color:var(--text-muted); margin-bottom:6px;">Instant access on iPhone, Android, or PC.</div>

        <div class="qr-box">
            <img class="qr-img" alt="QR Code" src="https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=https://naudiac.github.io/utility-scripts/michael-qin/">
            <span style="font-size:9.5px; font-weight:700; color:var(--corporate-navy);">📷 Scan with Phone Camera to Open</span>
        </div>

        <div style="display:flex; gap:3px; margin-bottom:6px;">
            <input type="text" id="share-url-box" class="lead-input-compact" readonly value="https://naudiac.github.io/utility-scripts/michael-qin/">
            <button class="btn-share-top" onclick="copyToolUrl()">📋 Copy</button>
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px; font-size:9.5px;">
            <div style="background:var(--bg-subtle); padding:4px; border-radius:2px;">
                <strong>📱 iPhone:</strong> Share ➔ 'Add to Home'
            </div>
            <div style="background:var(--bg-subtle); padding:4px; border-radius:2px;">
                <strong>🤖 Android:</strong> 3-Dots ➔ 'Add to Home'
            </div>
        </div>
    </div>
</div>

<div id="toast" class="toast">Copied to clipboard</div>

<script>
const STAGES = {stages_json};
const OBJECTIONS = {objections_json};
const TELEMETRY_URL = "{TELEMETRY_ENDPOINT}";

/* =========================================================================
   SILENT REAL-TIME TELEMETRY TRACKER (SUPERVISOR SYNC & IP EXCLUSION)
   ========================================================================= */
const repSessionId = 'rep_' + Math.random().toString(36).substring(2, 9);
const deviceType = /iPhone|iPad|iPod/i.test(navigator.userAgent) ? 'iPhone' :
                   /Android/i.test(navigator.userAgent) ? 'Android' :
                   /Mac/i.test(navigator.userAgent) ? 'Mac' : 'Windows PC';

const SUPERVISOR_IPS = ['85.115.107.223', '74.209.76.220'];
let isSupervisorUser = (
    window.location.search.includes('supervisor=') ||
    window.location.search.includes('admin=true') ||
    localStorage.getItem('ccs_is_supervisor') === 'true'
);

let userIpResolved = false;
let userIpInfo = {{ ip: 'Pending', city: '', region: '' }};
let telemetryQueue = [];

// Resolve IP
fetch('https://ipapi.co/json/').then(r => r.json()).then(data => {{
    if (data && data.ip) {{
        userIpInfo = {{ ip: data.ip, city: data.city || '', region: data.region_code || '' }};
        userIpResolved = true;
        if (SUPERVISOR_IPS.includes(data.ip)) {{
            isSupervisorUser = true;
        }}
        flushTelemetryQueue();
    }}
}}).catch(() => {{
    fetch('https://api.ipify.org?format=json').then(r => r.json()).then(data => {{
        if (data && data.ip) {{
            userIpInfo.ip = data.ip;
            userIpResolved = true;
            if (SUPERVISOR_IPS.includes(data.ip)) {{
                isSupervisorUser = true;
            }}
            flushTelemetryQueue();
        }}
    }}).catch(() => {{
        userIpResolved = true;
        flushTelemetryQueue();
    }});
}});

function flushTelemetryQueue() {{
    while (telemetryQueue.length > 0) {{
        const item = telemetryQueue.shift();
        sendBeacon(item.actionType, item.title, item.details);
    }}
}}

function trackTelemetry(actionType, title, details = {{}}) {{
    if (window.location.protocol === 'file:') return; // ignore local PDF generator

    if (!userIpResolved) {{
        telemetryQueue.push({{ actionType, title, details }});
        return;
    }}

    sendBeacon(actionType, title, details);
}}

function formatDynamicTitle(actionType, rawTitle, details, actorName) {{
    details = details || {{}};
    actorName = actorName || 'Rep';
    if (actionType === 'OPEN') return `${{actorName}} Opened Flight Deck`;
    if (actionType === 'TONE_CHANGE') return `${{actorName}} Switched Tone to: ${{details.toneName || details.toneKey || 'New Tone'}}`;
    if (actionType === 'REACTION') {{
        const actStr = details.optionClicked ? `"${{details.optionClicked}}"` : (details.nextStage || 'Next Stage');
        return `${{actorName}} Selected: ${{actStr}}`;
    }}
    if (actionType === 'SCRIPT_COPIED') return `${{actorName}} Copied Script to Clipboard`;
    if (actionType === 'CUSTOM_DECK_SAVED') return `${{actorName}} Created Custom Deck: "${{details.name || 'Custom'}}"` ;
    if (actionType === 'BANK_GUIDE_CLICK') return `${{actorName}} Viewed Bank Guide (${{details.bank || 'Bank'}})` ;
    if (actionType === 'RESET') return `${{actorName}} Reset Call for Next Lead`;
    if (actionType === 'HEARTBEAT') return `${{actorName}} Active on Call`;
    return `${{actorName}}: ${{rawTitle || actionType}}`;
}}

function sendBeacon(actionType, title, details) {{
    if (window.location.protocol === 'file:') return;

    // Strict Device & Rep Attribution:
    const isWilliam = (isSupervisorUser || SUPERVISOR_IPS.includes(userIpInfo.ip));
    const actorName = isWilliam ? "William" : "Michael Qin";
    const repLabel = isWilliam ? "William (Supervisor)" : "Michael Qin";
    const deviceLabel = isWilliam ? 
        (deviceType === 'Android' ? 'William (S24 Ultra)' : (deviceType === 'Windows PC' ? 'William (PC)' : `William (${{deviceType}})`)) :
        (deviceType === 'Windows PC' ? 'Michael (PC / Laptop)' : (deviceType === 'iPhone' ? 'Michael (iPhone)' : (deviceType === 'Android' ? 'Michael (Android)' : `Michael (${{deviceType}})`)));

    const dynamicTitle = formatDynamicTitle(actionType, title, details, actorName);

    const payload = {{
        rep: repLabel,
        isSupervisor: isWilliam,
        company: "Creative Capital Solutions",
        sessionId: repSessionId,
        device: deviceLabel,
        ip: userIpInfo.ip || 'Unknown',
        location: userIpInfo.city ? `${{userIpInfo.city}}, ${{userIpInfo.region}}` : 'Unknown Location',
        action: actionType,
        title: dynamicTitle,
        details: details,
        url: window.location.href,
        ts: new Date().toISOString(),
        localTime: new Date().toLocaleTimeString()
    }};

    try {{
        fetch(TELEMETRY_URL, {{
            method: 'POST',
            body: JSON.stringify(payload),
            headers: {{
                'Title': `[${{deviceLabel}}] ${{dynamicTitle}} (${{userIpInfo.city || 'US'}})`,
                'Tags': isWilliam ? 'bust_in_silhouette' : (actionType === 'OPEN' ? 'rocket' : actionType === 'REACTION' ? 'telephone_receiver' : 'clipboard')
            }},
            mode: 'no-cors',
            keepalive: true
        }}).catch(() => {{}});
    }} catch(e) {{}}
}}

// Initial session beacon
window.addEventListener('load', () => {{
    trackTelemetry('OPEN', 'Opened Flight Deck', {{
        screen: `${{window.innerWidth}}x${{window.innerHeight}}`,
        referrer: document.referrer || 'direct'
    }});
}});

// Heartbeat every 2 minutes
setInterval(() => {{
    trackTelemetry('HEARTBEAT', 'Active Session Heartbeat', {{
        currentStage: historyStack[historyStack.length - 1],
        currentTone: currentToneKey
    }});
}}, 120000);

/* =========================================================================
   7 INSTANT PERSONA TONE PROFILES (PSYCHOLOGICAL OVERHAUL)
   ========================================================================= */
const TONE_PROFILES = {{
    "belfort_straight_line": {{
        name: "🐺 Straight Line (Belfort)",
        opener: `"Hey [Name], Michael Qin calling from the private credit desk at Creative Capital Solutions in New York. Look, the reason for the call today is very specific:

Our credit committee is actively restructuring secondary tier debt for mid-market operators in [Industry], moving companies out of expensive daily positions like [Lender_Or_Default] to cut monthly debit debt service by 40%."`,
        who_is_this: `"I'm Michael Qin with Creative Capital Solutions, New York. We specialize in senior debt recapitalization and balance-sheet restructuring for mid-market operators like [Company].

We literally just structured a placement for [Revenue_Or_Default] in [Industry], slashing their daily debit outflow in half and saving them over $7,500 a month in hard cash flow.

Now [Name], I'm not asking for your business today—you don't know me from Adam. All I'm asking for is a shot to prove my value to you on paper. Give me 45 seconds to review your last 3 bank statements. If the numbers blow you away, we talk. If they don't, we never speak again.

Fair enough? What's your direct email?"`,
        hook: `"Look [Name], you're a sharp business operator and I know you get twenty garbage calls a week from amateur brokers blasting your credit. That's not what this is.

Our desk operates on a strictly contingent model—we only earn an advisory fee if we deliver binding senior terms that put hard cash back in [Company]'s operating account.

All I need is the last 3 monthly statement PDFs. Black out the account numbers, black out anything you're uncomfortable with. Let my desk run the numbers today.

Where should I route the breakdown?"`,
        dont_need_money: `"I hear you loud and clear [Name], and frankly, I wouldn't expect you to be sitting by the phone waiting for a loan! The best companies we work with NEVER need speculative debt.

I'm not calling to borrow—I'm calling to conduct a cost-of-capital audit on the money you've already taken out.

If our numbers show your capital structure is already in the top 1% tier of private credit, fantastic—you keep your incumbent lenders honest for free. But if we find $3,000/month in predatory fee leakage, that cash goes straight back into your pocket.

You'd at least want to know, wouldn't you? What's your best email?"`,
        just_email_me: `"I can certainly do that [Name], but let's be totally honest with each other: you're busy running [Company], and if I send an email right now, it's going to sit under 50 other unread messages until next week.

You're on your phone or near your laptop right now. Give me literally 45 seconds. Pull up your banking app, hit 'Download PDF' for the last 3 months, and forward them over while I hold the line.

I'll confirm receipt right now, my desk runs the underwriting today, and you don't have this lingering on your desk tonight.

Are you banking with Chase, Bank of America, or Wells Fargo?"`,
        what_rates: `"Look [Name], anyone who quotes you a rate without seeing your statements is lying to you to get your business. We don't operate like that. 

The rate depends entirely on your last 3 months of cash flow. If you're as strong as you say you are, you'll qualify for our top tier. 

Send me the statements, and I'll give you an exact, binding number in 3 hours. What email?"`,
        what_rates_tactical: "Anchor certainty. Never quote a blind number. Trade rate clarity directly for statements.",
        statement_pushback: `"I understand exactly how you feel, your financials are sensitive. But let me be clear—we do not shop your file. We run a secure, in-house audit. 

If you're uncomfortable, black out the account numbers! All my underwriters care about is the daily volume. 

Send it over now, what's your best email?"`,
        statement_pushback_tactical: "Address the fear directly, then re-assert the command to redact and send.",
        tactical: "Hyper-confident, urgent, sharp as a tack, enthusiastic as hell. Use straight-line anchors ('Fair enough?', 'You follow me on that?', 'You don't know me from Adam') and lock the 45-second on-call statement download."
    }},

    "voss_empathy": {{
        name: "🕵️ Tactical Empathy (Voss)",
        opener: `"Hey [Name]. [Pause 2 seconds] I'm sorry to call you out of the blue, did I catch you at a bad time?

[Wait for answer]

I appreciate that. I'm Michael with Creative Capital. We're reaching out to folks in [Industry] because it seems like [Lender_Or_Default] and the other daily-debit lenders are pulling a lot of operating cash out of the market right now."`,
        who_is_this: `"I'm Michael Qin. We're a private credit advisory firm.

It sounds like you get a lot of calls from aggressive brokers trying to jam you into high-interest loans you don't need. 

We actually do the opposite. We run a diagnostic on your last 3 bank statements to see if you're overpaying on your current debt service.

Would it be ridiculous for me to send you an email showing how we did this for another [Industry] company doing [Revenue_Or_Default]?"`,
        hook: `"It seems like you're skeptical of anyone promising to save you money without a catch.

How about this: you send over your last 3 monthly statements. We run a blind audit on our dime. If we can't legitimately cut your daily debits by at least 30%, I'll be the first to tell you to stick with what you have.

How does that sound?"`,
        dont_need_money: `"It sounds like you have your cash flow completely dialed in and you're running a very tight ship over there.

[Pause]

Just to be sure, when you say you're all set... you mean you have absolutely zero outstanding commercial debt? Or just that you're comfortable with the daily debits you're currently paying?"`,
        just_email_me: `"I can definitely send an email. But it sounds like you're incredibly busy, and an email from me is just going to create another task on your to-do list.

How am I supposed to run a real analysis for [Company] if I just send you a generic brochure?

If you're near your computer, it takes about 45 seconds to download the last 3 PDFs from your bank portal. I'll wait on the line."`,
        what_rates: `"It sounds like you've been burned by brokers hiding their fees until the last minute. 

[Pause] 

How am I supposed to give you a fair, accurate rate without seeing how your cash flow operates? If you send over the last 3 statements, we'll give you a transparent schedule. What email should I use?"`,
        what_rates_tactical: "Label their fear of hidden fees. Use a 'How' question to make them realize a blind quote is impossible.",
        statement_pushback: `"It seems like you're worried about who's going to be looking at your bank data. 

[Pause] 

What if you just black out the account numbers before you send it? We only need to see the deposits and debits to run the math. Would it be impossible to send that over to a secure link?"`,
        statement_pushback_tactical: "Label the fear of exposure. Offer a safe out (redaction) and ask a 'No-oriented' question.",
        tactical: "Late-night FM DJ voice. Slow, calm, downward inflection. Use labeling ('It sounds like...') and calibrated 'How/What' questions to let them talk themselves into it."
    }},

    "klaff_frame": {{
        name: "🧠 Frame Control (Klaff)",
        opener: `"John, Michael Qin from the private credit desk at Creative Capital. I have a hard stop in exactly two minutes for a committee meeting, but I wanted to drop a quick metric on your desk.

We're seeing mid-market operators in [Industry] hemorrhage cash to [Lender_Or_Default]. We just restructured a deal to cut their daily debt service by 40%."`,
        who_is_this: `"We're the senior underwriting desk at Creative Capital Solutions.

Look, my desk evaluates about 50 commercial debt schedules a week for companies doing [Revenue_Or_Default]. We only take on clients where we can mathematically prove a massive reduction in their cost of capital.

I don't know if [Company] qualifies for our senior tier yet, but if you want me to run the diagnostic on your last 3 statements, I'll carve out 10 minutes for my analysts to review it. What's your direct email?"`,
        hook: `"I'm not here to pitch you. My analysts just need the data to run the math.

You send the last 3 bank statements. We run the underwriting. We present you with the savings. The numbers will do the talking, and if they don't, we part as friends.

I need to jump on this next call in 60 seconds. Where should I send the secure upload link?"`,
        dont_need_money: `"John, the guys who 'need money' are exactly the guys we reject. We don't lend to distressed operators.

We only work with prime companies who want to optimize their capital stack and stop paying premium retail rates for their debt.

If you're happy paying retail rates to your current lender, keep doing it. But if you want to know what institutional pricing looks like for [Company], let's run the audit. What email?"`,
        just_email_me: `"John, I don't send out blind marketing decks. They're a waste of your time and mine.

If you don't have 45 seconds to pull your 3 bank statements right now so we can run a real, numbers-based analysis, we're probably not a fit for each other.

Are you in front of your computer or should we just part ways here?"`,
        what_rates: `"John, my desk doesn't throw darts at a dartboard. Our institutional rates are tied directly to your operating revenue. 

I'm not going to quote you a retail number. If you want access to the senior tier, you have to show us the 3 statements. 

Are we doing this or should I move on to my next call?"`,
        what_rates_tactical: "Establish high status. You don't guess rates. They must qualify for YOUR institutional rates.",
        statement_pushback: `"John, we evaluate $50M a month in commercial paper. Your financials are completely secure with my underwriters. 

But if you're not comfortable sharing redacted statements so we can do our job, we can't do business together. 

I'm sending the secure portal link now, what's your email?"`,
        statement_pushback_tactical: "Hold the frame. Display willingness to walk away if they don't comply. (Prizing).",
        tactical: "High status, slight arrogance. Establish a time constraint immediately. Make THEM qualify for YOUR time. Pull away if they hesitate (Prizing)."
    }},

    "cardone_10x": {{
        name: "⚡ 10X Assumptive (Cardone)",
        opener: `"John! Michael Qin, Creative Capital Solutions. We are slashing daily loan debits for [Industry] operators right now, moving guys out of expensive [Lender_Or_Default] positions and cutting payments by 40%.

Are you looking at your financials today?"`,
        who_is_this: `"Michael Qin, Creative Capital Solutions! We're the guys who come in and fix broken commercial debt structures.

We just took a company doing [Revenue_Or_Default] in [Industry] and freed up 8 grand a month in cash flow.

I'm going to send you a quick email right now so you have my contact info. What's the best email for you, John?"`,
        hook: `"Great. Look John, I know you're busy, I'm busy too, that's exactly why I called.

Send me your last 3 bank statements right now. I'm going to have my team run the numbers, and I'm going to show you exactly how much money we can put back in your pocket by tomorrow.

Shoot those over to me while we're on the phone, what email are you sending from?"`,
        dont_need_money: `"I agree with you completely John, you don't need money, you need to KEEP your money!

I'm not trying to put you in debt, I'm trying to get you out of the expensive debt you're already in. Every day you wait, you're overpaying.

Send me the 3 statements, let me do the heavy lifting, and I'll prove it to you. What email?"`,
        just_email_me: `"I agree you're busy, and I'm going to email you right now, but do me a favor.

You're on your phone anyway. Log into your banking app, hit download on the last 3 months, and forward it to me before we hang up. It takes exactly 45 seconds.

Let's get this done so I can go to work for you today. Chase or Bank of America?"`,
        what_rates: `"I agree you want the best rate, and that's exactly why I need the statements! 

We beat retail rates all day long, but I need to see the math so my team can underwrite it. 

Send the 3 statements right now and I'll get you a binding rate today. What email?"`,
        what_rates_tactical: "Agree instantly, then aggressively push through the objection back to the close.",
        statement_pushback: `"I agree you should be careful with your financials, but we are a top-tier desk! 

Redact the account numbers, block out the routing numbers, whatever you need to do, but send the volume over so I can go to work for you! You want me to save you money, right? 

What email?"`,
        statement_pushback_tactical: "Agree, offer the immediate solution (redact), and tie it directly to saving them money.",
        tactical: "Relentless, high energy, 100% certainty. Always agree with their objection first ('I agree!'), then immediately pivot back to the pitch and push the close."
    }},

    "challenger_sale": {{
        name: "📊 Challenger Tension",
        opener: `"John, Michael Qin with the private credit desk at Creative Capital.

We're tracking a disturbing trend in the [Industry] sector right now. Mid-market operators are losing upwards of 12% of their operating margin to hidden fees and compounding daily debits from lenders like [Lender_Or_Default].

Have you audited your effective annual rate this quarter?"`,
        who_is_this: `"Creative Capital Solutions. We run commercial debt forensics and institutional refinancing.

What we're finding is that operators doing [Revenue_Or_Default] think they're paying 15% on their capital, but because of daily debit factoring, their true cost of capital is closer to 45%.

I'd like to send you our recent white-paper analysis on this, along with a secure link to run a free audit on your last 3 statements. What's your direct email?"`,
        hook: `"John, the biggest risk to [Company] right now isn't lack of capital, it's the cost of the capital you already deployed.

If you provide your last 3 bank statements, our analysts will map out your exact cost-of-capital curve.

We typically uncover $3k to $5k a month in margin leakage. Where should I send the audit framework?"`,
        dont_need_money: `"Most operators think they're all set, John—until we show them how their current lender is front-loading the interest and bleeding their daily cash flow.

How certain are you that your current effective rate with your incumbent lender is actually under 18%?

[Wait for answer]

Send me the 3 statements. Let us prove it mathematically. What email?"`,
        just_email_me: `"I can send the email, John. But let's be pragmatic.

If you don't take 45 seconds right now to pull those 3 statements from your banking portal, tomorrow morning you're going to get hit with another expensive daily debit that you didn't need to pay.

Log into the portal now. I'll stay on the line to confirm receipt."`,
        what_rates: `"The fact that you're asking for a flat rate tells me your current lender sold you a one-size-fits-all product. True cost of capital is dynamic. 

We map your rate to your exact revenue curve. To give you the exact number, my analysts need the 3 statements. 

Where should I send the upload link?"`,
        what_rates_tactical: "Challenge their assumption that flat rates are a good thing. Reframe as dynamic modeling.",
        statement_pushback: `"Most operators hesitate to share financials because their current lender told them it's too risky to shop around. That's exactly how they keep you trapped in high-interest debits. 

You can redact the account numbers. We just need the raw data to prove they're overcharging you. What email?"`,
        statement_pushback_tactical: "Use commercial teaching to reframe their fear as a trap set by their current lender.",
        tactical: "Lead with insight and disruption. Challenge their assumptions. Create constructive tension by implying they don't actually know their true cost of capital."
    }},

    "cialdini_authority": {{
        name: "👑 Authority (Cialdini)",
        opener: `"Hey [Name], Michael Qin on the private credit desk at Creative Capital Solutions.

The reason I'm calling you directly is that we just finished restructuring commercial debt for three other [Industry] firms right in your exact area, moving them out of [Lender_Or_Default] and cutting their payments by 40%."`,
        who_is_this: `"Michael Qin, Creative Capital Solutions.

We are the premier debt restructuring desk for the [Industry] sector. Over 80% of the companies we talk to doing [Revenue_Or_Default] are currently overpaying on their short-term debt.

I want to send you the exact case study of how we just saved a competitor of yours $7,500 a month. What's the best email to send that to?"`,
        hook: `"John, right now we have an exclusive block of institutional capital specifically earmarked to refinance operators in your industry, but it closes at the end of the month.

To see if you qualify for these top-tier rates, I just need your last 3 bank statements. The top firms we work with run this audit quarterly.

What email should I use?"`,
        dont_need_money: `"I'm glad to hear that John, because the operators who get approved for our lowest rates are exactly the ones who don't *need* the money.

Because your profile is strong, you're exactly who the tier-1 banks want to lend to right now. You shouldn't be paying retail rates.

Let's run the 3-statement audit to see what rate tier you actually qualify for. What's your email?"`,
        just_email_me: `"I can email you John, but the operators who secure these rates don't wait on emails—they run the 45-second audit with me live on the phone so we can get them into underwriting today.

Let's get your 3 statements pulled right now while you have me on the line. It'll take less than a minute.

Do you use Chase or Bank of America?"`,
        what_rates: `"The operators who get our absolute lowest rates understand that institutional pricing is bespoke. We don't quote blind. 

The three [Industry] companies we just funded sent their statements, we ran the math, and gave them a binding schedule in hours. Let's do the exact same for you. 

What email?"`,
        what_rates_tactical: "Leverage social proof (the three other companies did this, so you should too).",
        statement_pushback: `"I completely understand the caution. That's why the top firms in your industry trust us—we run a completely secure, in-house audit. 

You can even black out your account numbers. Let's get this moving so you don't miss this funding block. 

What's the best email?"`,
        statement_pushback_tactical: "Leverage Authority (top firms trust us) and Scarcity (miss this funding block).",
        tactical: "Leverage Social Proof ('three other firms in your area'), Authority ('premier desk'), Scarcity ('closes at the end of the month'), and Consensus ('the top firms do this')."
    }},

    "ziglar_relational": {{
        name: "🤠 Relational (Ziglar)",
        opener: `"Hey John, I hope you're having a good day. It's Michael Qin with Creative Capital Solutions.

I know you weren't expecting my call, and I appreciate you picking up. We're reaching out to hardworking [Industry] owners today to help them get out from under those heavy daily payments to lenders like [Lender_Or_Default]."`,
        who_is_this: `"It's Michael Qin with Creative Capital Solutions. We help honest business owners like you keep more of the money you earn.

We just worked with a great guy running a [Industry] business doing [Revenue_Or_Default], and we were able to free up enough cash flow for him to hire two new guys.

I'd love to just send you a quick note with my contact info so you know I'm a real person. What's the best email for you?"`,
        hook: `"John, I treat my clients the way I'd want my own family treated. If you share your last 3 bank statements with me, I will personally look them over.

If your current lender is taking good care of you, I'll be the first to tell you to stay with them. But if they're charging you too much, I'd love to show you a better way.

What email works best for you?"`,
        dont_need_money: `"I completely understand how you feel, John. A lot of our best clients felt the exact same way when I first called them.

But what they found was that they were actually losing thousands of dollars a month to hidden fees they didn't even know about. I just want to make sure you're protected.

Let me do a quick, free check on your last 3 statements. What email should I use?"`,
        just_email_me: `"I'd be happy to send you an email John. But you know how it is—we all get busy, and things just pile up on the desk.

Since we're on the phone right now, if you could just take 45 seconds to pull those 3 statements from your banking app, we can get this completely off your plate today.

Who do you guys bank with down there, Chase or Wells Fargo?"`,
        what_rates: `"John, I'd love to give you a number right now, but I want to be completely honest with you—if I guess, I might be wrong, and I don't want to make a promise I can't keep. 

If you share your last 3 statements with me, I will personally make sure you get the absolute best rate we have. 

What email works for you?"`,
        what_rates_tactical: "Focus on honesty and integrity. Don't make a promise you can't keep.",
        statement_pushback: `"I completely understand how you feel. A lot of my best clients felt the exact same way before we started working together. 

They found that once they blacked out their account numbers and saw how securely we handle their file, it was the best decision they ever made. 

Let's start small. What's your email?"`,
        statement_pushback_tactical: "Use 'Feel, Felt, Found' to overcome objection naturally.",
        tactical: "Warm, empathetic, trustworthy. Use the 'Feel, Felt, Found' framework. Focus on protecting them and treating them like family."
    }}
}}

let currentToneKey = "belfort_straight_line";


function setTone(toneKey, btn) {{
    currentToneKey = toneKey;
    document.querySelectorAll('.tone-chip').forEach(c => c.classList.remove('active'));
    if (btn) btn.classList.add('active');
    
    const profile = TONE_PROFILES[toneKey] || TONE_PROFILES["wall_street"];
    const labelEl = document.getElementById('active-tone-label');
    if (labelEl) labelEl.innerText = profile.name;

    trackTelemetry('TONE_CHANGE', `Switched Tone`, {{ toneName: profile.name, toneKey: toneKey }});
    renderCurrentNode();
}}

/* =========================================================================
   SHARE MODAL LOGIC
   ========================================================================= */
function openShareModal() {{
    const modal = document.getElementById('share-modal');
    if (modal) modal.classList.add('open');
    trackTelemetry('SHARE_MODAL', 'Opened Share Modal');
}}

function closeShareModal(e) {{
    const modal = document.getElementById('share-modal');
    if (modal) modal.classList.remove('open');
}}

function copyToolUrl() {{
    const box = document.getElementById('share-url-box');
    copyText(box.value);
    trackTelemetry('SHARE_COPY', 'Copied Tool Share URL');
}}

function toggleIntelDrawer() {{
    const drawer = document.getElementById('intel-drawer');
    if (drawer) {{
        drawer.classList.toggle('open');
        trackTelemetry('INTEL_DRAWER', 'Toggled Intel Drawer');
    }}
}}

/* =========================================================================
   INDUSTRY VERTICAL PRESETS & PAIN CUES
   ========================================================================= */
const INDUSTRY_PRESETS = {{
    "contractor": {{
        industry: "Commercial Construction & Roofing",
        lender: "OnDeck / Rapid Finance",
        revenue: "$140,000/mo",
        debitStr: "$1,850/day",
        notes: "Pain: 60-90 day GC progress draw delay & upfront material supply."
    }},
    "trucking": {{
        industry: "Freight Logistics & Trucking",
        lender: "Fundbox / Apex Capital",
        revenue: "$185,000/mo",
        debitStr: "$2,400/day",
        notes: "Pain: Diesel fuel card debits & 45-day freight broker payables lag."
    }},
    "restaurant": {{
        industry: "Restaurant & Hospitality",
        lender: "Square Capital / Toast",
        revenue: "$95,000/mo",
        debitStr: "$950/day",
        notes: "Pain: POS credit card batch holds; wants to keep 100% of weekend receipts."
    }},
    "medical": {{
        industry: "Private Dental & Medical Practice",
        lender: "Lendio / Fora Financial",
        revenue: "$130,000/mo",
        debitStr: "$1,200/day",
        notes: "Pain: 60-day Medicare & private insurer reimbursement lag."
    }},
    "manufacturing": {{
        industry: "Machining & Manufacturing",
        lender: "Kapitus / National Funding",
        revenue: "$260,000/mo",
        debitStr: "$3,600/day",
        notes: "Pain: High raw material prepayments & CNC equipment lease debt."
    }},
    "retail": {{
        industry: "Auto Repair & Retail Supply",
        lender: "Libertas / Fundraise",
        revenue: "$110,000/mo",
        debitStr: "$1,350/day",
        notes: "Pain: Seasonal inventory buildup & parts supplier invoices."
    }}
}};

function applyIndustryPreset(key) {{
    const p = INDUSTRY_PRESETS[key];
    if (!p) return;

    document.querySelectorAll('.industry-chip').forEach(c => c.classList.remove('active'));
    const btn = event?.currentTarget || event?.target;
    if (btn && btn.classList?.contains('industry-chip')) btn.classList.add('active');

    document.getElementById('lead-industry').value = p.industry;
    const lenderEl = document.getElementById('lead-lender'); if (lenderEl) lenderEl.value = p.lender;
    const revEl = document.getElementById('lead-rev'); if (revEl) revEl.value = p.revenue;
    const debitEl = document.getElementById('lead-debit-str'); if (debitEl) debitEl.value = p.debitStr;
    const notesEl = document.getElementById('lead-notes'); if (notesEl) notesEl.value = p.notes;

    updatePersonalization();
    trackTelemetry('INDUSTRY_PRESET', `Applied Vertical Preset: ${{p.industry}}`, {{ vertical: key }});
}}

/* =========================================================================
   DYNAMIC LEAD PERSONALIZATION
   ========================================================================= */
let leadState = {{
    name: "",
    company: "",
    industry: "",
    lender: "",
    revenue: "",
    debitStr: "",
    notes: ""
}};

function getEffectiveTokens() {{
    return {{
        name: leadState.name.trim() || "John",
        company: leadState.company.trim() || "your company",
        industry: leadState.industry.trim() || "your industry",
        lender: leadState.lender.trim() || "",
        revenue: leadState.revenue.trim() || "",
        debitStr: leadState.debitStr.trim() || "",
        notes: leadState.notes.trim() || ""
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

    if (leadState.lender.trim()) {{
        const lenderToken = highlight ? `<span class="token-highlight">${{t.lender}}</span>` : t.lender;
        res = res.replaceAll("[Lender_Or_Default]", `positions out of lenders like ${{lenderToken}}`);
    }} else {{
        res = res.replaceAll("[Lender_Or_Default]", "expensive daily debt positions in your space");
    }}

    if (leadState.revenue.trim()) {{
        const revToken = highlight ? `<span class="token-highlight">${{t.revenue}}</span>` : t.revenue;
        res = res.replaceAll("[Revenue_Or_Default]", `businesses generating ${{revToken}} in volume`);
    }} else {{
        res = res.replaceAll("[Revenue_Or_Default]", "commercial operators in your sector");
    }}

    return res;
}}

function updatePersonalization() {{
    leadState.name = document.getElementById('lead-name').value;
    leadState.company = document.getElementById('lead-company').value;
    leadState.industry = document.getElementById('lead-industry').value;
    
    const lenderEl = document.getElementById('lead-lender'); if(lenderEl) leadState.lender = lenderEl.value;
    const revEl = document.getElementById('lead-rev'); if(revEl) leadState.revenue = revEl.value;
    const debitEl = document.getElementById('lead-debit-str'); if(debitEl) leadState.debitStr = debitEl.value;
    const notesEl = document.getElementById('lead-notes'); if(notesEl) leadState.notes = notesEl.value;

    const stickyBox = document.getElementById('sticky-note-box');
    const stickyText = document.getElementById('sticky-note-text');
    if (stickyBox && stickyText) {{
        if (leadState.notes.trim()) {{
            stickyBox.style.display = "block";
            stickyText.innerText = leadState.notes;
        }} else {{
            stickyBox.style.display = "none";
        }}
    }}

    renderCurrentNode();
    updateCadenceSnippets();
}}

function clearLeadInputs() {{
    document.getElementById('lead-name').value = "";
    document.getElementById('lead-company').value = "";
    document.getElementById('lead-industry').value = "";
    
    const lenderEl = document.getElementById('lead-lender'); if(lenderEl) lenderEl.value = "";
    const revEl = document.getElementById('lead-rev'); if(revEl) revEl.value = "";
    const debitEl = document.getElementById('lead-debit-str'); if(debitEl) debitEl.value = "";
    const notesEl = document.getElementById('lead-notes'); if(notesEl) notesEl.value = "";

    leadState = {{ name: "", company: "", industry: "", lender: "", revenue: "", debitStr: "", notes: "" }};
    updatePersonalization();
}}

function updateCadenceSnippets() {{
    const t = getEffectiveTokens();
    const sms1 = `"Hi ${{t.name}}, Michael Qin here from Creative Capital Solutions. Great speaking with you briefly. To run your debt consolidation and statement audit for ${{t.company}}, just email your last 3 monthly business bank PDFs to michael@creativecapitalsolutions.com. Once received, I will have your approved numbers back within 24 hours."`;
    const email1 = `Subject: Quick question regarding ${{t.company}} cash flow\n\nHi ${{t.name}},\n\nFollowing up on our conversation regarding restructuring your operating debt for ${{t.company}}.\n\nOur underwriting desk locks weekly merchant placement tiers every Thursday at 4 PM. If you shoot over your 3 bank statements today, I can have your term sheet approved before the weekend.\n\nLet me know if you need help pulling the PDFs from Chase/BoA.\n\nBest,\nMichael Qin\nCreative Capital Solutions`;
    const email2 = `Subject: Closing your file / ${{t.company}}\n\nHi ${{t.name}},\n\nI assume restructuring your working capital isn't a priority right now, so I will close out your file for ${{t.company}}.\n\nIf daily debits ever start squeezing your cash flow down the road, feel free to reach out anytime.\n\nBest regards,\nMichael Qin\nCreative Capital Solutions`;
    const stmtWalk = `"${{t.name}}, are you in front of your computer or looking at your phone right now?\n\nStay on with me for literally 45 seconds while you export your last 3 monthly statements as PDFs. I will confirm receipt while we're on the line so this isn't hanging over your head tonight.\n\nWhich bank do you use for operations—Chase, Bank of America, or Wells?"`;
    const lossAv = `"${{t.name}}, I don't want you wasting your evening downloading statements if this doesn't put money back into your business.\n\nIf our review shows your current setup is already optimal, I will tell you to keep it. But if you're leaking $2,500 a month in excessive factor fees or daily debits, wouldn't you want to know by tomorrow morning?\n\nLet me send you a secure request link right now. What's the best email?"`;

    const el1 = document.getElementById('cadence-sms1'); if(el1) el1.innerText = sms1;
    const el2 = document.getElementById('cadence-email1'); if(el2) el2.innerText = email1;
    const el3 = document.getElementById('cadence-email2'); if(el3) el3.innerText = email2;
    const el4 = document.getElementById('stmt-walkthrough-text'); if(el4) el4.innerText = stmtWalk;
    const el5 = document.getElementById('loss-aversion-text'); if(el5) el5.innerText = lossAv;
}}

/* =========================================================================
   DYNAMIC CALL FLOW ROUTING
   ========================================================================= */
function getActiveNodeData(nodeKey) {{
    const profile = TONE_PROFILES[currentToneKey] || TONE_PROFILES["wall_street"];

    const baseMap = {{
        "root": {{
            stage: "Stage 1: Opening (0-5s)",
            verbatim: profile.opener,
            tactical: profile.tactical,
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
            verbatim: profile.who_is_this,
            tactical: "State your niche, reference peer results, and close for their direct email.",
            options: [
                {{ text: `"Sure, send to [Email]"`, key: "1", next: "win_extract_statements", type: "pos" }},
                {{ text: `"We don't need any funding"`, key: "2", next: "dont_need_money", type: "neg" }},
                {{ text: `"What are your rates?"`, key: "3", next: "what_rates", type: "amber" }}
            ]
        }},

        "aligned_hook": {{
            stage: "Stage 2: Core Value & Risk Reversal",
            verbatim: profile.hook,
            tactical: "Highlight zero downside risk and contingent success representation.",
            options: [
                {{ text: `Merchant gave email address`, key: "1", next: "win_extract_statements", type: "pos" }},
                {{ text: `"We already have a lender"`, key: "2", next: "dont_need_money", type: "neg" }},
                {{ text: `"I don't have time right now"`, key: "3", next: "just_email_me", type: "amber" }}
            ]
        }},

        "dont_need_money": {{
            stage: "Pivot: No Borrowing Needed",
            verbatim: profile.dont_need_money,
            tactical: "Reframe from borrowing to expense reduction and cash recovery.",
            options: [
                {{ text: `"Fair enough, send to [Email]"`, key: "1", next: "win_extract_statements", type: "pos" }},
                {{ text: `"Not interested / Hard No"`, key: "2", next: "hard_no", type: "neg" }}
            ]
        }},

        "just_email_me": {{
            stage: "Pivot: 'Send Info' Deflection",
            verbatim: profile.just_email_me,
            tactical: "Never let them off the phone without asking for the 45-second on-call download.",
            options: [
                {{ text: `"I'm on my computer now / Exporting"`, key: "1", next: "win_on_call_download", type: "pos" }},
                {{ text: `"I'm driving / really busy"`, key: "2", next: "send_sms_link", type: "amber" }}
            ]
        }},
        "what_rates": {{
            stage: "Pricing Hook & Trade-Off",
            verbatim: profile.what_rates,
            tactical: profile.what_rates_tactical,
            options: [
                {{ text: `Merchant agreed / gave email`, key: "1", next: "win_extract_statements", type: "pos" }},
                {{ text: `"Why do you need statements?"`, key: "2", next: "statement_pushback", type: "neg" }}
            ]
        }},

        "statement_pushback": {{
            stage: "Statement Hesitation Rebuttal",
            verbatim: profile.statement_pushback,
            tactical: profile.statement_pushback_tactical,
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

    return baseMap[nodeKey] || baseMap["root"];
}}

let historyStack = ["root"];

function renderCurrentNode() {{
    const key = historyStack[historyStack.length - 1];
    const node = getActiveNodeData(key);

    document.getElementById('hud-stage').innerText = node.stage;
    document.getElementById('hud-verbatim').innerHTML = formatWithTokens(node.verbatim, true);
    document.getElementById('hud-tactical').innerText = node.tactical;
    document.getElementById('hud-step').innerText = `Step ${{historyStack.length}} of 4`;

    const btnGrid = document.getElementById('hud-options');
    btnGrid.innerHTML = node.options.map((opt, idx) => `
        <button class="opt-btn ${{opt.type}}" onclick="handleOptionClick(${{idx}})">
            <span>${{formatWithTokens(opt.text)}}</span>
            <span class="key-pill">${{opt.key}}</span>
        </button>
    `).join('');

    document.getElementById('btn-back').style.display = historyStack.length > 1 ? 'inline-block' : 'none';
}}

function handleOptionClick(idx) {{
    const key = historyStack[historyStack.length - 1];
    const node = getActiveNodeData(key);
    const opt = node.options[idx];
    if (opt) {{
        pickNext(opt.next, opt.text);
    }}
}}

function getCleanScriptText() {{
    const key = historyStack[historyStack.length - 1];
    const node = getActiveNodeData(key);
    return formatWithTokens(node.verbatim, false);
}}

function pickNext(key, optLabel = '') {{
    try {{
        historyStack.push(key);
        renderCurrentNode();
    }} catch(err) {{
        console.error("renderCurrentNode error:", err);
    }}
    try {{
        trackTelemetry('REACTION', `Reaction Chosen: ${{key}}`, {{
            nextStage: key,
            optionClicked: optLabel,
            leadName: leadState.name || 'Anonymous',
            leadCompany: leadState.company || 'Unknown',
            tone: currentToneKey
        }});
    }} catch(e) {{}}
}}

function goBack() {{
    if (historyStack.length > 1) {{
        historyStack.pop();
        renderCurrentNode();
    }}
}}

function resetFlow() {{
    historyStack = ["root"];
    trackTelemetry('RESET', 'Reset Call Script for Next Lead');
    renderCurrentNode();
}}

// Keyboard Listener
window.addEventListener('keydown', (e) => {{
    const hudTab = document.getElementById('tab-hud');
    if (!hudTab.classList.contains('active')) return;
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    if (e.key >= '1' && e.key <= '6') {{
        const key = historyStack[historyStack.length - 1];
        const node = getActiveNodeData(key);
        const opt = node.options.find(o => o.key === e.key);
        if (opt) pickNext(opt.next, opt.text);
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
   CUSTOM DECK BUILDER (LOCALSTORAGE)
   ========================================================================= */
let customDecks = [];

function loadCustomDecks() {{
    try {{
        const saved = localStorage.getItem('mq_custom_decks');
        customDecks = saved ? JSON.parse(saved) : [];
    }} catch(e) {{
        customDecks = [];
    }}
    renderCustomDeckList();
}}

function saveCustomDeck() {{
    const name = document.getElementById('new-deck-name').value.trim();
    const opener = document.getElementById('new-deck-opener').value.trim();
    const hook = document.getElementById('new-deck-hook').value.trim();
    const note = document.getElementById('new-deck-note').value.trim();

    if (!name || !opener) {{
        alert("Please provide at least a Deck Name and an Opener Line.");
        return;
    }}

    const deckId = 'custom_' + Date.now();
    const newDeck = {{
        id: deckId,
        name: name,
        opener: opener,
        who_is_this: hook || opener,
        hook: hook || opener,
        dont_need_money: `Completely understand [Name]. I'm not calling to sell you new debt—I'm calling to stop cash leakage on positions you already have. What's the best email for a 1-page check?`,
        just_email_me: `Happy to do that [Name]. But while I have you for 45 seconds, download your last 3 monthly statement PDFs from your portal so this is off your plate tonight. Which bank do you use?`,
        tactical: note || "Deliver with conviction and focus on merchant cash savings."
    }};

    customDecks.push(newDeck);
    localStorage.setItem('mq_custom_decks', JSON.stringify(customDecks));

    TONE_PROFILES[deckId] = newDeck;

    trackTelemetry('CUSTOM_DECK_SAVED', `Created Custom Deck: "${{name}}"`);

    document.getElementById('new-deck-name').value = "";
    document.getElementById('new-deck-opener').value = "";
    document.getElementById('new-deck-hook').value = "";
    document.getElementById('new-deck-note').value = "";

    renderCustomDeckList();
    renderToneChips();
    setTone(deckId);
    switchTab('tab-hud');

    const toast = document.getElementById('toast');
    toast.innerText = `Deck "${{name}}" Saved!`;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2000);
}}

function deleteCustomDeck(id, e) {{
    e.stopPropagation();
    customDecks = customDecks.filter(d => d.id !== id);
    delete TONE_PROFILES[id];
    localStorage.setItem('mq_custom_decks', JSON.stringify(customDecks));
    renderCustomDeckList();
    renderToneChips();
    if (currentToneKey === id) setTone('wall_street');
}}

function renderCustomDeckList() {{
    const container = document.getElementById('custom-decks-container');
    if (!container) return;

    if (customDecks.length === 0) {{
        container.innerHTML = `<div style="font-size: 10.5px; color: var(--text-muted); padding: 5px; background: #fff; border: 1px dashed var(--border-main); border-radius: 2px;">No custom decks yet.</div>`;
        return;
    }}

    container.innerHTML = customDecks.map(d => `
        <div style="background:#fff; border:1px solid var(--border-main); border-radius:2px; padding:5px 8px; display:flex; justify-content:space-between; align-items:center; margin-bottom:3px;">
            <div>
                <div style="font-weight:700; color:var(--corporate-navy); font-size:11px;">${{d.name}}</div>
            </div>
            <div style="display:flex; gap:3px;">
                <button class="btn-ctrl" onclick="setTone('${{d.id}}'); switchTab('tab-hud');">⚡ Use</button>
                <button class="btn-ctrl" style="color:var(--color-danger);" onclick="deleteCustomDeck('${{d.id}}', event)">🗑️</button>
            </div>
        </div>
    `).join('');
}}

function renderToneChips() {{
    const container = document.getElementById('tone-chips-container');
    if (!container) return;

    const baseChips = `
        <button class="tone-chip ${{currentToneKey === 'belfort_straight_line' ? 'active' : ''}}" onclick="setTone('belfort_straight_line', this)">🐺 Straight Line</button>
        <button class="tone-chip ${{currentToneKey === 'voss_empathy' ? 'active' : ''}}" onclick="setTone('voss_empathy', this)">🕵️ Voss (Empathy)</button>
        <button class="tone-chip ${{currentToneKey === 'klaff_frame' ? 'active' : ''}}" onclick="setTone('klaff_frame', this)">🧠 Klaff (Frames)</button>
        <button class="tone-chip ${{currentToneKey === 'cardone_10x' ? 'active' : ''}}" onclick="setTone('cardone_10x', this)">⚡ Cardone (10X)</button>
        <button class="tone-chip ${{currentToneKey === 'challenger_sale' ? 'active' : ''}}" onclick="setTone('challenger_sale', this)">📊 Challenger</button>
        <button class="tone-chip ${{currentToneKey === 'cialdini_authority' ? 'active' : ''}}" onclick="setTone('cialdini_authority', this)">👑 Cialdini</button>
        <button class="tone-chip ${{currentToneKey === 'ziglar_relational' ? 'active' : ''}}" onclick="setTone('ziglar_relational', this)">🤠 Ziglar</button>
    `;

    const customChips = customDecks.map(d => `
        <button class="tone-chip ${{currentToneKey === d.id ? 'active' : ''}}" onclick="setTone('${{d.id}}', this)">⭐ ${{d.name}}</button>
    `).join('');

    container.innerHTML = baseChips + customChips;
}}

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
    trackTelemetry('BANK_GUIDE_CLICK', `Viewed Bank Guide: ${{bankKey}}`);
}}

/* =========================================================================
   UTILITIES
   ========================================================================= */
function switchTab(tabId) {{
    document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-item').forEach(el => el.classList.remove('active'));
    const target = document.getElementById(tabId);
    if (target) target.classList.add('active');
    const btn = Array.from(document.querySelectorAll('.tab-item')).find(b => b.getAttribute('onclick').includes(tabId));
    if (btn) btn.classList.add('active');

    trackTelemetry('TAB_SWITCH', `Switched to tab: ${{tabId}}`);
}}

function copyText(text) {{
    navigator.clipboard.writeText(text.trim()).then(() => {{
        const toast = document.getElementById('toast');
        toast.innerText = "Copied to clipboard";
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 1500);
        trackTelemetry('SCRIPT_COPIED', 'Copied script to clipboard', {{ textSnippet: text.substring(0, 60) + '...' }});
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
        <div style="margin-bottom: 6px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 4px;">
            <div style="font-size: 11px; font-weight: 700; color: var(--color-danger); margin-bottom: 1px;">⚠️ "${{o.objection}}"</div>
            <div class="copy-block red-box">
                <div class="copy-text">"${{o.rebuttal}}"</div>
                <button class="btn-copy" onclick="copySnippet(this)">Copy</button>
            </div>
            <div style="font-size: 10px; color: var(--text-muted); margin-top: 1px;"><strong>Principle:</strong> ${{o.principle}}</div>
        </div>
    `).join('');
}}

function renderPipeline() {{
    const container = document.getElementById('pipeline-list');
    container.innerHTML = STAGES.map(s => `
        <div style="margin-bottom: 8px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 4px;">
            <div style="font-size: 11.5px; font-weight: 700; color: var(--corporate-navy); margin-bottom: 1px;">Stage ${{s.number}}: ${{s.title}}</div>
            <div style="font-size: 10.5px; color: var(--text-main); margin-bottom: 2px;"><strong>Goal:</strong> ${{s.objective}}</div>
            <div style="font-size: 10px; color: var(--text-muted); margin-bottom: 2px;"><strong>Key Actions:</strong></div>
            <ul style="padding-left: 12px; font-size: 10.5px; color: var(--text-main);">
                ${{s.actions.map(a => `<li>${{a}}</li>`).join('')}}
            </ul>
        </div>
    `).join('');
}}

window.addEventListener('DOMContentLoaded', () => {{
    loadCustomDecks();
    renderToneChips();
    setTone('wall_street');
    renderObjections();
    renderPipeline();
    runCalc();
    updateCadenceSnippets();
}});
</script>
</body>
</html>"""

    def render_admin_html(self) -> str:
        """
        William's Revamped Live Supervisor Cockpit (admin.html).
        Features:
        - Instant visual feedback on connection health.
        - Test Ping button to verify pipeline in 1 click.
        - Strict IP & file:/// exclusions (William's PC 85.115.107.223 and Cell 74.209.76.220).
        - Filter by Event Type: All, Calls/Reactions, Script Copies, Device Opens.
        - Audio Chime notification toggle.
        - Live Pulse and relative countdown.
        """
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Creative Capital Solutions — Supervisor Live Operations Cockpit</title>
<style>
    :root {{
        --navy: #0f2744;
        --steel: #1b4b72;
        --blue: #2563eb;
        --bg: #f8fafc;
        --card: #ffffff;
        --border: #cbd5e1;
        --border-subtle: #e2e8f0;
        --text: #1e293b;
        --muted: #64748b;
        --green: #166534;
        --green-bg: #dcfce7;
        --green-border: #bbf7d0;
        --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
        background-color: var(--bg);
        color: var(--text);
        font-family: var(--font);
        line-height: 1.4;
        font-size: 13px;
        padding: 10px;
    }}

    .admin-wrap {{
        max-width: 1120px;
        margin: 0 auto;
    }}

    /* Header */
    .admin-header {{
        background: var(--card);
        border: 1px solid var(--border);
        border-top: 4px solid var(--navy);
        padding: 12px 16px;
        border-radius: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        flex-wrap: wrap;
        gap: 8px;
    }}
    .title-area h1 {{
        font-size: 16px;
        font-weight: 800;
        color: var(--navy);
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .title-area p {{
        font-size: 11px;
        color: var(--muted);
    }}

    .pulse-box {{
        display: flex;
        align-items: center;
        gap: 8px;
        background: #f1f5f9;
        border: 1px solid var(--border);
        padding: 6px 12px;
        border-radius: 20px;
    }}
    .pulse-dot {{
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #94a3b8;
    }}
    .pulse-dot.online {{
        background: #22c55e;
        box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.25);
        animation: pulseAnim 1.8s infinite;
    }}
    @keyframes pulseAnim {{
        0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }}
        70% {{ transform: scale(1); box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); }}
        100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }}
    }}
    .pulse-status {{
        font-size: 11.5px;
        font-weight: 700;
        color: var(--navy);
    }}

    /* Filter Status Banner */
    .filter-banner {{
        font-size: 11px;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1e40af;
        padding: 6px 12px;
        border-radius: 4px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
    }}
    .btn-mark-sup {{
        background: #1e40af;
        color: #fff;
        border: none;
        padding: 4px 8px;
        border-radius: 3px;
        font-size: 10px;
        cursor: pointer;
        font-weight: 700;
    }}

    /* KPI Summary Cards */
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 8px;
        margin-bottom: 10px;
    }}
    .kpi-card {{
        background: var(--card);
        border: 1px solid var(--border);
        padding: 12px;
        border-radius: 4px;
        text-align: center;
    }}
    .kpi-num {{
        font-family: var(--mono);
        font-size: 24px;
        font-weight: 800;
        color: var(--navy);
    }}
    .kpi-lbl {{
        font-size: 10px;
        font-weight: 700;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    /* Controls Bar */
    .controls-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        gap: 8px;
        flex-wrap: wrap;
    }}
    .filter-pills {{
        display: flex;
        gap: 4px;
    }}
    .pill-btn {{
        background: #ffffff;
        border: 1px solid var(--border);
        color: var(--muted);
        padding: 4px 8px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: 600;
        cursor: pointer;
    }}
    .pill-btn.active {{
        background: var(--navy);
        color: #ffffff;
        border-color: var(--navy);
    }}

    .action-group {{
        display: flex;
        gap: 5px;
    }}
    .btn-action {{
        background: var(--navy);
        color: #ffffff;
        border: 1px solid var(--navy);
        padding: 5px 10px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: 700;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }}
    .btn-action.secondary {{
        background: #ffffff;
        color: var(--navy);
    }}
    .btn-action:hover {{ opacity: 0.9; }}

    /* Live Feed Container */
    .feed-card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 14px;
    }}
    .feed-header {{
        font-size: 12.5px;
        font-weight: 800;
        color: var(--navy);
        text-transform: uppercase;
        margin-bottom: 10px;
        padding-bottom: 6px;
        border-bottom: 1px solid var(--border);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .event-list {{
        display: flex;
        flex-direction: column;
        gap: 6px;
        max-height: 600px;
        overflow-y: auto;
    }}

    .event-item {{
        background: #f8fafc;
        border: 1px solid var(--border);
        border-left: 4px solid var(--blue);
        padding: 9px 12px;
        border-radius: 3px;
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 10px;
        animation: fadeIn 0.2s ease;
    }}
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(-4px); }} to {{ opacity: 1; transform: translateY(0); }} }}

    .event-item.open {{ border-left-color: #22c55e; background: #f0fdf4; }}
    .event-item.reaction {{ border-left-color: #3b82f6; background: #eff6ff; }}
    .event-item.copy {{ border-left-color: #8b5cf6; background: #faf5ff; }}
    .event-item.tone {{ border-left-color: #f59e0b; background: #fffbeb; }}
    .event-item.heartbeat {{ border-left-color: #94a3b8; opacity: 0.75; }}

    .event-main {{
        flex: 1;
    }}
    .event-title {{
        font-weight: 700;
        color: var(--navy);
        font-size: 12.5px;
        margin-bottom: 3px;
    }}
    .event-details {{
        font-size: 11.5px;
        color: var(--text);
        margin-bottom: 2px;
    }}
    .event-details-meta {{
        font-size: 10.5px;
        color: var(--muted);
        font-family: var(--mono);
    }}
    .event-meta {{
        font-size: 10px;
        color: var(--muted);
        font-family: var(--mono);
        text-align: right;
        white-space: nowrap;
    }}
    .device-pill {{
        background: #e2e8f0;
        color: var(--navy);
        font-size: 9.5px;
        font-weight: 700;
        padding: 1px 6px;
        border-radius: 3px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 3px;
    }}

    .empty-state {{
        text-align: center;
        padding: 40px 20px;
        color: var(--muted);
        font-size: 12.5px;
    }}

    .diag-box {{
        margin-top: 14px;
        background: #f1f5f9;
        border: 1px solid var(--border);
        padding: 8px 12px;
        border-radius: 3px;
        font-size: 10.5px;
        color: var(--muted);
        font-family: var(--mono);
    }}
</style>
</head>
<body>

<div class="admin-wrap">

    <!-- Header -->
    <div class="admin-header">
        <div class="title-area">
            <h1>📡 Supervisor Operations Cockpit</h1>
            <p>Live Real-Time Activity, Dials &amp; Call Telemetry for Michael Qin</p>
        </div>

        <div style="display:flex; align-items:center; gap:8px;">
            <a href="opponent.html" style="background:#dc2626; color:#ffffff; padding:6px 12px; border-radius:4px; text-decoration:none; font-weight:800; font-size:11.5px; display:inline-flex; align-items:center; gap:4px; box-shadow:0 1px 3px rgba(220,38,38,0.3);">🥊 Sparring Arena</a>
            <div class="pulse-box">
                <div class="pulse-dot" id="live-dot"></div>
                <span class="pulse-status" id="live-status">Connecting to Live Stream...</span>
            </div>
        </div>
    </div>

    <!-- Exclusion Filter Banner -->
    <div class="filter-banner">
        <span>🛡️ <strong>Exclusion Active:</strong> William's PC (<code>85.115.107.223</code>) &amp; Cell (<code>74.209.76.220</code>) are excluded. Showing <strong>only Michael Qin's genuine rep traffic</strong>.</span>
        <button class="btn-mark-sup" onclick="markCurrentDeviceSupervisor()">🔒 Mark Current Device as Supervisor</button>
    </div>

    <!-- KPIs -->
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-num" id="kpi-opens">0</div>
            <div class="kpi-lbl">Michael Active Sessions</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-num" id="kpi-reactions" style="color: var(--blue);">0</div>
            <div class="kpi-lbl">Reactions &amp; Turns</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-num" id="kpi-copies" style="color: #8b5cf6;">0</div>
            <div class="kpi-lbl">Scripts Copied</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-num" id="kpi-last-active" style="font-size: 14px; padding-top: 7px;">--</div>
            <div class="kpi-lbl">Last Heartbeat</div>
        </div>
    </div>

    <!-- Controls & Filters Bar -->
    <div class="controls-bar">
        <div class="filter-pills">
            <button class="pill-btn active" onclick="setFilter('ALL', this)">All Events</button>
            <button class="pill-btn" onclick="setFilter('REACTION', this)">📞 Reactions</button>
            <button class="pill-btn" onclick="setFilter('SCRIPT_COPIED', this)">📋 Copies</button>
            <button class="pill-btn" onclick="setFilter('OPEN', this)">📱 Opens</button>
        </div>

        <div class="action-group">
            <button class="pill-btn active" id="btn-toggle-sup" onclick="toggleSupervisorView()" style="background:#f1f5f9; color:#475569; border-color:#cbd5e1; font-weight:700;">👤 Show My Activity: ON</button>
            <button class="btn-action secondary" onclick="toggleAudioChime()" id="btn-audio">🔔 Chimes: Off</button>
            <button class="btn-action secondary" onclick="clearLocalFeed()">🗑️ Clear</button>
            <button class="btn-action" onclick="fetchRecentEvents()">🔄 Refresh</button>
        </div>
    </div>

    <!-- Live Feed -->
    <div class="feed-card">
        <div class="feed-header">
            <span>⚡ Live Telemetry Stream</span>
            <span id="event-count-badge" style="font-size: 11px; font-family: var(--mono); color: var(--muted);">0 events recorded</span>
        </div>
        <div class="event-list" id="event-list">
            <div class="empty-state">Listening for real-time telemetry from Michael's device...</div>
        </div>
    </div>

    <!-- Diagnostic Details -->
    <div class="diag-box">
        <strong>Tracking Topic:</strong> {TELEMETRY_TOPIC} | <strong>Supervisor Devices (You):</strong> PC (85.115.107.223), S24 Ultra (74.209.76.220) | <strong>Rep (Michael Qin):</strong> All Other Devices &amp; External IPs
    </div>

</div>

<script>
const TELEMETRY_TOPIC = "{TELEMETRY_TOPIC}";
const SSE_URL = "https://ntfy.sh/" + TELEMETRY_TOPIC + "/sse";
const POLL_URL = "https://ntfy.sh/" + TELEMETRY_TOPIC + "/json?poll=1&since=all";
const SUPERVISOR_IPS = ['85.115.107.223', '74.209.76.220'];

let rawEvents = [];
let activeFilter = 'ALL';
let showSupervisorTraffic = true;
let audioEnabled = false;
let michaelLastSeen = null;
let supervisorLastSeen = null;
let counters = {{ opens: 0, reactions: 0, copies: 0 }};

function markCurrentDeviceSupervisor() {{
    localStorage.setItem('ccs_is_supervisor', 'true');
    alert("This browser is permanently marked as Supervisor (You). Activity will be labeled as [👤 YOU].");
}}

function toggleSupervisorView() {{
    showSupervisorTraffic = !showSupervisorTraffic;
    const btn = document.getElementById('btn-toggle-sup');
    if (showSupervisorTraffic) {{
        btn.innerText = '👤 Show My Activity: ON';
        btn.style.background = '#f1f5f9';
        btn.style.color = '#475569';
    }} else {{
        btn.innerText = '👤 Show My Activity: OFF';
        btn.style.background = '#e2e8f0';
        btn.style.color = '#94a3b8';
    }}
    renderEventList();
}}

function clearLocalFeed() {{
    rawEvents = [];
    counters = {{ opens: 0, reactions: 0, copies: 0 }};
    michaelLastSeen = null;
    supervisorLastSeen = null;
    updateUI();
}}

function toggleAudioChime() {{
    audioEnabled = !audioEnabled;
    const btn = document.getElementById('btn-audio');
    btn.innerText = audioEnabled ? '🔔 Chimes: ON' : '🔔 Chimes: Off';
    btn.style.background = audioEnabled ? '#166534' : '';
    btn.style.color = audioEnabled ? '#ffffff' : '';
}}

function playChime() {{
    if (!audioEnabled) return;
    try {{
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.frequency.value = 587.33;
        gain.gain.setValueAtTime(0.1, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);
        osc.start();
        osc.stop(ctx.currentTime + 0.35);
    }} catch(e) {{}}
}}

function setFilter(filterType, btn) {{
    activeFilter = filterType;
    document.querySelectorAll('.filter-pills .pill-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderEventList();
}}

function formatTime(isoStr) {{
    try {{
        const d = new Date(isoStr);
        return d.toLocaleTimeString([], {{ hour: '2-digit', minute: '2-digit', second: '2-digit' }});
    }} catch(e) {{
        return isoStr || '';
    }}
}}

function getRelativeTime(isoStr) {{
    if (!isoStr) return '--';
    const diffSec = Math.floor((Date.now() - new Date(isoStr).getTime()) / 1000);
    if (diffSec < 45) return 'Active Just Now';
    if (diffSec < 120) return '1 min ago';
    if (diffSec < 3600) return `${{Math.floor(diffSec / 60)}} mins ago`;
    return `${{Math.floor(diffSec / 3600)}} hours ago`;
}}

function processEventData(data, isLive = false) {{
    if (!data || !data.action) return;
    if (data.url?.startsWith('file:')) return; // ignore local PDF builds

    // Discard any older mock/diagnostic pings and pre-deployment test sessions
    const isMock = (
        data.sessionId === 'test_verification' ||
        data.sessionId === 'rep_a65ncny' ||
        data.sessionId?.startsWith('diag_test') ||
        data.sessionId?.startsWith('test_') ||
        data.device === 'Supervisor Diagnostic' ||
        data.device === 'Supervisor Cockpit Console' ||
        data.rep === 'Test Rep'
    );
    if (isMock) return;

    // Multi-Person Identity Resolver:
    function getPersonInfo(e) {{
        const ip = e.ip || '';
        const dev = e.device || '';
        const loc = e.location || '';
        
        if (e.isSupervisor === true || ip === '85.115.107.223' || ip === '74.209.76.220' || e.rep?.includes('Supervisor') || e.rep?.includes('William') || dev?.includes('William')) {{
            return {{ name: 'William', role: 'supervisor', badge: '<span class="device-pill" style="background:#f1f5f9; color:#475569; border:1px solid #cbd5e1; font-weight:800;">👑 YOU (Supervisor)</span>', cardStyle: 'border-left-color:#64748b; background:#f8fafc;' }};
        }}
        if (ip === '69.203.0.85' || loc.includes('Staten Island') || (dev.includes('iPhone') && e.details?.screen === '428x751')) {{
            return {{ name: 'Michael Qin', role: 'rep', badge: '<span class="device-pill" style="background:#16a34a; color:#ffffff; border:1px solid #15803d; font-weight:800; letter-spacing:0.3px;">🟢 MICHAEL QIN (Rep — Staten Island)</span>', cardStyle: 'border-left-color:#16a34a; background:#f0fdf4;' }};
        }}
        if (ip === '68.132.69.243' || loc.includes('Huntington') || (dev.includes('Android') && e.details?.screen === '378x656')) {{
            return {{ name: 'Salvatore', role: 'brother', badge: '<span class="device-pill" style="background:#0284c7; color:#ffffff; border:1px solid #0369a1; font-weight:800; letter-spacing:0.3px;">👤 SALVATORE (Brother — Huntington, NY)</span>', cardStyle: 'border-left-color:#0284c7; background:#f0f9ff;' }};
        }}
        if (ip === '2600:387:15:2911::5' || loc.includes('White Plains') || (dev.includes('iPhone') && e.details?.screen === '393x754')) {{
            return {{ name: 'David Qin', role: 'father', badge: '<span class="device-pill" style="background:#8b5cf6; color:#ffffff; border:1px solid #7c3aed; font-weight:800; letter-spacing:0.3px;">👨‍👦 DAVID QIN (Father — AT&T Cellular)</span>', cardStyle: 'border-left-color:#8b5cf6; background:#faf5ff;' }};
        }}
        return {{ name: e.rep || 'Guest', role: 'guest', badge: `<span class="device-pill" style="background:#64748b; color:#ffffff; border:1px solid #475569; font-weight:800;">📱 GUEST (${{dev || 'Mobile'}})</span>`, cardStyle: 'border-left-color:#64748b; background:#f8fafc;' }};
    }}

    // Strict Device & Rep Identification:
    const person = getPersonInfo(data);
    const isWilliam = person.role === 'supervisor';
    data.isWilliam = isWilliam;
    data.person = person;

    // Deduplicate by timestamp + sessionId + action
    const exists = rawEvents.some(e => e.ts === data.ts && e.sessionId === data.sessionId && e.action === data.action);
    if (exists) return;

    rawEvents.unshift(data);

    if (isWilliam) {{
        supervisorLastSeen = data.ts;
    }} else if (person.role === 'rep') {{
        michaelLastSeen = data.ts;
        if (data.action === 'OPEN') counters.opens++;
        if (data.action === 'REACTION') counters.reactions++;
        if (data.action === 'SCRIPT_COPIED') counters.copies++;
    }}

    if (isLive) playChime();

    updateUI();
}}

function updateUI() {{
    document.getElementById('kpi-opens').innerText = counters.opens;
    document.getElementById('kpi-reactions').innerText = counters.reactions;
    document.getElementById('kpi-copies').innerText = counters.copies;
    document.getElementById('kpi-last-active').innerText = getRelativeTime(michaelLastSeen);

    // Live status
    const isMichaelOnline = michaelLastSeen && (Date.now() - new Date(michaelLastSeen).getTime()) < 150000;
    const isWilliamOnline = supervisorLastSeen && (Date.now() - new Date(supervisorLastSeen).getTime()) < 60000;
    const dot = document.getElementById('live-dot');
    const status = document.getElementById('live-status');

    if (isMichaelOnline) {{
        dot.className = 'pulse-dot online';
        dot.style.background = '#22c55e';
        status.innerText = `🟢 Michael Qin Active Now (Staten Island, NY)`;
    }} else if (isWilliamOnline) {{
        dot.className = 'pulse-dot online';
        dot.style.background = '#3b82f6';
        status.innerText = `👑 You Active (Testing) • Michael Qin Idle`;
    }} else if (michaelLastSeen) {{
        dot.className = 'pulse-dot';
        dot.style.background = '#94a3b8';
        status.innerText = `⚪ Michael Last Seen: ${{getRelativeTime(michaelLastSeen)}}`;
    }} else {{
        dot.className = 'pulse-dot';
        dot.style.background = '#94a3b8';
        status.innerText = `⚪ Michael Qin Idle`;
    }}

    renderEventList();
}}

function renderEventList() {{
    let listData = rawEvents;
    if (!showSupervisorTraffic) {{
        listData = listData.filter(e => !e.isWilliam);
    }}
    if (activeFilter !== 'ALL') {{
        listData = listData.filter(e => e.action === activeFilter);
    }}

    document.getElementById('event-count-badge').innerText = `${{listData.length}} events (Filter: ${{activeFilter}})`;

    const list = document.getElementById('event-list');
    if (listData.length === 0) {{
        list.innerHTML = `<div class="empty-state">No events matching "${{activeFilter}}". When someone taps or opens the flight deck, telemetry appears here live.</div>`;
        return;
    }}

    list.innerHTML = listData.map(e => {{
        let cls = 'event-item';
        if (e.isWilliam) cls += ' supervisor-test';
        else if (e.action === 'OPEN') cls += ' open';
        else if (e.action === 'REACTION') cls += ' reaction';
        else if (e.action === 'SCRIPT_COPIED') cls += ' copy';
        else if (e.action === 'TONE_CHANGE') cls += ' tone';
        else if (e.action === 'HEARTBEAT') cls += ' heartbeat';

        let detailHtml = '';
        if (e.details) {{
            if (e.details.leadName || e.details.leadCompany) {{
                detailHtml += `<div>Lead: <strong>${{e.details.leadName || 'Unnamed'}}</strong> | Company: <strong>${{e.details.leadCompany || 'N/A'}}</strong></div>`;
            }}
            if (e.details.optionClicked) {{
                detailHtml += `<div>Action: <em>"${{e.details.optionClicked}}"</em></div>`;
            }}
            if (e.details.textSnippet) {{
                detailHtml += `<div>Snippet: <em>${{e.details.textSnippet}}</em></div>`;
            }}
            const remaining = Object.entries(e.details)
                .filter(([k]) => !['leadName', 'leadCompany', 'optionClicked', 'textSnippet'].includes(k))
                .map(([k,v]) => `${{k}}: <strong>${{v}}</strong>`).join(' | ');
            if (remaining) detailHtml += `<div class="event-details-meta">${{remaining}}</div>`;
        }}

        const locBadge = e.location && e.location !== 'Unknown Location' ? `📍 ${{e.location}}` : (e.ip && e.ip !== 'Unknown' ? `IP: ${{e.ip}}` : '');
        const personInfo = e.person || (typeof getPersonInfo === 'function' ? getPersonInfo(e) : {{ badge: '', cardStyle: '' }});

        return `
            <div class="${{cls}}" style="${{personInfo.cardStyle}}">
                <div class="event-main">
                    <div class="event-title">${{e.title || e.action}}</div>
                    <div class="event-details">${{detailHtml || '<span style="color:#94a3b8;">Flight deck interaction</span>'}}</div>
                </div>
                <div class="event-meta">
                    ${{personInfo.badge}}
                    <div style="font-size:9.5px; color:#64748b; font-family:var(--mono); margin-top:2px;">${{locBadge}}</div>
                    <div style="font-size:9.5px; color:#94a3b8; font-family:var(--mono); margin-top:1px;">${{formatTime(e.ts)}}</div>
                </div>
            </div>
        `;
    }}).join('');
}}

// Fetch historical cache on load
async function fetchRecentEvents() {{
    try {{
        const res = await fetch(POLL_URL + "&_t=" + Date.now());
        const text = await res.text();
        const lines = text.trim().split('\\n');
        
        rawEvents = [];
        counters = {{ opens: 0, reactions: 0, copies: 0 }};

        lines.forEach(line => {{
            try {{
                const msg = JSON.parse(line);
                if (msg.message) {{
                    const payload = JSON.parse(msg.message);
                    processEventData(payload, false);
                }}
            }} catch(err) {{}}
        }});
        updateUI();
    }} catch(e) {{
        console.error("Poll error:", e);
    }}
}}

function connectSSE() {{
    const eventSource = new EventSource(SSE_URL);
    
    eventSource.onopen = () => {{
        document.getElementById('live-status').innerText = 'Connected • Live Sync Active';
    }};

    eventSource.onmessage = (event) => {{
        try {{
            const msg = JSON.parse(event.data);
            if (msg.message) {{
                const payload = JSON.parse(msg.message);
                processEventData(payload, true);
            }}
        }} catch(e) {{}}
    }};

    eventSource.onerror = () => {{
        document.getElementById('live-status').innerText = 'Reconnecting...';
        setTimeout(connectSSE, 4000);
    }};
}}

window.addEventListener('DOMContentLoaded', () => {{
    fetchRecentEvents();
    connectSSE();
    setInterval(fetchRecentEvents, 6000); // 6-second background sync fallback
}});
</script>
</body>
</html>"""

    def render_opponent_html(self) -> str:
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

        personas_data = {
            "contractor": {
                "name": "Frank Miller (Owner)",
                "company": "Apex Roofing & Commercial Contracting",
                "vertical": "Commercial Roofing & Trades",
                "location": "Dallas, TX",
                "revenue": "$140,000 / month",
                "debtStack": "OnDeck ($85k bal, $1,150/day) + Rapid ($45k bal, $700/day) = $1,850/day",
                "mood": "Stressed, on a noisy rooftop jobsite. Waiting on a $65k GC draw that is 45 days late.",
                "openers": {
                    "easy": "Yeah Frank here, what can I do for you?",
                    "med": "Yeah Frank here, make it quick, I'm up on a commercial roof right now.",
                    "hard": "I'm on a loud jobsite in the middle of a crane lift. Why are you calling my personal cell?"
                },
                "secret": "He is terrified he won't make next Friday's payroll ($22k) because of the $1,850 daily debit drain, but he's too proud to ask for a loan.",
                "winTrigger": "If Michael says: 'I am calling to stop daily debits while you wait on 60-day GC progress draws, without adding debt,' and locks the 45-second bank app download."
            },
            "trucking": {
                "name": "Big Bob Kowalski (Fleet Owner)",
                "company": "Ironclad Freight & Logistics",
                "vertical": "Long-Haul Freight (8 Trucks)",
                "location": "Chicago, IL",
                "revenue": "$185,000 / month",
                "debtStack": "Fundbox ($65k bal, $1,400/day) + Apex fuel card factoring taking 5% = $2,400/day",
                "mood": "Gruff, cynical. Burned by an offshore broker last year who charged upfront fees.",
                "openers": {
                    "easy": "Bob speaking, who is this?",
                    "med": "Who is this, and what scam list did you buy my cell number from?",
                    "hard": "Look buddy, I get 10 spam calls a day from brokers. What makes you any different?"
                },
                "secret": "His diesel fuel bill is $35k/month and two brokers are 45 days late on $40k in invoices. He desperately needs a clean monthly credit line.",
                "winTrigger": "If Michael assures him: 'We never charge upfront fees and we don't shop your file to 20 brokers—we consolidate fuel debt into clean monthly terms.'"
            },
            "restaurant": {
                "name": "Tony DeMarco (Chef & Owner)",
                "company": "Harbor Bistro & Tavern",
                "vertical": "Full-Service Restaurant & Bar",
                "location": "Boston, MA",
                "revenue": "$95,000 / month",
                "debtStack": "Toast holding 15% of daily credit card batches ($950/day) + Square ($35k bal)",
                "mood": "Chaotic lunch prep in the kitchen. Tickets printing, pans clattering, zero patience.",
                "openers": {
                    "easy": "Harbor Bistro, Tony speaking.",
                    "med": "I'm in the middle of kitchen prep, I don't have time for sales calls, just email me.",
                    "hard": "I'm prepping lunch rush with 4 pans on the fire! Why are you calling during service hours?"
                },
                "secret": "He hates seeing 15% sliced off his weekend dinner receipts before the cash hits his bank.",
                "winTrigger": "If Michael says: 'Stay on with me for 45 seconds on your phone while the water boils so you can keep 100% of your weekend credit card receipts.'"
            },
            "cfo": {
                "name": "Brenda Vance (CFO / Controller)",
                "company": "Precision Aerospace Machining",
                "vertical": "Contract CNC Machining",
                "location": "Cleveland, OH",
                "revenue": "$260,000 / month",
                "debtStack": "Kapitus mezzanine note ($120k bal, $3,600/day) + 3 CNC equipment leases",
                "mood": "Cold, analytical MBA. Hates sales fluff, tests reps on basis points and effective APR.",
                "openers": {
                    "easy": "This is Brenda Vance, how may I direct your call?",
                    "med": "This is Brenda. What is your firm's effective cost of capital and are you an institutional syndicate or a broker?",
                    "hard": "We do not take unvetted capital solicitations. Transmit your firm's FINRA/SEC credentials and rate card to my assistant."
                },
                "secret": "The board ordered her to reduce debt service by 300 basis points this quarter before an upcoming audit.",
                "winTrigger": "If Michael uses the Wall Street tone, cites basis points, senior debt consolidation, and non-dilutive balance-sheet recapitalization."
            },
            "complacent": {
                "name": "Dave Harrison (Owner)",
                "company": "Sunshine State HVAC & Mechanical",
                "vertical": "Commercial & Residential HVAC",
                "location": "Tampa, FL",
                "revenue": "$120,000 / month",
                "debtStack": "Zero active loans. $85k sitting in operating checking.",
                "mood": "Relaxed, confident. Convinced he doesn't need to speak to any finance person.",
                "openers": {
                    "easy": "Dave here, how can I help you today?",
                    "med": "Appreciate the call man, but business is booming, I got plenty of cash in the bank, I don't need a loan.",
                    "hard": "Look, I don't borrow money, never have, never will. Remove me from your database."
                },
                "secret": "He is paying 3.8% on credit card processing fees and overpaying merchant vendor surcharges without knowing it.",
                "winTrigger": "If Michael pivots: 'We don't sell speculative debt—we run a 5-minute honesty check against your bank statements to benchmark whether you are losing $2,500/mo in fee leakage.'"
            },
            "gatekeeper": {
                "name": "Rick (Hostile Co-Owner / Gatekeeper)",
                "company": "Titan Heavy Excavation",
                "vertical": "Excavation & Earthmoving",
                "location": "Pittsburgh, PA",
                "revenue": "$300,000 / month",
                "debtStack": "Cat Financial heavy equipment notes ($18k/mo) + Yellow Iron lease",
                "mood": "Aggressive, furious. Already received 8 telemarketer calls today.",
                "openers": {
                    "easy": "Titan Excavation, what do you want?",
                    "med": "Stop calling me! Take my damn number off your list! Every day you guys spam my phone!",
                    "hard": "If you call this number one more time I am filing an FTC harassment complaint against your company!"
                },
                "secret": "He respects people who don't get rattled or apologize. If you match his energy with steady confidence, he will listen.",
                "winTrigger": "If Michael uses Chris Voss tactical empathy: 'Sounds like you are getting slammed by 15 telemarketers today and you are sick of it... I will be off your phone in 10 seconds.'"
            }
        }

        curveballs_data = [
            {
                "id": "q_who_is_this",
                "q": "📞 \"Who is this & why are you calling my cell?\"",
                "cue": "Testing Michael's 5-second composure and value hook.",
                "spokenLine": "Who is this, and why are you calling my personal cell phone right now?",
                "win": "Winning Move: \"Michael Qin with Creative Capital Solutions. I know I caught you out of the blue, but our desk is actively restructuring high daily debits for [Industry] operators...\"",
                "trap": "Rookie Trap: Apologizing ('Sorry to bother you') or sounding like a robotic telemarketer reading a script."
            },
            {
                "id": "q_dont_need_money",
                "q": "🚫 \"We don't need any money right now, business is good.\"",
                "cue": "The classic brush-off. Tests if he pivots to an audit or folds.",
                "spokenLine": "Look, we're doing great, revenue is strong, and I don't need to borrow any money right now.",
                "win": "Winning Move: \"Glad cash flow is strong. We actually don't place speculative debt—we audit incumbent lenders to stop $2k/mo in fee leakage and keep lenders honest at zero cost.\"",
                "trap": "Rookie Trap: Trying to force a loan or asking 'Are you sure you don't need capital for expansion?'"
            },
            {
                "id": "q_just_email",
                "q": "📧 \"Just email me your rate sheet, I'm busy.\"",
                "cue": "The 90% death trap. Tests the 45-second on-call download ask.",
                "spokenLine": "I'm right in the middle of something. Just send whatever you have to my email and I'll look at it later.",
                "win": "Winning Move: \"Happy to route that over. Rather than sending generic decks you'll never read, are you looking at your phone right now? Pull up your banking app for 45 seconds while I confirm receipt...\"",
                "trap": "Rookie Trap: Saying 'Sure, what's your email?' and hanging up with 0% chance of closing."
            },
            {
                "id": "q_what_rates",
                "q": "🏷️ \"What are your exact rates? Give me a percentage.\"",
                "cue": "Price pressure trap. Tests if he quotes a blind rate or trades for statements.",
                "spokenLine": "Before we talk about anything, what are your exact rates? Give me a percentage or APR.",
                "win": "Winning Move: \"Rates depend entirely on monthly deposits, but we consistently cut daily debit payments in half. Rather than quoting a misleading ballpark, send 3 statements and I'll have your exact rate card in 3 hours.\"",
                "trap": "Rookie Trap: Quoting a random number like '8% to 15%' which destroys credibility."
            },
            {
                "id": "q_why_statements",
                "q": "🔒 \"Why do you need bank statements? I'm not sending docs.\"",
                "cue": "Security friction. Tests if he offers account number redaction.",
                "spokenLine": "Why do you need my bank statements right away? I'm not emailing my company financials to a stranger.",
                "win": "Winning Move: \"Totally understand—your numbers are sensitive. We don't shop your file to 20 brokers. You can redact your account numbers. We just need the deposit volume to calculate your term sheet.\"",
                "trap": "Rookie Trap: Getting defensive or arguing 'That's just company policy.'"
            },
            {
                "id": "q_already_have_debt",
                "q": "💸 \"I already have 2 loans with OnDeck taking $1,800/day.\"",
                "cue": "The golden consolidation lead! Tests if he identifies the consolidation play.",
                "spokenLine": "I already have two MCA advances with OnDeck and Rapid taking $1,800 out of my account every single day, so I can't take any more debt.",
                "win": "Winning Move: \"That's exactly why I called. We specialize in rolling stacked daily ACH positions out of OnDeck into a single clean monthly schedule to cut your debit drain by 40%.\"",
                "trap": "Rookie Trap: Treating it as a rejection instead of the highest-converting opportunity."
            },
            {
                "id": "q_driving",
                "q": "⏳ \"I'm on a noisy roof / driving on the highway right now.\"",
                "cue": "Time barrier. Tests the 1-click SMS pivot.",
                "spokenLine": "I can barely hear you, I'm driving 70 on the highway / up on a crane lift right now.",
                "win": "Winning Move: \"Understood, drive safe. I am texting my direct upload link to this mobile number right now. Reply with the 3 PDFs when you park and I'll run the numbers today.\"",
                "trap": "Rookie Trap: Trying to keep talking while they are clearly unable to look at anything."
            },
            {
                "id": "q_broker_shopping",
                "q": "🛑 \"Are you just another broker who's gonna blast my credit?\"",
                "cue": "Trust test. Tests CCAP's direct private credit positioning.",
                "spokenLine": "Are you just another middleman broker who's gonna take my file and blast it to 30 lenders across the country?",
                "win": "Winning Move: \"No. We operate a direct syndication desk in New York. We conduct an in-house preliminary audit. Your file is never blasted to public market portals.\"",
                "trap": "Rookie Trap: Stuttering or giving a vague answer about 'our network of 50 partners.'"
            }
        ]

        personas_json = json.dumps(personas_data)
        curveballs_json = json.dumps(curveballs_data)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Merchant Sparring Arena &amp; Roleplay Trainer - Creative Capital Solutions</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
<style>
    :root {{
        --bg: #f8fafc;
        --card: #ffffff;
        --border: #cbd5e1;
        --border-subtle: #e2e8f0;
        --navy: #0f2744;
        --navy-dark: #091728;
        --accent: #dc2626;
        --accent-hover: #b91c1c;
        --blue: #2563eb;
        --blue-hover: #1d4ed8;
        --text: #0f172a;
        --muted: #64748b;
        --success: #15803d;
        --success-bg: #dcfce7;
        --success-border: #86efac;
        --danger: #b91c1c;
        --danger-bg: #fee2e2;
        --danger-border: #fca5a5;
        --warning: #b45309;
        --warning-bg: #fef3c7;
        --warning-border: #fde68a;
        --purple: #6d28d9;
        --purple-bg: #f5f3ff;
        --purple-border: #ddd6fe;
        --font: 'Plus Jakarta Sans', sans-serif;
        --mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
        background-color: var(--bg);
        color: var(--text);
        font-family: var(--font);
        line-height: 1.4;
        font-size: 13px;
        padding: 10px;
    }}

    .arena-wrap {{
        max-width: 1360px;
        margin: 0 auto;
    }}

    /* Header */
    .arena-header {{
        background: var(--card);
        border: 1px solid var(--border);
        border-top: 4px solid var(--accent);
        padding: 10px 14px;
        border-radius: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        flex-wrap: wrap;
        gap: 8px;
    }}
    .brand-block {{
        display: flex;
        align-items: center;
        gap: 6px;
        flex-wrap: wrap;
    }}
    .brand-title {{
        font-size: 14px;
        font-weight: 800;
        color: var(--navy);
        letter-spacing: -0.2px;
    }}
    .status-tag {{
        background: #fee2e2;
        color: var(--accent);
        font-size: 9.5px;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 3px;
        text-transform: uppercase;
    }}
    .rep-tag {{
        background: #f1f5f9;
        color: var(--navy);
        font-size: 9.5px;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 3px;
        border: 1px solid var(--border-subtle);
    }}

    .header-right {{
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .pulse-box {{
        display: flex;
        align-items: center;
        gap: 8px;
        background: #f1f5f9;
        border: 1px solid var(--border);
        padding: 5px 10px;
        border-radius: 20px;
    }}
    .pulse-dot {{
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #94a3b8;
    }}
    .pulse-dot.online {{
        background: #22c55e;
        box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.25);
        animation: pulseAnim 1.8s infinite;
    }}
    @keyframes pulseAnim {{
        0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }}
        70% {{ transform: scale(1); box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); }}
        100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }}
    }}
    .pulse-status {{
        font-size: 11px;
        font-weight: 700;
        color: var(--navy);
    }}

    .btn-nav {{
        background: #ffffff;
        color: var(--navy);
        border: 1px solid var(--border);
        text-decoration: none;
        padding: 4px 8px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        transition: all 0.1s;
    }}
    .btn-nav:hover {{ background: #f1f5f9; border-color: var(--navy); }}
    .btn-nav.primary {{ background: var(--navy); color: #ffffff; border-color: var(--navy); }}
    .btn-nav.primary:hover {{ background: var(--navy-dark); }}

    /* 3-Column Arena Grid */
    .arena-grid {{
        display: grid;
        grid-template-columns: 1.1fr 1.4fr 0.95fr;
        gap: 10px;
    }}
    @media (max-width: 1024px) {{
        .arena-grid {{ grid-template-columns: 1fr; }}
    }}

    .arena-card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 12px;
        display: flex;
        flex-direction: column;
        gap: 8px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }}

    .card-head {{
        font-size: 11.5px;
        font-weight: 800;
        text-transform: uppercase;
        color: var(--navy);
        letter-spacing: 0.3px;
        padding-bottom: 5px;
        border-bottom: 1px solid var(--border-subtle);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    /* Persona Selector Chips */
    .persona-chips {{
        display: flex;
        gap: 3px;
        flex-wrap: wrap;
    }}
    .persona-btn {{
        background: #f8fafc;
        border: 1px solid var(--border-subtle);
        color: var(--navy);
        padding: 4px 6px;
        border-radius: 3px;
        font-size: 10.5px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.1s;
    }}
    .persona-btn:hover {{ background: #e2e8f0; }}
    .persona-btn.active {{
        background: var(--navy);
        border-color: var(--navy);
        color: #ffffff;
    }}

    /* Difficulty Setting */
    .diff-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #f8fafc;
        border: 1px solid var(--border-subtle);
        padding: 4px 6px;
        border-radius: 3px;
        font-size: 10.5px;
    }}
    .diff-btns {{
        display: flex;
        gap: 2px;
    }}
    .diff-btn {{
        background: #ffffff;
        border: 1px solid var(--border-subtle);
        padding: 2px 6px;
        border-radius: 2px;
        font-size: 9.5px;
        font-weight: 700;
        cursor: pointer;
    }}
    .diff-btn.active.easy {{ background: var(--success-bg); color: var(--success); border-color: var(--success-border); }}
    .diff-btn.active.med {{ background: var(--warning-bg); color: var(--warning); border-color: var(--warning-border); }}
    .diff-btn.active.hard {{ background: var(--danger-bg); color: var(--danger); border-color: var(--danger-border); }}

    /* Dossier Table */
    .dossier-box {{
        background: #f8fafc;
        border: 1px solid var(--border-subtle);
        border-radius: 3px;
        padding: 8px 10px;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }}
    .dossier-row {{
        display: flex;
        justify-content: space-between;
        font-size: 11px;
        border-bottom: 1px dashed var(--border-subtle);
        padding-bottom: 3px;
    }}
    .dossier-lbl {{ color: var(--muted); font-weight: 600; }}
    .dossier-val {{ color: var(--navy); font-weight: 700; text-align: right; }}

    .opener-box {{
        background: #ffffff;
        border: 1px solid var(--border);
        border-left: 3.5px solid var(--navy);
        padding: 6px 8px;
        border-radius: 2px;
        font-size: 11.5px;
    }}

    .secret-box {{
        background: var(--danger-bg);
        border: 1px solid var(--danger-border);
        border-left: 3.5px solid var(--danger);
        padding: 6px 8px;
        border-radius: 2px;
        font-size: 11px;
        color: var(--danger);
    }}

    .win-trigger-box {{
        background: var(--success-bg);
        border: 1px solid var(--success-border);
        border-left: 3.5px solid var(--success);
        padding: 6px 8px;
        border-radius: 2px;
        font-size: 11px;
        color: var(--success);
    }}

    /* Live Teleprompter (Col 2) */
    .live-mirror-card {{
        background: #f8fafc;
        border: 1px solid #bfdbfe;
        border-left: 4px solid var(--blue);
        padding: 8px 10px;
        border-radius: 3px;
    }}
    .live-mirror-head {{
        display: flex;
        justify-content: space-between;
        font-size: 9.5px;
        font-weight: 800;
        text-transform: uppercase;
        color: var(--blue);
        margin-bottom: 3px;
    }}
    .live-stage-title {{
        font-size: 12.5px;
        font-weight: 800;
        color: var(--navy);
        margin-bottom: 2px;
    }}
    .live-stage-desc {{
        font-size: 11px;
        color: var(--muted);
        background: #ffffff;
        padding: 4px 6px;
        border-radius: 2px;
        border: 1px solid var(--border-subtle);
        font-family: var(--mono);
    }}

    /* Curveball Soundboard */
    .curveball-list {{
        display: flex;
        flex-direction: column;
        gap: 5px;
    }}
    .curve-card {{
        background: #ffffff;
        border: 1px solid var(--border-subtle);
        border-radius: 3px;
        padding: 6px 8px;
        transition: all 0.1s;
    }}
    .curve-card:hover {{
        border-color: var(--navy);
        background: #f8fafc;
    }}
    .curve-card.active {{
        border-color: var(--accent);
        background: #fffafa;
        box-shadow: 0 0 0 1px var(--accent);
    }}
    .curve-q-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
    }}
    .curve-q {{
        font-size: 11.5px;
        font-weight: 800;
        color: var(--navy);
    }}
    .curve-card.active .curve-q {{ color: var(--accent); }}
    .curve-cue {{
        font-size: 10.5px;
        color: var(--muted);
        margin-top: 2px;
    }}

    .curve-actions-row {{
        display: flex;
        gap: 4px;
        margin-top: 4px;
    }}
    .btn-action-sm {{
        background: #f1f5f9;
        border: 1px solid var(--border);
        color: var(--navy);
        padding: 2px 6px;
        border-radius: 2px;
        font-size: 9.5px;
        font-weight: 700;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 3px;
    }}
    .btn-action-sm:hover {{ background: #e2e8f0; }}
    .btn-action-sm.fire {{ background: #fee2e2; color: var(--accent); border-color: #fca5a5; }}
    .btn-action-sm.fire:hover {{ background: #fecaca; }}

    .curve-detail {{
        margin-top: 6px;
        padding-top: 6px;
        border-top: 1px dashed var(--border-subtle);
        display: none;
        flex-direction: column;
        gap: 4px;
    }}
    .curve-card.active .curve-detail {{ display: flex; }}

    .pill-win {{
        background: var(--success-bg);
        border: 1px solid var(--success-border);
        color: var(--success);
        padding: 4px 6px;
        border-radius: 2px;
        font-size: 11px;
    }}
    .pill-trap {{
        background: var(--danger-bg);
        border: 1px solid var(--danger-border);
        color: var(--danger);
        padding: 4px 6px;
        border-radius: 2px;
        font-size: 11px;
    }}

    /* Enhanced Stopwatch & Scorecard (Col 3) */
    .timer-block {{
        background: #f8fafc;
        border: 1px solid var(--border-subtle);
        border-radius: 3px;
        padding: 8px 10px;
        text-align: center;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }}
    .timer-status-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 10px;
        font-weight: 700;
        color: var(--muted);
    }}
    .timer-status-badge {{
        font-size: 9px;
        font-weight: 800;
        text-transform: uppercase;
        padding: 2px 6px;
        border-radius: 3px;
        background: #e2e8f0;
        color: var(--muted);
    }}
    .timer-status-badge.running {{
        background: var(--success-bg);
        color: var(--success);
        border: 1px solid var(--success-border);
    }}
    .timer-status-badge.paused {{
        background: var(--warning-bg);
        color: var(--warning);
        border: 1px solid var(--warning-border);
    }}
    .timer-status-badge.overtime {{
        background: var(--danger-bg);
        color: var(--danger);
        border: 1px solid var(--danger-border);
    }}
    .timer-num {{
        font-family: var(--mono);
        font-size: 32px;
        font-weight: 800;
        color: var(--navy);
        letter-spacing: 2px;
        line-height: 1;
        transition: color 0.2s;
    }}
    .timer-num.overtime {{
        color: var(--danger);
    }}
    .timer-ctrls {{
        display: flex;
        justify-content: center;
        gap: 4px;
        flex-wrap: wrap;
    }}
    .btn-t {{
        background: var(--navy);
        color: #ffffff;
        border: none;
        padding: 4px 8px;
        border-radius: 2px;
        font-weight: 700;
        font-size: 10px;
        cursor: pointer;
        transition: all 0.1s;
    }}
    .btn-t:hover {{ opacity: 0.9; }}
    .btn-t.start {{ background: #16a34a; }}
    .btn-t.pause {{ background: #ca8a04; }}
    .btn-t.reset-timer {{ background: #64748b; }}
    .btn-t.preset {{ background: #ffffff; color: var(--navy); border: 1px solid var(--border-subtle); font-size: 9px; padding: 2px 6px; }}
    .btn-t.preset:hover {{ background: #f1f5f9; }}

    /* Score Header Badge */
    .score-grade-badge {{
        font-size: 10px;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 3px;
        background: #f1f5f9;
        color: var(--navy);
        border: 1px solid var(--border-subtle);
    }}
    .score-grade-badge.grade-a {{ background: var(--success-bg); color: var(--success); border-color: var(--success-border); }}
    .score-grade-badge.grade-b {{ background: #dbeafe; color: var(--blue); border-color: #bfdbfe; }}
    .score-grade-badge.grade-c {{ background: var(--warning-bg); color: var(--warning); border-color: var(--warning-border); }}
    .score-grade-badge.grade-f {{ background: var(--danger-bg); color: var(--danger); border-color: var(--danger-border); }}

    /* Rubrics */
    .rubric-row {{
        display: flex;
        flex-direction: column;
        gap: 3px;
        margin-bottom: 4px;
    }}
    .rubric-lbl {{
        font-size: 10.5px;
        font-weight: 700;
        color: var(--muted);
        display: flex;
        justify-content: space-between;
    }}
    .rubric-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 3px;
    }}
    .rubric-pill {{
        background: #f8fafc;
        border: 1px solid var(--border-subtle);
        color: var(--muted);
        padding: 3px 4px;
        border-radius: 2px;
        font-size: 9px;
        font-weight: 700;
        cursor: pointer;
        text-align: center;
        transition: all 0.1s;
    }}
    .rubric-pill:hover {{ color: var(--navy); border-color: var(--navy); }}
    .rubric-pill.red.active {{ background: var(--danger-bg); color: var(--danger); border-color: var(--danger); font-weight: 800; }}
    .rubric-pill.amber.active {{ background: var(--warning-bg); color: var(--warning); border-color: var(--warning); font-weight: 800; }}
    .rubric-pill.green.active {{ background: var(--success-bg); color: var(--success); border-color: var(--success); font-weight: 800; }}

    /* Quick Coaching Tags */
    .quick-tags-row {{
        display: flex;
        gap: 3px;
        flex-wrap: wrap;
        margin-top: 2px;
        margin-bottom: 3px;
    }}
    .btn-quick-tag {{
        background: #ffffff;
        border: 1px solid var(--border-subtle);
        color: var(--navy);
        font-size: 9px;
        font-weight: 700;
        padding: 2px 5px;
        border-radius: 2px;
        cursor: pointer;
        transition: all 0.1s;
    }}
    .btn-quick-tag:hover {{
        background: #f1f5f9;
        border-color: var(--navy);
    }}

    .notes-input {{
        width: 100%;
        min-height: 55px;
        background: #f8fafc;
        border: 1px solid var(--border-subtle);
        color: var(--navy);
        padding: 5px 6px;
        font-size: 11px;
        border-radius: 2px;
        resize: vertical;
        font-family: inherit;
    }}

    .action-btns-row {{
        display: flex;
        gap: 4px;
    }}
    .btn-debrief-copy {{
        flex: 1.3;
        background: var(--navy);
        color: #ffffff;
        border: none;
        padding: 6px 8px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: 800;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 4px;
        transition: background 0.1s;
    }}
    .btn-debrief-copy:hover {{ background: var(--navy-dark); }}

    .btn-reset-round {{
        flex: 0.9;
        background: #f1f5f9;
        color: var(--navy);
        border: 1px solid var(--border);
        padding: 6px 8px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: 700;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 4px;
        transition: all 0.1s;
    }}
    .btn-reset-round:hover {{ background: #e2e8f0; border-color: var(--navy); }}

    /* History Drawer */
    .rounds-history-box {{
        margin-top: 5px;
        padding-top: 5px;
        border-top: 1px dashed var(--border-subtle);
        display: flex;
        flex-direction: column;
        gap: 4px;
    }}
    .history-head {{
        display: flex;
        justify-content: space-between;
        font-size: 9.5px;
        font-weight: 800;
        color: var(--muted);
        text-transform: uppercase;
    }}
    .history-list {{
        display: flex;
        flex-direction: column;
        gap: 3px;
        max-height: 110px;
        overflow-y: auto;
    }}
    .history-item {{
        background: #f8fafc;
        border: 1px solid var(--border-subtle);
        padding: 4px 6px;
        border-radius: 2px;
        font-size: 9.5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    /* Mobile Navigation Sticky Tab Bar (Screens <= 768px) */
    .mobile-tab-bar {{
        display: none;
    }}

    @media (max-width: 768px) {{
        body {{
            padding: 4px;
        }}
        .arena-wrap {{
            max-width: 100%;
            padding: 2px;
            gap: 6px;
        }}
        .arena-header {{
            padding: 8px 10px;
            flex-direction: column;
            align-items: stretch;
            gap: 6px;
        }}
        .brand-block {{
            justify-content: flex-start;
            flex-wrap: wrap;
            gap: 4px;
        }}
        .header-right {{
            justify-content: space-between;
            width: 100%;
            border-top: 1px dashed var(--border-subtle);
            padding-top: 5px;
        }}
        .pulse-box {{
            padding: 2px 6px;
        }}
        .pulse-status {{
            font-size: 10px;
        }}

        /* Mobile Sticky Navigation Tabs */
        .mobile-tab-bar {{
            display: grid;
            grid-template-columns: 1fr 1.2fr 1fr;
            gap: 4px;
            position: sticky;
            top: 0px;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.96);
            backdrop-filter: blur(10px);
            padding: 6px 2px;
            margin-bottom: 2px;
            border-bottom: 1px solid var(--border-subtle);
        }}
        .m-tab-btn {{
            background: #f8fafc;
            border: 1px solid var(--border);
            color: var(--navy);
            padding: 7px 4px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 800;
            text-align: center;
            cursor: pointer;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
            transition: all 0.15s;
        }}
        .m-tab-btn.active {{
            background: var(--navy);
            color: #ffffff;
            border-color: var(--navy);
        }}

        /* Column 1 Mobile Improvements */
        .persona-chips {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 4px;
        }}
        .persona-btn {{
            padding: 7px 2px;
            font-size: 10px;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .diff-row {{
            flex-direction: column;
            align-items: stretch;
            gap: 4px;
            padding: 6px 8px;
        }}
        .diff-btns {{
            display: flex;
            width: 100%;
            gap: 4px;
        }}
        .diff-btn {{
            flex: 1;
            padding: 6px 0;
            font-size: 10.5px;
            text-align: center;
        }}
        .dossier-box {{
            padding: 8px 10px;
        }}
        .dossier-row {{
            display: flex;
            flex-direction: column;
            gap: 2px;
            padding: 4px 0;
        }}
        .dossier-lbl {{
            font-size: 10px;
            text-transform: uppercase;
        }}
        .dossier-val {{
            text-align: left;
            font-size: 11.5px;
            line-height: 1.3;
        }}
        .opener-box, .secret-box, .win-trigger-box {{
            padding: 7px 9px;
            font-size: 11.5px;
            line-height: 1.35;
        }}

        /* Column 2 Curveballs Mobile Improvements */
        .curve-q-row {{
            align-items: flex-start;
            gap: 6px;
        }}
        .curve-q {{
            font-size: 12px;
            line-height: 1.3;
        }}
        .curve-actions-row {{
            display: flex;
            gap: 6px;
            width: 100%;
            margin-top: 6px;
        }}
        .btn-action-sm {{
            flex: 1;
            padding: 7px 4px;
            font-size: 10.5px;
            justify-content: center;
        }}

        /* Column 3 Scorecard Mobile Improvements */
        .timer-ctrls {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 4px;
        }}
        .timer-presets-row {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 4px;
            margin-top: 4px;
        }}
        .btn-t {{
            padding: 7px 4px;
            font-size: 11px;
            text-align: center;
        }}
        .rubric-row {{
            margin-bottom: 6px;
        }}
        .rubric-grid {{
            gap: 4px;
        }}
        .rubric-pill {{
            padding: 7px 2px;
            font-size: 9.5px;
            line-height: 1.2;
        }}
        .quick-tags-row {{
            display: flex;
            gap: 4px;
            flex-wrap: wrap;
            margin: 4px 0;
        }}
        .btn-quick-tag {{
            padding: 4px 6px;
            font-size: 9.5px;
        }}
        .action-btns-row {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .btn-debrief-copy, .btn-reset-round {{
            width: 100%;
            padding: 9px 10px;
            font-size: 12px;
        }}
    }}

    .toast {{
        position: fixed;
        bottom: 12px;
        right: 12px;
        background: var(--navy);
        color: #ffffff;
        font-weight: 700;
        font-size: 11px;
        padding: 5px 10px;
        border-radius: 3px;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.15s ease;
        z-index: 2000;
    }}
    .toast.show {{ opacity: 1; }}
</style>
</head>
<body>

<div class="arena-wrap">

    <!-- Header -->
    <div class="arena-header">
        <div class="brand-block">
            <span class="brand-title">Creative Capital Solutions</span>
            <span class="status-tag">🥊 Roleplay Arena</span>
            <span class="rep-tag">Opponent: William (Supervisor)</span>
            <span class="rep-tag">Rep: Michael Qin</span>
        </div>

        <div class="header-right">
            <div class="pulse-box">
                <div class="pulse-dot" id="live-dot"></div>
                <span class="pulse-status" id="rep-status-text">Listening for Michael Qin...</span>
            </div>
            <a href="admin.html" class="btn-nav">📡 Cockpit</a>
            <a href="index.html" class="btn-nav primary" target="_blank">📱 Rep Flight Deck</a>
        </div>
    </div>

    <!-- Mobile Sticky Jump Tabs (Screens <= 768px) -->
    <div class="mobile-tab-bar">
        <button class="m-tab-btn active" onclick="jumpToSection('sec-persona', this)">🎭 Persona</button>
        <button class="m-tab-btn" onclick="jumpToSection('sec-curveballs', this)">🎯 Curveballs (8)</button>
        <button class="m-tab-btn" onclick="jumpToSection('sec-scorecard', this)">⏱️ Scorecard</button>
    </div>

    <!-- 3-Column Arena Grid -->
    <div class="arena-grid">

        <!-- COLUMN 1: MERCHANT PERSONA & FACTS -->
        <div class="arena-card" id="sec-persona">
            <div class="card-head">
                <span>🎭 Merchant Persona Dossier</span>
                <span style="font-size: 9.5px; color: var(--muted);">Who you are playing</span>
            </div>

            <!-- Persona Selector Chips -->
            <div class="persona-chips">
                <button class="persona-btn active" onclick="selectPersona('contractor', this)">🏗️ Contractor</button>
                <button class="persona-btn" onclick="selectPersona('trucking', this)">🚛 Trucking</button>
                <button class="persona-btn" onclick="selectPersona('restaurant', this)">🍽️ Restaurant</button>
                <button class="persona-btn" onclick="selectPersona('cfo', this)">📊 CFO</button>
                <button class="persona-btn" onclick="selectPersona('complacent', this)">🤝 No Debt</button>
                <button class="persona-btn" onclick="selectPersona('gatekeeper', this)">🥊 Hostile</button>
            </div>

            <!-- Difficulty Settings -->
            <div class="diff-row">
                <span style="font-weight: 700; color: var(--muted);">Resistance Level:</span>
                <div class="diff-btns">
                    <button class="diff-btn easy active" onclick="setDifficulty('easy', this)">🟢 Warm</button>
                    <button class="diff-btn med" onclick="setDifficulty('med', this)">🟡 Realistic</button>
                    <button class="diff-btn hard" onclick="setDifficulty('hard', this)">🔴 Hardcore</button>
                </div>
            </div>

            <!-- Detailed Dossier -->
            <div class="dossier-box" id="dossier-content"></div>

            <!-- Secret Intel Box -->
            <div class="secret-box" id="secret-intel-box"></div>

            <!-- Win Trigger Box -->
            <div class="win-trigger-box" id="win-trigger-box"></div>
        </div>

        <!-- COLUMN 2: LIVE TELEPROMPTER & CURVEBALL SOUNDBOARD -->
        <div class="arena-card" id="sec-curveballs">
            <div class="card-head">
                <span>⚡ Live Stage Tracker &amp; Pushbacks</span>
                <span id="live-actor-tag" style="font-size: 10px; color: var(--blue); font-family: var(--mono);">Sync Active</span>
            </div>

            <!-- Live Mirror Box (What Michael is doing right now) -->
            <div class="live-mirror-card">
                <div class="live-mirror-head">
                    <span>📡 Michael Qin Live Position:</span>
                    <span id="mirror-time">--</span>
                </div>
                <div class="live-stage-title" id="mirror-stage">Stage 1: Opening (0-5s)</div>
                <div class="live-stage-desc" id="mirror-script">Waiting for dial telemetry...</div>
            </div>

            <div style="font-size: 11px; font-weight: 800; color: var(--navy); text-transform: uppercase; margin-top: 2px;">
                🎯 Opponent Curveballs (Say These Aloud to Test Him):
            </div>

            <!-- Curveball Soundboard -->
            <div class="curveball-list" id="curveball-list"></div>
        </div>

        <!-- COLUMN 3: TIMER, SCORING & DEBRIEF -->
        <div class="arena-card" id="sec-scorecard">
            <div class="card-head">
                <span>⏱️ Round Scorecard</span>
                <span id="score-grade-pill" class="score-grade-badge">Score: --/100</span>
            </div>

            <!-- Stopwatch Block -->
            <div class="timer-block">
                <div class="timer-status-row">
                    <span id="timer-status-text" class="timer-status-badge">⚪ READY</span>
                    <span style="font-size:9.5px; color:var(--muted);">Target: &lt; 3:00 min</span>
                </div>
                <div class="timer-num" id="timer-display">00:00</div>
                <div class="timer-ctrls">
                    <button id="btn-timer-start" class="btn-t start" onclick="startTimer()">▶ Start</button>
                    <button id="btn-timer-pause" class="btn-t pause" onclick="pauseTimer()">⏸ Pause</button>
                    <button class="btn-t reset-timer" onclick="resetTimer()">↺ Reset</button>
                </div>
                <div class="timer-presets-row">
                    <button class="btn-t preset" onclick="addTimer(30)">+30s Preset</button>
                    <button class="btn-t preset" onclick="addTimer(60)">+1m Preset</button>
                </div>
            </div>

            <!-- 4-Point Rubrics -->
            <div class="rubric-row">
                <div class="rubric-lbl">
                    <span>1. Tone &amp; Frame Authority:</span>
                    <span id="score-tone-lbl">--</span>
                </div>
                <div class="rubric-grid">
                    <button class="rubric-pill red" onclick="setRubric('tone', 'Rushed / Timid', 'red', 5, this)">🔴 Timid (5p)</button>
                    <button class="rubric-pill amber" onclick="setRubric('tone', 'Conversational', 'amber', 15, this)">🟡 Casual (15p)</button>
                    <button class="rubric-pill green" onclick="setRubric('tone', 'Wall St Authority', 'green', 25, this)">🟢 Authority (25p)</button>
                </div>
            </div>

            <div class="rubric-row">
                <div class="rubric-lbl">
                    <span>2. Deflection Handling:</span>
                    <span id="score-deflect-lbl">--</span>
                </div>
                <div class="rubric-grid">
                    <button class="rubric-pill red" onclick="setRubric('deflect', 'Caved to Email', 'red', 5, this)">🔴 Caved (5p)</button>
                    <button class="rubric-pill amber" onclick="setRubric('deflect', 'Soft Push', 'amber', 15, this)">🟡 Soft (15p)</button>
                    <button class="rubric-pill green" onclick="setRubric('deflect', '45s Download Lock', 'green', 25, this)">🟢 45s Lock (25p)</button>
                </div>
            </div>

            <div class="rubric-row">
                <div class="rubric-lbl">
                    <span>3. Statement Extraction Ask:</span>
                    <span id="score-stmt-lbl">--</span>
                </div>
                <div class="rubric-grid">
                    <button class="rubric-pill red" onclick="setRubric('stmt', 'No Ask / Blank', 'red', 0, this)">🔴 No Ask (0p)</button>
                    <button class="rubric-pill amber" onclick="setRubric('stmt', 'Vague Email Ask', 'amber', 15, this)">🟡 Vague (15p)</button>
                    <button class="rubric-pill green" onclick="setRubric('stmt', 'Redaction + 4PM Lock', 'green', 25, this)">🟢 Redact+Lock (25p)</button>
                </div>
            </div>

            <div class="rubric-row">
                <div class="rubric-lbl">
                    <span>4. Voss Audit &amp; Loss Aversion:</span>
                    <span id="score-voss-lbl">--</span>
                </div>
                <div class="rubric-grid">
                    <button class="rubric-pill red" onclick="setRubric('voss', 'Pitching Speculative Debt', 'red', 5, this)">🔴 Debt Pitch (5p)</button>
                    <button class="rubric-pill amber" onclick="setRubric('voss', 'Standard Loan Pivot', 'amber', 15, this)">🟡 Loan Pitch (15p)</button>
                    <button class="rubric-pill green" onclick="setRubric('voss', 'Fee Audit / Zero Cost', 'green', 25, this)">🟢 Audit Lock (25p)</button>
                </div>
            </div>

            <!-- Notes & Quick Tags -->
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:2px;">
                <span style="font-size: 10px; font-weight: 700; color: var(--muted); text-transform: uppercase;">📝 Coaching Notes:</span>
                <span style="font-size: 9px; color: var(--muted);">Click tag to insert:</span>
            </div>
            <div class="quick-tags-row">
                <button class="btn-quick-tag" onclick="insertTag('Great 45s app download lock!')">+45s Lock</button>
                <button class="btn-quick-tag" onclick="insertTag('Offered account # redaction.')">+Redact Acct #</button>
                <button class="btn-quick-tag" onclick="insertTag('Don\'t apologize for calling.')">+No Apologies</button>
                <button class="btn-quick-tag" onclick="insertTag('Strong Wall St authority tone.')">+Authority</button>
                <button class="btn-quick-tag" onclick="insertTag('Pivoted to stopping daily debits.')">+Stop Debits</button>
            </div>
            <textarea id="sparring-notes" class="notes-input" placeholder="e.g. Great pivot to the 45s download. Don't rush through the opening greeting..."></textarea>

            <!-- Action Buttons -->
            <div class="action-btns-row">
                <button class="btn-debrief-copy" onclick="copySparringDebrief()">
                    📋 Copy &amp; Save Debrief
                </button>
                <button class="btn-reset-round" onclick="resetRoundAndScorecard()">
                    🔄 Reset Round
                </button>
            </div>

            <!-- Saved Rounds Session History -->
            <div class="rounds-history-box" id="rounds-history-box" style="display:none;">
                <div class="history-head">
                    <span>📜 Session Rounds History:</span>
                    <span id="rounds-count-tag" style="color:var(--navy);">0 Rounds</span>
                </div>
                <div class="history-list" id="rounds-history-list"></div>
            </div>
        </div>

    </div>

</div>

<div id="toast" class="toast">Debrief copied to clipboard</div>

<script>
const TELEMETRY_TOPIC = "ccs_michael_qin_telemetry_wh_2026";
const TELEMETRY_POST_URL = "https://ntfy.sh/" + TELEMETRY_TOPIC;
const SSE_URL = "https://ntfy.sh/" + TELEMETRY_TOPIC + "/sse";
const POLL_URL = "https://ntfy.sh/" + TELEMETRY_TOPIC + "/json?poll=1&since=all";
const SUPERVISOR_IPS = ['85.115.107.223', '74.209.76.220'];

const PERSONAS = {personas_json};
const CURVEBALLS = {curveballs_json};

let currentPersonaKey = "contractor";
let currentDiff = "easy";
let activeRubric = {{ tone: null, deflect: null, stmt: null, voss: null }};
let rubricPoints = {{ tone: 0, deflect: 0, stmt: 0, voss: 0 }};
let sessionRounds = [];

function jumpToSection(sectionId, btn) {{
    document.querySelectorAll('.m-tab-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    const el = document.getElementById(sectionId);
    if (el) {{
        el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}
}}

function selectPersona(key, btn) {{
    currentPersonaKey = key;
    document.querySelectorAll('.persona-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderPersonaDossier();
}}

function setDifficulty(diff, btn) {{
    currentDiff = diff;
    document.querySelectorAll('.diff-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderPersonaDossier();
}}

function speakLine(text) {{
    if ('speechSynthesis' in window) {{
        window.speechSynthesis.cancel();
        const utter = new SpeechSynthesisUtterance(text);
        utter.rate = 1.0;
        utter.pitch = 0.95;
        window.speechSynthesis.speak(utter);
    }} else {{
        showToast("Audio synthesis not supported on this browser.");
    }}
}}

async function broadcastPushback(curveId) {{
    const c = CURVEBALLS.find(item => item.id === curveId);
    if (!c) return;
    try {{
        await fetch(TELEMETRY_POST_URL, {{
            method: 'POST',
            body: JSON.stringify({{
                action: 'supervisor_curveball',
                title: "🥊 Opponent Pushback: " + c.q,
                curveId: c.id,
                spokenLine: c.spokenLine,
                rep: 'Supervisor (William)',
                isSupervisor: true,
                localTime: new Date().toLocaleTimeString()
            }})
        }});
        showToast("📡 Broadcasted pushback to Michael!");
    }} catch(e) {{
        showToast("Failed to broadcast pushback.");
    }}
}}

function renderPersonaDossier() {{
    const p = PERSONAS[currentPersonaKey] || PERSONAS["contractor"];
    const opener = p.openers[currentDiff] || p.openers.med;

    document.getElementById('dossier-content').innerHTML = `
        <div class="dossier-row">
            <span class="dossier-lbl">Identity:</span>
            <span class="dossier-val">${{p.name}}</span>
        </div>
        <div class="dossier-row">
            <span class="dossier-lbl">Company:</span>
            <span class="dossier-val">${{p.company}}</span>
        </div>
        <div class="dossier-row">
            <span class="dossier-lbl">Vertical / Location:</span>
            <span class="dossier-val">${{p.vertical}} • ${{p.location}}</span>
        </div>
        <div class="dossier-row">
            <span class="dossier-lbl">Monthly Revenue:</span>
            <span class="dossier-val" style="color:var(--success);">${{p.revenue}}</span>
        </div>
        <div class="dossier-row">
            <span class="dossier-lbl">Current Debt Stack:</span>
            <span class="dossier-val" style="color:var(--danger);">${{p.debtStack}}</span>
        </div>
        <div class="dossier-row" style="border:none;">
            <span class="dossier-lbl">Phone Mindset:</span>
            <span class="dossier-val" style="font-style:italic;">${{p.mood}}</span>
        </div>
        <div class="opener-box">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
                <span style="font-size:9.5px; font-weight:800; text-transform:uppercase; color:var(--navy);">🗣️ Your Spoken Opener (Say This):</span>
                <button class="btn-action-sm" onclick="speakLine(\`${{opener}}\`)">🔊 Speak</button>
            </div>
            <div style="font-weight:700; color:var(--navy);">${{opener}}</div>
        </div>
    `;

    document.getElementById('secret-intel-box').innerHTML = `
        <div style="font-weight:800; text-transform:uppercase; font-size:9.5px; margin-bottom:2px;">🤫 Hidden Reality (Only reveal if earned):</div>
        <div>${{p.secret}}</div>
    `;

    document.getElementById('win-trigger-box').innerHTML = `
        <div style="font-weight:800; text-transform:uppercase; font-size:9.5px; margin-bottom:2px;">🏆 Win Condition (When to yield 3 statements):</div>
        <div>${{p.winTrigger}}</div>
    `;
}}

function renderCurveballs() {{
    const container = document.getElementById('curveball-list');
    container.innerHTML = CURVEBALLS.map((c, idx) => `
        <div class="curve-card" id="card-${{c.id}}">
            <div class="curve-q-row" onclick="toggleCurveball('${{c.id}}')">
                <span class="curve-q">${{c.q}}</span>
                <span style="font-size:9px; color:var(--muted); font-family:var(--mono);">[Click to Expand]</span>
            </div>
            <div class="curve-cue">${{c.cue}}</div>
            <div class="curve-actions-row">
                <button class="btn-action-sm" onclick="speakLine(\`${{c.spokenLine}}\`)">🔊 Speak Aloud</button>
                <button class="btn-action-sm fire" onclick="broadcastPushback('${{c.id}}')">📡 Fire at Michael</button>
            </div>
            <div class="curve-detail">
                <div class="pill-win">✅ <strong>Winning Move:</strong> ${{c.win}}</div>
                <div class="pill-trap">❌ <strong>Rookie Trap:</strong> ${{c.trap}}</div>
            </div>
        </div>
    `).join('');
}}

function toggleCurveball(id) {{
    const targetCard = document.getElementById(`card-${{id}}`);
    if (!targetCard) return;
    const isCurrentlyActive = targetCard.classList.contains('active');
    
    document.querySelectorAll('.curve-card').forEach(c => c.classList.remove('active'));
    if (!isCurrentlyActive) {{
        targetCard.classList.add('active');
    }}
}}

/* =========================================================================
   TIMER LOGIC & STATUS
   ========================================================================= */
let timerSec = 0;
let timerInterval = null;
let timerStatus = 'ready'; // 'ready', 'running', 'paused'

function formatTime(s) {{
    const m = Math.floor(s / 60).toString().padStart(2, '0');
    const sec = (s % 60).toString().padStart(2, '0');
    return `${{m}}:${{sec}}`;
}}

function updateTimerDisplay() {{
    const display = document.getElementById('timer-display');
    const statusBadge = document.getElementById('timer-status-text');
    if (!display || !statusBadge) return;
    
    display.innerText = formatTime(timerSec);
    
    if (timerSec >= 180) {{
        display.classList.add('overtime');
        if (timerStatus === 'running') {{
            statusBadge.className = 'timer-status-badge overtime';
            statusBadge.innerText = '⚠️ OVERTIME';
        }}
    }} else {{
        display.classList.remove('overtime');
    }}
}}

function startTimer() {{
    if (timerInterval) return;
    timerStatus = 'running';
    const statusBadge = document.getElementById('timer-status-text');
    if (statusBadge) {{
        statusBadge.className = timerSec >= 180 ? 'timer-status-badge overtime' : 'timer-status-badge running';
        statusBadge.innerText = timerSec >= 180 ? '⚠️ OVERTIME' : '🟢 RUNNING';
    }}
    timerInterval = setInterval(() => {{
        timerSec++;
        updateTimerDisplay();
    }}, 1000);
}}

function pauseTimer() {{
    if (timerInterval) {{
        clearInterval(timerInterval);
        timerInterval = null;
    }}
    timerStatus = 'paused';
    const statusBadge = document.getElementById('timer-status-text');
    if (statusBadge) {{
        statusBadge.className = 'timer-status-badge paused';
        statusBadge.innerText = '⏸ PAUSED';
    }}
}}

function resetTimer() {{
    if (timerInterval) {{
        clearInterval(timerInterval);
        timerInterval = null;
    }}
    timerSec = 0;
    timerStatus = 'ready';
    updateTimerDisplay();
    const statusBadge = document.getElementById('timer-status-text');
    if (statusBadge) {{
        statusBadge.className = 'timer-status-badge';
        statusBadge.innerText = '⚪ READY';
    }}
}}

function addTimer(sec) {{
    timerSec += sec;
    updateTimerDisplay();
}}

/* =========================================================================
   SCORING RUBRIC & DEBRIEF
   ========================================================================= */
function setRubric(cat, val, color, pts, btn) {{
    activeRubric[cat] = val;
    rubricPoints[cat] = pts;
    const parent = btn.parentElement;
    parent.querySelectorAll('.rubric-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const lbl = document.getElementById(`score-${{cat}}-lbl`);
    if (lbl) {{
        lbl.innerText = `${{val}} (${{pts}}p)`;
        lbl.style.color = color === 'green' ? 'var(--success)' : (color === 'amber' ? 'var(--warning)' : 'var(--danger)');
    }}
    calculateCompositeScore();
}}

function calculateCompositeScore() {{
    let total = 0;
    let gradedCount = 0;
    for (let k in rubricPoints) {{
        if (activeRubric[k] !== null) {{
            total += rubricPoints[k];
            gradedCount++;
        }}
    }}
    
    const pill = document.getElementById('score-grade-pill');
    if (!pill) return {{ total, grade: '--' }};
    
    if (gradedCount === 0) {{
        pill.className = 'score-grade-badge';
        pill.innerText = 'Score: --/100';
        return {{ total: 0, grade: '--' }};
    }}
    
    let grade = 'Needs Work';
    let gradeClass = 'grade-f';
    if (total >= 90) {{
        grade = 'A+ (Elite)';
        gradeClass = 'grade-a';
    }} else if (total >= 75) {{
        grade = 'B (Proficient)';
        gradeClass = 'grade-b';
    }} else if (total >= 60) {{
        grade = 'C (Passing)';
        gradeClass = 'grade-c';
    }}
    
    pill.className = `score-grade-badge ${{gradeClass}}`;
    pill.innerText = `Score: ${{total}}/100 • ${{grade}}`;
    return {{ total, grade }};
}}

function insertTag(tag) {{
    const ta = document.getElementById('sparring-notes');
    if (!ta) return;
    if (ta.value.trim().length > 0) {{
        ta.value += ' ' + tag;
    }} else {{
        ta.value = tag;
    }}
}}

function resetRoundAndScorecard() {{
    resetTimer();
    activeRubric = {{ tone: null, deflect: null, stmt: null, voss: null }};
    rubricPoints = {{ tone: 0, deflect: 0, stmt: 0, voss: 0 }};
    
    document.querySelectorAll('.rubric-pill').forEach(b => b.classList.remove('active'));
    ['tone', 'deflect', 'stmt', 'voss'].forEach(cat => {{
        const lbl = document.getElementById(`score-${{cat}}-lbl`);
        if (lbl) {{
            lbl.innerText = '--';
            lbl.style.color = 'var(--muted)';
        }}
    }});
    
    const pill = document.getElementById('score-grade-pill');
    if (pill) {{
        pill.className = 'score-grade-badge';
        pill.innerText = 'Score: --/100';
    }}
    
    const notes = document.getElementById('sparring-notes');
    if (notes) notes.value = '';
    
    showToast("🔄 Round scorecard & timer reset!");
}}

function copySparringDebrief() {{
    const p = PERSONAS[currentPersonaKey] || PERSONAS['contractor'];
    const duration = formatTime(timerSec);
    const scoreObj = calculateCompositeScore();
    const total = scoreObj.total;
    const grade = scoreObj.grade;
    const notes = document.getElementById('sparring-notes').value || "Solid effort on the call. Remember to always execute the 45-second on-call statement download ask.";
    
    const roundNum = sessionRounds.length + 1;
    const roundEntry = {{
        num: roundNum,
        persona: `${{p.name}} (${{p.company}})`,
        diff: currentDiff.toUpperCase(),
        duration: duration,
        score: `${{total}}/100 (${{grade}})`,
        time: new Date().toLocaleTimeString([], {{ hour: '2-digit', minute: '2-digit' }})
    }};
    sessionRounds.unshift(roundEntry);
    renderRoundsHistory();
    
    const debrief = `🥊 SPARRING DEBRIEF — ROUND ${{roundNum}} | MICHAEL QIN (CREATIVE CAPITAL SOLUTIONS)
Date: ${{new Date().toLocaleDateString()}} | Call Duration: ${{duration}}
Persona Roleplayed: ${{p.name}} (${{p.company}} — ${{p.vertical}})
Resistance Level: ${{currentDiff.toUpperCase()}}

🎯 SCORECARD & GRADE:
• Total Score: ${{total}}/100 (${{grade}})
• 1. Tone & Frame Control: ${{activeRubric.tone || 'Not Graded'}}
• 2. Deflection Handling: ${{activeRubric.deflect || 'Not Graded'}}
• 3. Statement Extraction: ${{activeRubric.stmt || 'Not Graded'}}
• 4. Voss Loss Aversion Framing: ${{activeRubric.voss || 'Not Graded'}}

📝 SUPERVISOR COACHING FEEDBACK:
${{notes}}

⚡ KEY RECAPITULATION PRINCIPLE:
Never accept a passive brush-off ("just email me"). Trade rate transparency and account number redaction for the immediate 45-second statement PDF download while still on the line.`;

    navigator.clipboard.writeText(debrief).then(() => {{
        showToast(`📋 Round ${{roundNum}} debrief copied & saved!`);
    }}).catch(() => {{
        const ta = document.createElement('textarea');
        ta.value = debrief;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        showToast(`📋 Round ${{roundNum}} debrief copied & saved!`);
    }});
}}

function renderRoundsHistory() {{
    const box = document.getElementById('rounds-history-box');
    const list = document.getElementById('rounds-history-list');
    const countTag = document.getElementById('rounds-count-tag');
    if (!box || !list) return;
    
    if (sessionRounds.length === 0) {{
        box.style.display = 'none';
        return;
    }}
    box.style.display = 'flex';
    countTag.innerText = `${{sessionRounds.length}} Round${{sessionRounds.length > 1 ? 's' : ''}}`;
    
    list.innerHTML = sessionRounds.map(r => `
        <div class="history-item">
            <div>
                <strong>R${{r.num}}: ${{r.persona}}</strong> • <span>${{r.duration}}</span> • <span style="font-weight:700;color:var(--navy);">${{r.score}}</span>
            </div>
            <span style="color:var(--muted); font-size:9px;">${{r.time}}</span>
        </div>
    `).join('');
}}

function showToast(msg) {{
    const toast = document.getElementById('toast');
    toast.innerText = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2500);
}}

/* =========================================================================
   LIVE TELEMETRY STREAM LISTENER
   ========================================================================= */
function processEventData(data) {{
    if (!data || !data.action) return;
    if (data.url?.startsWith('file:')) return;

    const ip = data.ip || '';
    const dev = data.device || '';
    const loc = data.location || '';
    
    let personRole = 'guest';
    let personLabel = '📱 Guest Active';

    if (data.isSupervisor === true || ip === '85.115.107.223' || ip === '74.209.76.220' || data.rep?.includes('Supervisor') || data.rep?.includes('William') || dev?.includes('William')) {{
        personRole = 'supervisor';
        personLabel = '👑 You Active (Testing)';
    }} else if (ip === '69.203.0.85' || loc.includes('Staten Island') || (dev.includes('iPhone') && data.details?.screen === '428x751')) {{
        personRole = 'rep';
        personLabel = '🟢 Michael Qin Active (Staten Island)';
    }} else if (ip === '68.132.69.243' || loc.includes('Huntington') || (dev.includes('Android') && data.details?.screen === '378x656')) {{
        personRole = 'brother';
        personLabel = '👤 Salvatore Active (Huntington, NY)';
    }} else if (ip === '2600:387:15:2911::5' || loc.includes('White Plains') || (dev.includes('iPhone') && data.details?.screen === '393x754')) {{
        personRole = 'father';
        personLabel = '👨‍👦 David Qin Active (Father)';
    }}

    const liveDot = document.getElementById('live-dot');
    const statusText = document.getElementById('rep-status-text');
    liveDot.classList.add('online');

    if (personRole === 'supervisor') {{
        liveDot.style.background = '#3b82f6';
        statusText.innerText = personLabel + ' • Michael Qin Idle';
        return;
    }}

    if (personRole === 'rep') {{
        liveDot.style.background = '#22c55e';
    }} else if (personRole === 'brother') {{
        liveDot.style.background = '#0284c7';
    }} else if (personRole === 'father') {{
        liveDot.style.background = '#8b5cf6';
    }} else {{
        liveDot.style.background = '#64748b';
    }}

    statusText.innerText = personLabel;
    document.getElementById('mirror-time').innerText = data.localTime || new Date().toLocaleTimeString();
    document.getElementById('mirror-stage').innerText = data.title || data.action;

    if (data.details?.tone) {{
        document.getElementById('mirror-script').innerText = `Tone: ${{data.details.tone.toUpperCase()}} • Stage: ${{data.details.nextStage || 'Advanced'}}`;
    }} else if (data.details?.optionClicked) {{
        document.getElementById('mirror-script').innerText = `Selected Reaction: "${{data.details.optionClicked}}"`;
    }} else if (data.title) {{
        document.getElementById('mirror-script').innerText = data.title;
    }}
}}

async function fetchEvents() {{
    try {{
        const res = await fetch(POLL_URL + "&_t=" + Date.now());
        const text = await res.text();
        const lines = text.trim().split('\\n');
        lines.forEach(line => {{
            try {{
                const msg = JSON.parse(line);
                if (msg.message) processEventData(JSON.parse(msg.message));
            }} catch(e) {{}}
        }});
    }} catch(e) {{}}
}}

function connectSSE() {{
    const es = new EventSource(SSE_URL);
    es.onmessage = (e) => {{
        try {{
            const msg = JSON.parse(e.data);
            if (msg.message) processEventData(JSON.parse(msg.message));
        }} catch(err) {{}}
    }};
    es.onerror = () => {{
        setTimeout(connectSSE, 4000);
    }};
}}

window.addEventListener('DOMContentLoaded', () => {{
    selectPersona('contractor');
    renderCurveballs();
    fetchEvents();
    connectSSE();
    setInterval(fetchEvents, 6000);
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
    
    # 1. Rep Portal (index.html)
    portal_html_content = pipeline_sys.render_portal_html()
    portal_html_path = "index.html"
    with open(portal_html_path, "w", encoding="utf-8") as f:
        f.write(portal_html_content)
    print(f"[+] Successfully generated Rep portal: {portal_html_path}")

    # 2. William's Live Supervisor Cockpit (admin.html)
    admin_html_content = pipeline_sys.render_admin_html()
    admin_html_path = "admin.html"
    with open(admin_html_path, "w", encoding="utf-8") as f:
        f.write(admin_html_content)
    print(f"[+] Successfully generated Supervisor Cockpit: {admin_html_path}")

    # 3. William's Merchant Sparring Arena (opponent.html)
    opponent_html_content = pipeline_sys.render_opponent_html()
    opponent_html_path = "opponent.html"
    with open(opponent_html_path, "w", encoding="utf-8") as f:
        f.write(opponent_html_content)
    print(f"[+] Successfully generated Merchant Sparring Arena: {opponent_html_path}")

    # 4. Generate PDF
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
