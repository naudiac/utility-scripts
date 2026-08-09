#!/usr/bin/env python3
"""
gws.py — Google Workspace CLI (Drive + Gmail)
Global token: C:\\Users\\whanusiewicz\\.gemini\\config\\google-workspace\\token.json

Usage:
    python gws.py token test
    python gws.py drive list-folder --folder-id FOLDER_ID
    python gws.py drive upload-file --local-path file.pdf --parent-id FOLDER_ID
    python gws.py gmail search --query "from:kim" --limit 5
    python gws.py gmail create-draft --to "kim@example.com" --subject "Hi" --body "Hello" --attach file.pdf

Set $env:PYTHONIOENCODING="utf-8" in PowerShell before running.
"""
import argparse, json, os, sys, time, mimetypes, base64
import urllib.request, urllib.parse, urllib.error
from pathlib import Path

# ── Global token path ─────────────────────────────────────────────────────────
TOKEN_FILE = Path(r"C:\Users\whanusiewicz\.gemini\config\google-workspace\token.json")
DRIVE_BASE = "https://www.googleapis.com/drive/v3"
GMAIL_BASE = "https://gmail.googleapis.com/gmail/v1/users/me"
UPLOAD_BASE = "https://www.googleapis.com/upload/drive/v3"

# ── Rate limiting ─────────────────────────────────────────────────────────────
_last: dict[str, float] = {}
RATE = {"drive": 1/8, "gmail": 1/5, "sheets": 1/4}

def _throttle(api: str):
    gap = RATE.get(api, 0.2)
    since = time.monotonic() - _last.get(api, 0)
    if since < gap:
        time.sleep(gap - since)
    _last[api] = time.monotonic()

# ── Token management ──────────────────────────────────────────────────────────
_token_cache: str | None = None

