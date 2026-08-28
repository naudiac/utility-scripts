#!/usr/bin/env python3
"""
Antigravity IDE - Michael Qin's Merchant Statement & Sales Mastery Flight Deck
Ultra-Clean, Minimalist, High-Contrast Edition.
Zero visual noise, zero glassy clutter. Instant legibility for Autodialers & Mobile.
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
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<title>{self.rep_name} | Sales Flight Deck</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
    :root {{
        --bg-base: #090a0f;
        --bg-surface: #12141a;
        --bg-card: #161922;
        --bg-input: #0d0f14;
        --border: #232733;
        --border-focus: #3b82f6;
        --text-pure: #ffffff;
        --text-primary: #e2e8f0;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --accent: #38bdf8;
        --success: #10b981;
        --danger: #f43f5e;
        --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        -webkit-tap-highlight-color: transparent;
    }}

    body {{
        background-color: var(--bg-base);
        color: var(--text-primary);
        font-family: var(--font-sans);
        font-size: 14px;
        line-height: 1.5;
        padding-bottom: env(safe-area-inset-bottom, 30px);
        min-height: 100vh;
    }}

    /* Minimalist Top Nav */
    header {{
        background: var(--bg-surface);
        border-bottom: 1px solid var(--border);
        padding: 12px 16px;
        position: sticky;
        top: 0;
        z-index: 50;
    }}
    .header-inner {{
        max-width: 960px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .header-brand {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .rep-name {{
        font-size: 14px;
        font-weight: 800;
        color: var(--text-pure);
        letter-spacing: -0.2px;
    }}
    .deck-label {{
        font-size: 11px;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        background: #1c202b;
        padding: 2px 6px;
        border-radius: 4px;
        border: 1px solid var(--border);
    }}

    .nav-tabs {{
        max-width: 960px;
        margin: 0 auto;
        display: flex;
        gap: 4px;
        padding: 10px 16px 0;
        overflow-x: auto;
        scrollbar-width: none;
    }}
    .nav-tabs::-webkit-scrollbar {{ display: none; }}
    .tab-item {{
        background: none;
        border: none;
        color: var(--text-secondary);
        font-size: 13px;
        font-weight: 600;
        padding: 8px 14px;
        border-radius: 6px;
        cursor: pointer;
        white-space: nowrap;
        transition: all 0.1s ease;
    }}
    .tab-item:hover {{ color: var(--text-pure); }}
    .tab-item.active {{
        background: var(--bg-surface);
        color: var(--accent);
        border: 1px solid var(--border);
    }}

    /* Main Content */
    main {{
        max-width: 960px;
        margin: 16px auto;
        padding: 0 16px;
    }}

    .tab-pane {{ display: none; }}
    .tab-pane.active {{ display: block; }}

    /* =========================================================================
       ULTRA-CLEAN AUTODIALER HUD
       ========================================================================= */
    .hud-box {{
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
    }}
    @media (max-width: 600px) {{
        .hud-box {{ padding: 14px; }}
    }}

    .hud-meta {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        font-family: var(--font-mono);
        font-size: 11px;
        color: var(--text-muted);
    }}
    .hud-phase {{
        color: var(--accent);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .script-display {{
        background: var(--bg-input);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 16px 18px;
        margin-bottom: 16px;
    }}
    .script-goal {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: var(--text-secondary);
        margin-bottom: 6px;
    }}
    .script-text {{
        font-size: 18px;
        font-weight: 600;
        color: var(--text-pure);
        line-height: 1.45;
        white-space: pre-wrap;
    }}
    @media (max-width: 600px) {{
        .script-text {{ font-size: 15px; line-height: 1.4; }}
    }}
    .script-note {{
        margin-top: 10px;
        font-size: 11.5px;
        color: var(--text-muted);
        border-top: 1px solid var(--border);
        padding-top: 8px;
    }}

    .buttons-grid {{
        display: grid;
        grid-template-columns: 1fr;
        gap: 8px;
        margin-bottom: 16px;
    }}
    @media (min-width: 640px) {{
        .buttons-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}

    .btn-action {{
        background: var(--bg-card);
        border: 1px solid var(--border);
        color: var(--text-primary);
        padding: 12px 14px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
        text-align: left;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: background 0.1s, border-color 0.1s;
    }}
    .btn-action:hover {{
        background: #1c202c;
        border-color: #3b4255;
    }}
    .btn-action:active {{
        background: #242938;
    }}
    .btn-action.opt-pos {{
        border-left: 3px solid var(--success);
    }}
    .btn-action.opt-neg {{
        border-left: 3px solid var(--danger);
    }}

    .key-badge {{
        background: #0d0f14;
        border: 1px solid var(--border);
        color: var(--accent);
        font-family: var(--font-mono);
        font-size: 11px;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
        margin-left: 8px;
        flex-shrink: 0;
    }}

    .hud-controls {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 12px;
        border-top: 1px solid var(--border);
    }}
    .btn-ctrl {{
        background: var(--bg-card);
        border: 1px solid var(--border);
        color: var(--text-secondary);
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
    }}
    .btn-ctrl:hover {{ color: var(--text-pure); border-color: var(--text-secondary); }}

    /* =========================================================================
       CLEAN CARDS & UTILITIES
       ========================================================================= */
    .card {{
        background: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 14px;
    }}
    .card-title {{
        font-size: 14px;
        font-weight: 700;
        color: var(--text-pure);
        margin-bottom: 10px;
    }}

    .bank-chips {{
        display: flex;
        gap: 6px;
        margin-bottom: 12px;
        overflow-x: auto;
    }}
    .bank-chip {{
        background: var(--bg-card);
        border: 1px solid var(--border);
        color: var(--text-secondary);
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
    }}
    .bank-chip.active {{
        background: #1e293b;
        color: var(--accent);
        border-color: var(--border-focus);
    }}

    .copy-block {{
        background: var(--bg-input);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 12px 14px;
        position: relative;
        margin-top: 8px;
    }}
    .copy-content {{
        font-size: 13px;
        color: var(--text-primary);
        line-height: 1.5;
        white-space: pre-wrap;
    }}
    .btn-copy-float {{
        position: absolute;
        top: 8px;
        right: 8px;
        background: var(--bg-card);
        border: 1px solid var(--border);
        color: var(--text-secondary);
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 4px;
        cursor: pointer;
    }}
    .btn-copy-float:hover {{ color: var(--text-pure); }}

    /* Calculator */
    .calc-row {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 10px;
        margin-bottom: 12px;
    }}
    .calc-field label {{
        display: block;
        font-size: 11px;
        color: var(--text-muted);
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 4px;
    }}
    .calc-field input {{
        width: 100%;
        background: var(--bg-input);
        border: 1px solid var(--border);
        color: var(--text-pure);
        padding: 8px 10px;
        border-radius: 6px;
        font-family: var(--font-mono);
        font-size: 14px;
    }}
    .calc-field input:focus {{ outline: none; border-color: var(--border-focus); }}

    .calc-summary {{
        background: var(--bg-input);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 12px;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        text-align: center;
    }}
    .calc-val {{
        font-size: 18px;
        font-weight: 800;
        font-family: var(--font-mono);
        color: var(--accent);
    }}
    .calc-lbl {{
        font-size: 10px;
        color: var(--text-muted);
        text-transform: uppercase;
        margin-top: 2px;
    }}

    /* Toast */
    .toast {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--text-pure);
        color: #000;
        font-weight: 700;
        font-size: 12px;
        padding: 6px 14px;
        border-radius: 6px;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.15s ease;
        z-index: 1000;
    }}
    .toast.show {{ opacity: 1; }}

    @media print {{
        header, .nav-tabs, .btn-ctrl, .btn-copy-float {{ display: none !important; }}
        body {{ background: #fff; color: #000; }}
        .hud-box, .card {{ border: 1px solid #ccc; background: #fff; }}
        .script-display, .copy-block {{ background: #fafafa; border: 1px solid #ddd; }}
        .script-text, .copy-content {{ color: #000; }}
    }}
</style>
</head>
<body>

<header>
    <div class="header-inner">
        <div class="header-brand">
            <span class="rep-name">Michael Qin</span>
            <span class="deck-label">Merchant Closer Deck</span>
        </div>
        <div style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">
            Hotkeys: 1-6 | Space: Copy | R: Reset
        </div>
    </div>
</header>

<div class="nav-tabs">
    <button class="tab-item active" onclick="switchTab('tab-hud')">Dialer Copilot</button>
    <button class="tab-item" onclick="switchTab('tab-statement')">Statement Walkthrough</button>
    <button class="tab-item" onclick="switchTab('tab-calc')">Savings Calculator</button>
    <button class="tab-item" onclick="switchTab('tab-objections')">Pushbacks</button>
    <button class="tab-item" onclick="switchTab('tab-cadence')">Follow-Up SMS</button>
    <button class="tab-item" onclick="switchTab('tab-pipeline')">Pipeline Stages</button>
</div>

<main>

    <!-- TAB 1: DIALER COPILOT -->
    <div id="tab-hud" class="tab-pane active">
        <div class="hud-box">
            <div class="hud-meta">
                <span class="hud-phase" id="hud-phase">Stage: Opening (0-5s)</span>
                <span id="hud-step-num">Step 1 of 4</span>
            </div>

            <div class="script-display">
                <div class="script-goal" id="hud-goal">Goal: Permission & Status Anchor</div>
                <div class="script-text" id="hud-verbatim">"Hey [Name], I will be brief. I know I am calling out of the blue.

I work on the commercial capital placement side, and the reason for the call is simple: we are working with merchants in your industry right now to lower their daily/weekly debits and clean up expensive debt."</div>
                <div class="script-note" id="hud-note">Speak calmly, like an institutional auditor reviewing financials.</div>
            </div>

            <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 8px;">
                Merchant Response (Click or press number):
            </div>

            <div class="buttons-grid" id="hud-buttons">
                <!-- Dynamically populated -->
            </div>

            <div class="hud-controls">
                <button class="btn-ctrl" onclick="goBack()" id="btn-back" style="display:none;">⬅ Back</button>
                <div style="display: flex; gap: 6px; margin-left: auto;">
                    <button class="btn-ctrl" onclick="copyText(document.getElementById('hud-verbatim').innerText)">📋 Copy Line (Space)</button>
                    <button class="btn-ctrl" onclick="resetFlow()">🔄 Reset (R)</button>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 2: STATEMENT WALKTHROUGH -->
    <div id="tab-statement" class="tab-pane">
        <div class="card">
            <div class="card-title">45-Second On-Call Statement Walkthrough</div>
            <p style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 12px;">
                Keep the merchant on the line and talk them through exporting their 3 PDF statements immediately.
            </p>

            <div class="copy-block">
                <div class="copy-content">"John, are you in front of your computer or looking at your phone right now?

Stay on with me for literally 45 seconds while you export your last 3 monthly statements as PDFs. I will confirm receipt while we're on the line so this isn't hanging over your head tonight.

Which bank do you use for operations—Chase, Bank of America, or Wells?"</div>
                <button class="btn-copy-float" onclick="copySnippet(this)">Copy</button>
            </div>

            <div style="margin: 14px 0 6px; font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">
                Select Bank for Step-by-Step Instructions:
            </div>
            <div class="bank-chips">
                <button class="bank-chip active" onclick="pickBank('chase')">Chase</button>
                <button class="bank-chip" onclick="pickBank('boa')">Bank of America</button>
                <button class="bank-chip" onclick="pickBank('wells')">Wells Fargo</button>
                <button class="bank-chip" onclick="pickBank('universal')">Universal App</button>
            </div>

            <div class="copy-block">
                <div class="copy-content" id="bank-instructions">1. Tell merchant: "Log into Chase.com and click your business checking account."
2. "Click 'Statements & Documents' right below the balance."
3. "Download the last 3 monthly PDFs and forward directly to my email."</div>
                <button class="btn-copy-float" onclick="copySnippet(this)">Copy</button>
            </div>
        </div>

        <div class="card">
            <div class="card-title">The "Loss Aversion" Reframe (Chris Voss)</div>
            <div class="copy-block">
                <div class="copy-content">"John, I don't want you wasting your evening downloading statements if this doesn't put money back into your business.

If our review shows your current setup is already optimal, I will tell you to keep it. But if you're leaking $2,500 a month in excessive factor fees or daily debits, wouldn't you want to know by tomorrow morning?

Let me send you a secure request link right now. What's the best email?"</div>
                <button class="btn-copy-float" onclick="copySnippet(this)">Copy</button>
            </div>
        </div>
    </div>

    <!-- TAB 3: SAVINGS CALCULATOR -->
    <div id="tab-calc" class="tab-pane">
        <div class="card">
            <div class="card-title">Live Merchant Cash Flow & Debt Savings Calculator</div>
            <div class="calc-row">
                <div class="calc-field">
                    <label>Monthly Revenue ($)</label>
                    <input type="number" id="calc-rev" value="120000" step="5000" oninput="runCalc()">
                </div>
                <div class="calc-field">
                    <label>Current Debits ($/Month)</label>
                    <input type="number" id="calc-debit" value="18000" step="1000" oninput="runCalc()">
                </div>
                <div class="calc-field">
                    <label>Proposed New Payment ($/Mo)</label>
                    <input type="number" id="calc-new-pay" value="7500" step="500" oninput="runCalc()">
                </div>
                <div class="calc-field">
                    <label>New Capital ($)</label>
                    <input type="number" id="calc-advance" value="150000" step="10000" oninput="runCalc()">
                </div>
            </div>

            <div class="calc-summary">
                <div>
                    <div class="calc-val" id="res-monthly" style="color: var(--success);">+$10,500</div>
                    <div class="calc-lbl">Monthly Cash Freed</div>
                </div>
                <div>
                    <div class="calc-val" id="res-annual">$126,000</div>
                    <div class="calc-lbl">Annual Savings</div>
                </div>
                <div>
                    <div class="calc-val" id="res-capital">$150,000</div>
                    <div class="calc-lbl">Liquidity Unlocked</div>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 4: OBJECTIONS -->
    <div id="tab-objections" class="tab-pane">
        <div class="card">
            <div class="card-title">Pushback & Objection Matrix</div>
            <div id="objections-list"></div>
        </div>
    </div>

    <!-- TAB 5: CADENCE -->
    <div id="tab-cadence" class="tab-pane">
        <div class="card">
            <div class="card-title">10-Day Multi-Touch SMS & Email Cadence</div>
            
            <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-top: 10px;">Day 1: Instant Post-Call SMS</div>
            <div class="copy-block">
                <div class="copy-content">"Hi [Name], Michael Qin here from Capital Advisory. Great speaking with you briefly. To run your debt consolidation and statement audit, just email your last 3 monthly business bank PDFs to michael@capitaladvisory.com. Once received, I will have your approved numbers back within 24 hours."</div>
                <button class="btn-copy-float" onclick="copySnippet(this)">Copy</button>
            </div>

            <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-top: 14px;">Day 3: Midday Leakage Check-In</div>
            <div class="copy-block">
                <div class="copy-content">Subject: Quick question regarding [Business Name] cash flow

Hi [Name],

Following up on our conversation regarding restructuring your operating debt. 

Our underwriting desk locks weekly merchant placement tiers every Thursday at 4 PM. If you shoot over your 3 bank statements today, I can have your term sheet approved before the weekend.

Let me know if you need help pulling the PDFs from Chase/BoA.

Best,
Michael Qin</div>
                <button class="btn-copy-float" onclick="copySnippet(this)">Copy</button>
            </div>

            <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-top: 14px;">Day 8: Permission-to-Close Breakup</div>
            <div class="copy-block">
                <div class="copy-content">Subject: Closing your file / [Business Name]

Hi [Name],

I assume restructuring your working capital isn't a priority right now, so I will close out your file.

If daily debits ever start squeezing your cash flow down the road, feel free to reach out anytime.

Best regards,
Michael Qin</div>
                <button class="btn-copy-float" onclick="copySnippet(this)">Copy</button>
            </div>
        </div>
    </div>

    <!-- TAB 6: PIPELINE STAGES -->
    <div id="tab-pipeline" class="tab-pane">
        <div class="card">
            <div class="card-title">The 7-Stage Sales Architecture</div>
            <div id="pipeline-list"></div>
        </div>
    </div>

</main>

<div id="toast" class="toast">Copied to clipboard</div>

<script>
const STAGES = {stages_json};
const OBJECTIONS = {objections_json};

/* =========================================================================
   CLEAN COPILOT ENGINE
   ========================================================================= */
const CALL_FLOW = {{
    "root": {{
        phase: "Stage: Opening (0-5s)",
        goal: "Goal: Permission & Status Anchor",
        verbatim: `"Hey [Name], I will be brief. I know I am calling out of the blue.

I work on the commercial capital placement side, and the reason for the call is simple: we are working with merchants in your industry right now to lower their daily/weekly debits and clean up expensive debt."`,
        note: "Speak calmly, like an institutional auditor reviewing financials.",
        options: [
            {{ text: `"Who is this / What company?"`, key: "1", next: "who_is_this", type: "pos" }},
            {{ text: `[Listened / Silence / "Okay..."]`, key: "2", next: "aligned_hook", type: "pos" }},
            {{ text: `"We don't need money / We're all set"`, key: "3", next: "dont_need_money", type: "neg" }},
            {{ text: `"Just email me info / I'm busy"`, key: "4", next: "just_email_me", type: "neg" }},
            {{ text: `"What are your rates / factor rates?"`, key: "5", next: "what_rates", type: "pos" }},
            {{ text: `"I don't send bank statements"`, key: "6", next: "statement_pushback", type: "neg" }}
        ]
    }},

    "who_is_this": {{
        phase: "Identity & Disarm (6-15s)",
        goal: "Goal: Establish Credibility & Results",
        verbatim: `"I'm Michael Qin with Capital Placement Advisory. We specialize in commercial working capital and restructuring high-cost merchant debt.

The reason I reached out directly is because we just restructured financing for a business in your exact space, cutting their monthly debt payment by 40%.

I'm not asking for your business today—I just want to run a free debt audit against your last 3 statements to show you what you could save.

Where should I email the benchmark sheet?"`,
        note: "Give proof of results and close for the destination email address.",
        options: [
            {{ text: `"Sure, send to [Email]"`, key: "1", next: "win_extract_statements", type: "pos" }},
            {{ text: `"We don't need any funding"`, key: "2", next: "dont_need_money", type: "neg" }},
            {{ text: `"What are your rates?"`, key: "3", next: "what_rates", type: "pos" }}
        ]
    }},

    "aligned_hook": {{
        phase: "Core Value (16-23s)",
        goal: "Goal: Eliminate Risk with Success-Only Model",
        verbatim: `"I'm not asking you to commit to anything today. My model is simple: I only get paid if we actually deliver terms and lower payments that beat what you currently have.

If you shoot over your last 3 monthly statements, I will run a side-by-side comparison within 24 hours showing your exact monthly cash flow savings.

What is the best email to send that breakdown to?"`,
        note: "Emphasize zero downside risk for the merchant.",
        options: [
            {{ text: `Merchant gave email address`, key: "1", next: "win_extract_statements", type: "pos" }},
            {{ text: `"We already have a lender"`, key: "2", next: "dont_need_money", type: "neg" }},
            {{ text: `"I don't have time right now"`, key: "3", next: "just_email_me", type: "neg" }}
        ]
    }},

    "dont_need_money": {{
        phase: "Objection Pivot: No Funding Needed",
        goal: "Goal: Reframe to Expense Reduction",
        verbatim: `"Completely understand, and I'm glad business is healthy. I'm actually not calling to sell you new debt.

Most successful merchants we work with aren't looking to borrow—they just want to stop getting squeezed by high fees and daily debits on existing positions.

If our audit shows your current setup is optimal, at least you keep your lenders honest. If we find \$2,000 a month in leakage, you keep the cash.

What's the best email for that 1-page check?"`,
        note: "Frame as expense reduction and cash recovery.",
        options: [
            {{ text: `"Fair enough, send to [Email]"`, key: "1", next: "win_extract_statements", type: "pos" }},
            {{ text: `"Not interested / Hard No"`, key: "2", next: "hard_no", type: "neg" }}
        ]
    }},

    "just_email_me": {{
        phase: "Objection Pivot: 'Send Info' Deflection",
        goal: "Goal: Execute 45-Second On-Call Download",
        verbatim: `"Happy to do that. Rather than sending a generic PDF deck that will sit in your spam, are you in front of your computer or on your phone right now?

Stay with me for 45 seconds while you click 'Download Statements' on your bank portal. I will confirm receipt on the line so you don't have this on your to-do list tonight.

Which bank do you use—Chase, BoA, or Wells?"`,
        note: "Do NOT accept passive brush-offs without asking for the live download.",
        options: [
            {{ text: `"I'm on my computer now / Exporting"`, key: "1", next: "win_on_call_download", type: "pos" }},
            {{ text: `"I'm driving / really busy"`, key: "2", next: "send_sms_link", type: "neg" }}
        ]
    }},

    "what_rates": {{
        phase: "Pricing Hook & Trade-Off",
        goal: "Goal: Trade Rate Clarity for Statements",
        verbatim: `"Rates depend entirely on monthly revenue and cash flow, but we are consistently placing capital at single-digit to low-spread terms that cut daily debits in half.

To give you an exact rate card rather than a misleading ballpark, shoot over your last 3 monthly statements and I'll deliver your exact terms in 3 hours.

What address should I send the doc request to?"`,
        note: "Never quote a rigid number without requiring statements first.",
        options: [
            {{ text: `Merchant agreed / gave email`, key: "1", next: "win_extract_statements", type: "pos" }},
            {{ text: `"Why do you need statements?"`, key: "2", next: "statement_pushback", type: "neg" }}
        ]
    }},

    "statement_pushback": {{
        phase: "Statement Hesitation",
        goal: "Goal: Dissolve Security Fear",
        verbatim: `"Totally understand the caution—your financials are sensitive. 

We do not shop your file to 20 brokers. We do a direct, in-house preliminary audit to confirm your true monthly volume so we can negotiate institutional terms on your behalf.

You can redact your account numbers if you prefer. What is the best email to send the secure link to?"`,
        note: "Offer account number redaction to instantly eliminate security friction.",
        options: [
            {{ text: `"Okay, send the email"`, key: "1", next: "win_extract_statements", type: "pos" }}
        ]
    }},

    "win_extract_statements": {{
        phase: "Win: Email Captured",
        goal: "Goal: Lock in Statements on the Call",
        verbatim: `"Got that down. I just sent the direct link to [Email].

While I have you for 30 seconds, are you able to click 'Forward' on your last 3 monthly PDFs right now so I can prioritize your file for tomorrow morning's underwriting committee?"`,
        note: "Strike while you have them on the line.",
        options: [
            {{ text: `"Doing it right now on the phone"`, key: "1", next: "win_on_call_download", type: "pos" }},
            {{ text: `"I'll do it by 4 PM today"`, key: "2", next: "win_deadline_set", type: "pos" }}
        ]
    }},

    "win_on_call_download": {{
        phase: "🏆 Complete Win: Statements Received",
        goal: "Goal: Confirm & Promise 24-Hour Term Sheet",
        verbatim: `"Boom, I see the 3 PDFs in my inbox right now.

I will personally run the cash flow model and have your benchmark savings breakdown in your inbox by tomorrow morning.

Thank you John, speak tomorrow!"`,
        note: "Confirm receipt and close the call immediately.",
        options: [
            {{ text: `Reset for Next Call (R)`, key: "1", next: "root", type: "pos" }}
        ]
    }},

    "win_deadline_set": {{
        phase: "⏰ Win: 4 PM Deadline Set",
        goal: "Goal: Set Firm Calendar Commitment",
        verbatim: `"Perfect John. I will hold a spot with our credit desk for 4 PM today. As soon as you email those 3 PDFs, I will get you to the front of the queue.

Look out for my text message with the direct upload email. Have a great day!"`,
        note: "Send Day 1 SMS within 60 seconds.",
        options: [
            {{ text: `Reset for Next Call (R)`, key: "1", next: "root", type: "pos" }}
        ]
    }},

    "send_sms_link": {{
        phase: "Mobile Fallback: 1-Click SMS",
        goal: "Goal: Send Direct SMS to Mobile",
        verbatim: `"Understood John, drive safe. I am texting my direct email and a 2-click statement link to this mobile number right now.

Reply with the 3 PDFs when you're back at your desk and I'll jump on it immediately."`,
        note: "Send SMS immediately while your voice is fresh.",
        options: [
            {{ text: `Reset for Next Call (R)`, key: "1", next: "root", type: "pos" }}
        ]
    }},

    "hard_no": {{
        phase: "Graceful Exit",
        goal: "Goal: Leave Professional Door Open",
        verbatim: `"Totally respect that John. I'll leave you to your day. If cash flow ever gets tight down the road, you have my number. Have a great week!"`,
        note: "Never show frustration. Leave the door wide open.",
        options: [
            {{ text: `Reset for Next Call (R)`, key: "1", next: "root", type: "pos" }}
        ]
    }}
}};

let historyStack = ["root"];

function renderCurrentNode() {{
    const key = historyStack[historyStack.length - 1];
    const node = CALL_FLOW[key] || CALL_FLOW["root"];

    document.getElementById('hud-phase').innerText = node.phase;
    document.getElementById('hud-goal').innerText = node.goal;
    document.getElementById('hud-verbatim').innerText = node.verbatim;
    document.getElementById('hud-note').innerText = node.note;
    document.getElementById('hud-step-num').innerText = `Step ${{historyStack.length}}`;

    const btnGrid = document.getElementById('hud-buttons');
    btnGrid.innerHTML = node.options.map(opt => `
        <button class="btn-action ${{opt.type === 'pos' ? 'opt-pos' : 'opt-neg'}}" onclick="pickNext('${{opt.next}}')">
            <span>${{opt.text}}</span>
            <span class="key-badge">[${{opt.key}}]</span>
        </button>
    `).join('');

    document.getElementById('btn-back').style.display = historyStack.length > 1 ? 'inline-block' : 'none';
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
        copyText(document.getElementById('hud-verbatim').innerText);
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

function pickBank(bankKey) {{
    document.querySelectorAll('.bank-chip').forEach(el => el.classList.remove('active'));
    event.target.classList.add('active');
    document.getElementById('bank-instructions').innerText = BANK_SCRIPTS[bankKey];
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
}}

function copyText(text) {{
    navigator.clipboard.writeText(text.trim()).then(() => {{
        const toast = document.getElementById('toast');
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 1500);
    }});
}}

function copySnippet(btn) {{
    const content = btn.parentElement.querySelector('.copy-content').innerText;
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
            <div style="font-size: 13px; font-weight: 700; color: var(--danger); margin-bottom: 4px;">⚠️ "${{o.objection}}"</div>
            <div class="copy-block">
                <div class="copy-content">"${{o.rebuttal}}"</div>
                <button class="btn-copy-float" onclick="copySnippet(this)">Copy</button>
            </div>
            <div style="font-size: 11.5px; color: var(--text-muted); margin-top: 4px;"><strong>Principle:</strong> ${{o.principle}}</div>
        </div>
    `).join('');
}}

function renderPipeline() {{
    const container = document.getElementById('pipeline-list');
    container.innerHTML = STAGES.map(s => `
        <div style="margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 12px;">
            <div style="font-size: 13.5px; font-weight: 700; color: var(--text-pure); margin-bottom: 4px;">Stage ${{s.number}}: ${{s.title}}</div>
            <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 8px;"><strong>Goal:</strong> ${{s.objective}}</div>
            <div style="font-size: 11.5px; color: var(--text-muted); margin-bottom: 6px;"><strong>Key Actions:</strong></div>
            <ul style="padding-left: 16px; font-size: 12px; color: var(--text-secondary);">
                ${{s.actions.map(a => `<li>${{a}}</li>`).join('')}}
            </ul>
        </div>
    `).join('');
}}

window.addEventListener('DOMContentLoaded', () => {{
    renderCurrentNode();
    renderObjections();
    renderPipeline();
    runCalc();
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
    print(f"[+] Successfully generated ultra-clean portal: {portal_html_path}")

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
