#!/usr/bin/env python3
"""Post-refresh audit for Google Docs target docs.

Checks per doc:
1) heading order (optional, user-provided sequence)
2) code-like paragraph spacing style presence (spaceAbove/spaceBelow keys)
3) landscape/portrait section break counts
4) Drive modifiedTime + webViewLink

Usage:
  python preview_post_refresh_audit.py \
    --docs docA=DOC_ID docB=DOC_ID

Optional heading order check:
  python preview_post_refresh_audit.py \
    --docs docA=DOC_ID \
    --heading-order "Section A" "Section B" "Section C"

Notes:
- Treat {'unit':'PT'} on spaceAbove/spaceBelow as valid zero spacing.
- Detection avoids false positives by combining monospace ratio + code token heuristics.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]
MONO = {"Roboto Mono", "Courier New"}
CODE_TOKENS = ("{", "}", "=>", "->", "class ", "def ", "async ", "import ", '"', "[", "]", ":")


def load_creds() -> Credentials:
    token = Path(os.getenv("HERMES_HOME", str(Path.home() / ".hermes"))) / "google_token.json"
    creds = Credentials.from_authorized_user_file(str(token), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token.write_text(creds.to_json())
    return creds


def text_of_paragraph(para: dict) -> Tuple[str, float]:
    total = 0
    mono = 0
    parts: List[str] = []
    for e in para.get("elements", []):
        tr = e.get("textRun", {})
        t = tr.get("content", "")
        parts.append(t)
        total += len(t)
        ff = tr.get("textStyle", {}).get("weightedFontFamily", {}).get("fontFamily")
        if ff in MONO:
            mono += len(t)
    ratio = (mono / total) if total else 0.0
    return "".join(parts).strip("\n"), ratio


def is_code_like(text: str, mono_ratio: float) -> bool:
    t = text.strip()
    if not t:
        return False
    has_code_token = any(tok in t for tok in CODE_TOKENS)
    longish = len(t) >= 12
    return (mono_ratio >= 0.65 and has_code_token and longish) or (mono_ratio >= 0.9 and longish)


def parse_docs(pairs: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for p in pairs:
        k, v = p.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def evaluate_heading_order(content: List[dict], heading_order: List[str]) -> dict:
    if not heading_order:
        return {
            "enabled": False,
            "ok": None,
            "expected": [],
            "positions": {},
            "missing": [],
        }

    positions = {h: -1 for h in heading_order}
    for el in content:
        para = el.get("paragraph")
        if not para:
            continue
        text, _ = text_of_paragraph(para)
        if text in positions and positions[text] == -1:
            positions[text] = el.get("startIndex", -1)

    missing = [h for h, pos in positions.items() if pos == -1]
    in_order = all(
        positions[heading_order[i]] < positions[heading_order[i + 1]]
        for i in range(len(heading_order) - 1)
        if positions[heading_order[i]] != -1 and positions[heading_order[i + 1]] != -1
    )
    ok = (len(missing) == 0) and in_order

    return {
        "enabled": True,
        "ok": ok,
        "expected": heading_order,
        "positions": positions,
        "missing": missing,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", nargs="+", required=True, help="name=doc_id pairs")
    ap.add_argument(
        "--heading-order",
        nargs="*",
        default=[],
        help="Optional heading sequence to enforce (exact text, in order)",
    )
    args = ap.parse_args()

    docs_map = parse_docs(args.docs)
    creds = load_creds()
    docs = build("docs", "v1", credentials=creds, cache_discovery=False)
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    report = {}
    for name, doc_id in docs_map.items():
        d = docs.documents().get(documentId=doc_id).execute(num_retries=5)
        content = d.get("body", {}).get("content", [])

        code_like = 0
        spacing_ok = 0
        spacing_missing = 0
        spacing_partial = 0

        for el in content:
            para = el.get("paragraph")
            if not para:
                continue
            text, mono_ratio = text_of_paragraph(para)
            if is_code_like(text, mono_ratio):
                code_like += 1
                ps = para.get("paragraphStyle", {})
                has_sa = "spaceAbove" in ps
                has_sb = "spaceBelow" in ps
                if has_sa and has_sb:
                    spacing_ok += 1
                elif has_sa or has_sb:
                    spacing_partial += 1
                else:
                    spacing_missing += 1

        landscape = 0
        portrait = 0
        for el in content:
            sb = el.get("sectionBreak")
            if not sb:
                continue
            if sb.get("sectionStyle", {}).get("flipPageOrientation", False):
                landscape += 1
            else:
                portrait += 1

        heading = evaluate_heading_order(content, args.heading_order)

        meta = drive.files().get(
            fileId=doc_id,
            fields="id,name,modifiedTime,webViewLink",
        ).execute(num_retries=5)

        report[name] = {
            "doc_id": doc_id,
            "heading_order": heading,
            "code_like_paragraphs": code_like,
            "spacing_ok_both_keys": spacing_ok,
            "spacing_partial_one_key": spacing_partial,
            "spacing_missing": spacing_missing,
            "section_breaks": {"landscape": landscape, "portrait": portrait},
            "modifiedTime": meta.get("modifiedTime"),
            "webViewLink": meta.get("webViewLink"),
        }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