def get_token() -> str:
    global _token_cache
    if _token_cache:
        return _token_cache
    if not TOKEN_FILE.exists():
        print(f"ERROR: Token file not found at {TOKEN_FILE}", file=sys.stderr)
        print("Run reauth_workspace.py first.", file=sys.stderr)
        sys.exit(1)
    with open(TOKEN_FILE) as f:
        data = json.load(f)
    # Refresh using refresh_token
    params = urllib.parse.urlencode({
        "client_id":     data["client_id"],
        "client_secret": data["client_secret"],
        "refresh_token": data["refresh_token"],
        "grant_type":    "refresh_token",
    }).encode()
    req = urllib.request.Request(data["token_uri"], data=params, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            tok = json.loads(r.read())
        _token_cache = tok["access_token"]
        # Update stored token
        data["token"] = _token_cache
        TOKEN_FILE.write_text(json.dumps(data, indent=2))
        return _token_cache
    except Exception as e:
        # Fall back to stored token
        if data.get("token"):
            _token_cache = data["token"]
            return _token_cache
        raise RuntimeError(f"Token refresh failed: {e}")

# ── HTTP helpers ──────────────────────────────────────────────────────────────
def _api(method: str, url: str, api_type="drive", body=None, headers_extra=None, raw=False):
    _throttle(api_type)
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    if headers_extra:
        headers.update(headers_extra)
    data = json.dumps(body).encode() if body else None
    if data is None and method in ("POST", "PATCH", "PUT"):
        data = b""
        headers["Content-Length"] = "0"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as r:
                if raw:
                    return r.read()
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                time.sleep(2 ** attempt)
                continue
            body_text = e.read().decode(errors="replace")
            raise RuntimeError(f"HTTP {e.code}: {body_text}") from e
    raise RuntimeError("Max retries exceeded")

def _out(data, output_file=None):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    print(s)
    if output_file:
        Path(output_file).write_text(s, encoding="utf-8")

# ── Token commands ────────────────────────────────────────────────────────────
def cmd_token_test(args):
    tok = get_token()
    info = _api("GET", f"https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={tok}", api_type="drive")
    print(f"Token: OK")
    print(f"Scopes: {info.get('scope','')}")
    exp = int(info.get('expires_in', 0))
    print(f"Expires in: {exp}s ({exp//60} min)")

def cmd_token_get(args):
    print(get_token())

# ── Drive commands ────────────────────────────────────────────────────────────
def cmd_drive_list(args):
    url = f"{DRIVE_BASE}/files?q='{args.folder_id}'+in+parents+and+trashed=false&pageSize={args.limit}&fields=files(id,name,mimeType,size,modifiedTime)"
    r = _api("GET", url)
    _out(r, args.output)

def cmd_drive_search(args):
    q = urllib.parse.quote(args.query)
    url = f"{DRIVE_BASE}/files?q={q}&pageSize={args.limit}&fields=files(id,name,mimeType,size)"
    r = _api("GET", url)
    _out(r, args.output)

def cmd_drive_find_folder(args):
    q = f"name='{args.name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if args.parent_id:
        q += f" and '{args.parent_id}' in parents"
    url = f"{DRIVE_BASE}/files?q={urllib.parse.quote(q)}&fields=files(id,name)"
    r = _api("GET", url)
    files = r.get("files", [])
    result = {"id": files[0]["id"], "name": files[0]["name"]} if files else {"id": None}
    _out(result, args.output)

def cmd_drive_create_folder(args):
    # Idempotent: return existing if found
    q = f"name='{args.name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if args.parent_id:
        q += f" and '{args.parent_id}' in parents"
    url = f"{DRIVE_BASE}/files?q={urllib.parse.quote(q)}&fields=files(id,name)"
    existing = _api("GET", url).get("files", [])
    if existing:
        result = {"id": existing[0]["id"], "name": existing[0]["name"], "existed": True}
        _out(result, args.output)
        return
    body = {"name": args.name, "mimeType": "application/vnd.google-apps.folder"}
    if args.parent_id:
        body["parents"] = [args.parent_id]
    r = _api("POST", f"{DRIVE_BASE}/files", body=body)
    _out({"id": r["id"], "name": r["name"], "existed": False}, args.output)

def cmd_drive_upload(args):
    path = Path(args.local_path)
    name = args.name or path.name
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    meta = json.dumps({"name": name, "parents": [args.parent_id]}).encode()
    file_data = path.read_bytes()
    boundary = b"GWS_BOUNDARY_9182736455"
    body = (
        b"--" + boundary + b"\r\n"
        b"Content-Type: application/json; charset=UTF-8\r\n\r\n"
        + meta + b"\r\n"
        b"--" + boundary + b"\r\n"
        + f"Content-Type: {mime}\r\n\r\n".encode()
        + file_data + b"\r\n"
        b"--" + boundary + b"--"
    )
    token = get_token()
    req = urllib.request.Request(
        f"{UPLOAD_BASE}/files?uploadType=multipart",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/related; boundary={boundary.decode()}",
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read())
    _out({"id": result["id"], "name": result.get("name", name)}, args.output)

def cmd_drive_delete(args):
    _api("DELETE", f"{DRIVE_BASE}/files/{args.file_id}")
    print(f"Deleted {args.file_id}")

def cmd_drive_rename(args):
    r = _api("PATCH", f"{DRIVE_BASE}/files/{args.file_id}?fields=id,name", body={"name": args.name})
    _out(r, args.output)

# ── Gmail commands ────────────────────────────────────────────────────────────
def cmd_gmail_search(args):
    q = urllib.parse.quote(args.query)
    url = f"{GMAIL_BASE}/messages?q={q}&maxResults={args.limit}"
    r = _api("GET", url, api_type="gmail")
    messages = r.get("messages", [])
    results = []
    for m in messages:
        detail = _api("GET", f"{GMAIL_BASE}/messages/{m['id']}?format=metadata&metadataHeaders=From&metadataHeaders=To&metadataHeaders=Subject&metadataHeaders=Date", api_type="gmail")
        headers = {h["name"]: h["value"] for h in detail.get("payload", {}).get("headers", [])}
        results.append({"id": m["id"], "from": headers.get("From",""), "to": headers.get("To",""), "subject": headers.get("Subject",""), "date": headers.get("Date","")})
    _out(results, args.output)

def cmd_gmail_get(args):
    r = _api("GET", f"{GMAIL_BASE}/messages/{args.message_id}?format=full", api_type="gmail")
    _out(r, args.output)

def cmd_gmail_list_labels(args):
    r = _api("GET", f"{GMAIL_BASE}/labels", api_type="gmail")
    _out(r, args.output)

def cmd_gmail_create_label(args):
    # Idempotent
    existing = _api("GET", f"{GMAIL_BASE}/labels", api_type="gmail").get("labels", [])
    for lb in existing:
        if lb["name"].lower() == args.name.lower():
            _out({"id": lb["id"], "name": lb["name"], "existed": True}, args.output)
            return
    r = _api("POST", f"{GMAIL_BASE}/labels", api_type="gmail", body={"name": args.name})
    _out({"id": r["id"], "name": r["name"], "existed": False}, args.output)

def _build_message(to, subject, body, cc=None, attach_paths=None):
    """Build a MIME email and return base64url-encoded string."""
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders as enc
    if attach_paths:
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, "plain"))
    else:
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, "plain"))
    msg["To"]      = to
    msg["Subject"] = subject
    if cc:
        msg["Cc"] = cc
    if attach_paths:
        for ap in attach_paths:
            p = Path(ap)
            mime_type, _ = mimetypes.guess_type(str(p))
            maintype, subtype = (mime_type or "application/octet-stream").split("/", 1)
            part = MIMEBase(maintype, subtype)
            part.set_payload(p.read_bytes())
            enc.encode_base64(part)
            part.add_header("Content-Disposition", "attachment", filename=p.name)
            msg.attach(part)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return raw

