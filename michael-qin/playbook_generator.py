#!/usr/bin/env python3
"""
Antigravity IDE - Entity Pitch & Playbook Generator Engine
Generates plain-English, high-conversion sales playbooks and exports to HTML/PDF.
Includes optional Google Drive automated upload support.
"""

import sys
import json
from dataclasses import dataclass, field
from typing import List, Dict

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False


@dataclass
class ObjectionHandler:
    objection: str
    response: str


@dataclass
class PitchPlaybook:
    entity_title: str
    industry: str
    core_problem: str
    pitches: List[Dict[str, str]] = field(default_factory=list)
    script_30s: str = ""
    pacing_breakdown: List[Dict[str, str]] = field(default_factory=list)
    objections: List[ObjectionHandler] = field(default_factory=list)
    rules: List[str] = field(default_factory=list)

    def render_html(self) -> str:
        pitch_cards = "".join([
            f"""<div class="card pitch-card">
                <div class="card-tag">{p['title']}</div>
                <div class="quote-body">"{p['script']}"</div>
            </div>""" for p in self.pitches
        ])

        pacing_rows = "".join([
            f"""<tr>
                <td><strong>{row['time']}</strong></td>
                <td>{row['phase']}</td>
                <td>{row['goal']}</td>
            </tr>""" for row in self.pacing_breakdown
        ])

        objection_cards = "".join([
            f"""<div class="obj-card">
                <div class="obj-label">Objection: "{o.objection}"</div>
                <div class="obj-text">"{o.response}"</div>
            </div>""" for o in self.objections
        ])

        rules_list = "".join([f"<li>{r}</li>" for r in self.rules])

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @page {{ size: letter; margin: 16mm; background-color: #f8fafc; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #0f172a; line-height: 1.5; font-size: 9.5pt; margin: 0; }}
    .header {{ background: #0f172a; color: white; padding: 20px 24px; border-radius: 6px; margin-bottom: 20px; }}
    .tag {{ color: #38bdf8; font-size: 8pt; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }}
    h1 {{ margin: 4px 0 6px 0; font-size: 18pt; }}
    .sub {{ color: #94a3b8; font-size: 9pt; margin: 0; }}
    h2 {{ font-size: 12pt; border-left: 4px solid #0284c7; padding-left: 8px; margin: 20px 0 10px 0; color: #0f172a; }}
    .card {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 16px; margin-bottom: 12px; page-break-inside: avoid; }}
    .pitch-card {{ border-left: 4px solid #0284c7; }}
    .card-tag {{ color: #0369a1; font-weight: 700; font-size: 8.5pt; text-transform: uppercase; margin-bottom: 4px; }}
    .quote-body {{ font-size: 9.5pt; color: #0f172a; }}
    table {{ width: 100%; border-collapse: collapse; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; margin: 10px 0; }}
    th {{ background: #0f172a; color: white; text-align: left; padding: 8px 10px; font-size: 8.5pt; }}
    td {{ padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 8.5pt; }}
    .obj-card {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 14px; margin-bottom: 10px; page-break-inside: avoid; }}
    .obj-label {{ color: #b91c1c; font-weight: 700; margin-bottom: 4px; }}
    .obj-text {{ background: #f0fdf4; border-left: 3px solid #16a34a; padding: 8px 10px; color: #14532d; border-radius: 0 4px 4px 0; }}
    ul {{ margin: 0; padding-left: 18px; }}
    li {{ margin-bottom: 4px; }}
</style>
</head>
<body>
    <div class="header">
        <div class="tag">{self.industry} Strategic Playbook</div>
        <h1>{self.entity_title}</h1>
        <p class="sub">Refined communication structure, objection handlers, and frictionless conversion assets.</p>
    </div>

    <h2>1. Pitch Angle Frameworks</h2>
    {pitch_cards}

    <h2>2. 30-Second Verbatim Cold Call</h2>
    <div class="card" style="border-left: 4px solid #0f172a;">
        <div class="quote-body" style="font-weight: 500;">
            {self.script_30s.replace(chr(10), '<br>')}
        </div>
    </div>

    <table>
        <thead>
            <tr><th style="width: 20%;">Timeline</th><th style="width: 30%;">Phase</th><th style="width: 50%;">Strategic Goal</th></tr>
        </thead>
        <tbody>
            {pacing_rows}
        </tbody>
    </table>

    <h2>3. Core Pushback & Objection Handling</h2>
    {objection_cards}

    <h2>4. Execution & Operating Rules</h2>
    <div class="card">
        <ul>
            {rules_list}
        </ul>
    </div>
</body>
</html>"""

    def export(self, filename_base: str = "playbook_output"):
        import os
        import subprocess
        import shutil

        html_out = f"{filename_base}.html"
        pdf_out = f"{filename_base}.pdf"

        html_content = self.render_html()
        with open(html_out, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[+] Rendered HTML: {html_out}")

        if WEASYPRINT_AVAILABLE:
            HTML(html_out).write_pdf(pdf_out)
            print(f"[+] Rendered PDF (WeasyPrint): {pdf_out}")
        else:
            abs_html = os.path.abspath(html_out)
            abs_pdf = os.path.abspath(pdf_out)
            edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            browser_bin = None

            if os.path.exists(edge_path):
                browser_bin = edge_path
            elif os.path.exists(chrome_path):
                browser_bin = chrome_path
            else:
                browser_bin = shutil.which("msedge") or shutil.which("chrome")

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
                    print(f"[+] Rendered PDF (Headless Browser): {pdf_out}")
                except Exception as e:
                    print(f"[-] PDF render error: {e}")
            else:
                print("[!] WeasyPrint or compatible browser not found for PDF export.")


# ---------------------------------------------------------------------------
# Google Drive Uploader Module (Optional Integration)
# ---------------------------------------------------------------------------
def upload_to_drive(local_file_path: str, drive_folder_id: str = None):
    """
    Automates uploading the generated PDF to Google Drive via service account
    or OAuth2 credentials. Requires: pip install google-api-python-client google-auth
    """
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2 import service_account

        # Provide path to your local credentials JSON file
        SERVICE_ACCOUNT_FILE = 'credentials.json'
        SCOPES = ['https://www.googleapis.com/auth/drive.file']

        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {'name': local_file_path.split('/')[-1]}
        if drive_folder_id:
            file_metadata['parents'] = [drive_folder_id]

        media = MediaFileUpload(local_file_path, mimetype='application/pdf')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"[+] Successfully uploaded to Google Drive. File ID: {file.get('id')}")
    except Exception as e:
        print(f"[-] Drive Upload Note: Configure credentials.json to enable auto-upload. Error: {e}")


# ---------------------------------------------------------------------------
# Factory: Pre-Loaded Instance
# ---------------------------------------------------------------------------
def build_loan_playbook() -> PitchPlaybook:
    return PitchPlaybook(
        entity_title="Loan Origination Cold Call & Pitch Playbook",
        industry="Capital Markets & Debt Placement",
        core_problem="Replacing self-centered, high-friction pitches with low-risk benchmark models.",
        pitches=[
            {
                "title": "Option 1: Direct Numbers Pitch",
                "script": "My incentives are simple: I only make money if we actually get your deal funded on terms that beat what you have. Let me send you a quick sheet showing where the numbers and rates sit today. What is the best email for you?"
            },
            {
                "title": "Option 2: Benchmark Pitch (Zero Pressure)",
                "script": "I am not asking for a commitment right now. Let me send over a clean breakdown showing what we can price this at compared to other lenders. If the math works, great. If not, at least you have a real comparison. Where should I email that?"
            },
            {
                "title": "Option 3: Plain-English Aligned Pitch",
                "script": "If I cannot bring you better terms, higher proceeds, or an easier path to close, we do not expect your business. Let me shoot over a simple one-page breakdown so you can judge the math yourself. What email works best?"
            }
        ],
        script_30s=(
            "Hey [Name], I will be brief. I know I am calling out of the blue.\n\n"
            "I work on the lending side, and the reason for the call is simple: we are funding deals right now where we are consistently beating existing debt terms and finding better capital structures.\n\n"
            "I am not asking you to commit to anything today. My model is simple: I only get paid if we actually deliver numbers that beat what you currently have on the table.\n\n"
            "Let me email you a clean, one-page breakdown showing where our pricing and terms sit today so you have a live benchmark to compare against.\n\n"
            "What is the best email to send that to?"
        ),
        pacing_breakdown=[
            {"time": "0 to 5s", "phase": "Permission & Disarm", "goal": "Acknowledge the interruption to lower guard immediately."},
            {"time": "6 to 15s", "phase": "Core Value", "goal": "State exact capability: beating terms and structure."},
            {"time": "16 to 23s", "phase": "Aligned Hook", "goal": "State contingent, success-only model in plain English."},
            {"time": "24 to 30s", "phase": "Frictionless Close", "goal": "Ask for the destination email, not a commitment."}
        ],
        objections=[
            ObjectionHandler(
                objection="We are all set / We already have a lender.",
                response="Completely understand, and most firms we work with do. The reason I am reaching out is just to give you a live price check. If your current lender is still better, at least you keep them honest. If our math beats theirs, you have another option on the table. What is the best email to send that benchmark to?"
            ),
            ObjectionHandler(
                objection="Just email me some information.",
                response="Happy to do that. Rather than blasting you with generic marketing decks you will never read, what is the main number you care about most right now: rate, loan size, or speed to close? I will send just that one-page breakdown. What address works best?"
            ),
            ObjectionHandler(
                objection="What are your rates?",
                response="It depends on the asset and the structure, but we are actively beating market averages on spread and flexibility right now. If you tell me the rough size of the deal or the debt you have in place, I can email you an exact pricing sheet in ten minutes. What is your email?"
            )
        ],
        rules=[
            "Never ask for trust: Borrowers trust transparent numbers and clean term sheets.",
            "Sell the inbox delivery, not the loan: Close for the email address, not the deal.",
            "Validate before pivoting: Always acknowledge pushback with 'Completely understand' before reframing.",
            "Always end on the destination ask: Never finish an objection response on a statement."
        ]
    )


if __name__ == "__main__":
    playbook = build_loan_playbook()
    playbook.export("loan_origination_playbook")