def cmd_gmail_create_draft(args):
    attach = args.attach.split(",") if args.attach else None
    raw = _build_message(args.to, args.subject, args.body, args.cc, attach)
    body = {"message": {"raw": raw}}
    if args.thread_id:
        body["message"]["threadId"] = args.thread_id
    r = _api("POST", f"{GMAIL_BASE}/drafts", api_type="gmail", body=body)
    print(f"Draft created: {r.get('id')}")
    _out(r, args.output)

def cmd_gmail_send(args):
    attach = args.attach.split(",") if args.attach else None
    raw = _build_message(args.to, args.subject, args.body, args.cc, attach)
    r = _api("POST", f"{GMAIL_BASE}/messages/send", api_type="gmail", body={"raw": raw})
    print(f"Sent! Message ID: {r.get('id')}")
    _out(r, args.output)

def cmd_gmail_send_draft(args):
    r = _api("POST", f"{GMAIL_BASE}/drafts/send", api_type="gmail", body={"id": args.draft_id})
    print(f"Draft sent! Message ID: {r.get('id')}")
    _out(r, args.output)

def cmd_gmail_delete_draft(args):
    _api("DELETE", f"{GMAIL_BASE}/drafts/{args.draft_id}", api_type="gmail")
    print(f"Draft deleted: {args.draft_id}")

def cmd_gmail_apply_label(args):
    r = _api("POST", f"{GMAIL_BASE}/messages/{args.message_id}/modify", api_type="gmail",
             body={"addLabelIds": [args.label_id]})
    _out(r, args.output)

# ── Sheets commands ───────────────────────────────────────────────────────────
def cmd_sheets_create(args):
    body = {"properties": {"title": args.name}}
    r = _api("POST", "https://sheets.googleapis.com/v4/spreadsheets", api_type="sheets", body=body)
    sheet_id = r["spreadsheetId"]
    # Move to parent if specified
    if args.parent_id:
        _api("PATCH", f"{DRIVE_BASE}/files/{sheet_id}?addParents={args.parent_id}&removeParents=root&fields=id", api_type="drive")
    _out({"id": sheet_id, "url": r["spreadsheetUrl"]}, args.output)

def cmd_sheets_append(args):
    vals = [[v.strip() for v in args.values.split(",")]]
    sheet = urllib.parse.quote(args.sheet_name or "Sheet1")
    r = _api("POST", f"https://sheets.googleapis.com/v4/spreadsheets/{args.sheet_id}/values/{sheet}!A1:append?valueInputOption=USER_ENTERED",
             api_type="sheets", body={"values": vals})
    _out(r, args.output)

# ── CLI wiring ────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(prog="gws.py", description="Google Workspace CLI (Drive + Gmail)")
    sub = parser.add_subparsers(dest="cmd")

    # token
    t = sub.add_parser("token"); ts = t.add_subparsers(dest="sub")
    ts.add_parser("test"); ts.add_parser("get")

    # drive
    d = sub.add_parser("drive"); ds = d.add_subparsers(dest="sub")
    def da(cmd_name, **kw): p = ds.add_parser(cmd_name); [p.add_argument(f"--{k}", **v) for k,v in kw.items()]; p.add_argument("--output", default=None); return p
    da("list-folder",    folder_id=dict(required=True), limit=dict(default=50, type=int))
    da("search",         query=dict(required=True),     limit=dict(default=20, type=int))
    da("find-folder",    **{"name": dict(required=True), "parent_id": dict(default=None)})
    da("create-folder",  **{"name": dict(required=True), "parent_id": dict(default=None)})
    da("upload-file",    local_path=dict(required=True), parent_id=dict(required=True), **{"name": dict(default=None)})
    da("delete",         file_id=dict(required=True))
    da("rename",         file_id=dict(required=True),   **{"name": dict(required=True)})

    # gmail
    g = sub.add_parser("gmail"); gs = g.add_subparsers(dest="sub")
    def ga(cmd_name, **kw): p = gs.add_parser(cmd_name); [p.add_argument(f"--{k}", **v) for k,v in kw.items()]; p.add_argument("--output", default=None); return p
    ga("search",       query=dict(required=True), limit=dict(default=10, type=int))
    ga("get-message",  message_id=dict(required=True))
    ga("list-labels")
    ga("create-label", **{"name": dict(required=True)})
    ga("create-draft", to=dict(required=True), subject=dict(required=True), body=dict(required=True),
                       cc=dict(default=None), attach=dict(default=None), thread_id=dict(default=None))
    ga("send",         to=dict(required=True), subject=dict(required=True), body=dict(required=True),
                       cc=dict(default=None), attach=dict(default=None))
    ga("send-draft",   draft_id=dict(required=True))
    ga("delete-draft", draft_id=dict(required=True))
    ga("apply-label",  message_id=dict(required=True), label_id=dict(required=True))

    # sheets
    sh = sub.add_parser("sheets"); shs = sh.add_subparsers(dest="sub")
    def sha(cmd_name, **kw): p = shs.add_parser(cmd_name); [p.add_argument(f"--{k}", **v) for k,v in kw.items()]; p.add_argument("--output", default=None); return p
    sha("create",     **{"name": dict(required=True), "parent_id": dict(default=None)})
    sha("append-row", sheet_id=dict(required=True), values=dict(required=True), sheet_name=dict(default="Sheet1"))

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help(); return

    dispatch = {
        ("token","test"):          cmd_token_test,
        ("token","get"):           cmd_token_get,
        ("drive","list-folder"):   cmd_drive_list,
        ("drive","search"):        cmd_drive_search,
        ("drive","find-folder"):   cmd_drive_find_folder,
        ("drive","create-folder"): cmd_drive_create_folder,
        ("drive","upload-file"):   cmd_drive_upload,
        ("drive","delete"):        cmd_drive_delete,
        ("drive","rename"):        cmd_drive_rename,
        ("gmail","search"):        cmd_gmail_search,
        ("gmail","get-message"):   cmd_gmail_get,
        ("gmail","list-labels"):   cmd_gmail_list_labels,
        ("gmail","create-label"):  cmd_gmail_create_label,
        ("gmail","create-draft"):  cmd_gmail_create_draft,
        ("gmail","send"):          cmd_gmail_send,
        ("gmail","send-draft"):    cmd_gmail_send_draft,
        ("gmail","delete-draft"):  cmd_gmail_delete_draft,
        ("gmail","apply-label"):   cmd_gmail_apply_label,
        ("sheets","create"):       cmd_sheets_create,
        ("sheets","append-row"):   cmd_sheets_append,
    }
    fn = dispatch.get((args.cmd, getattr(args,"sub",None)))
    if fn:
        fn(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
