#!/usr/bin/env python3
"""Repair formatting in an an existing weekly report Google Doc.

Usage:
  python scripts/repair_weekly_report_format.py DOC_ID [TAB_ID]

What it does:
- Runs a legacy/manual-numbering repair pass for existing weekly reports.
- Confirms the seven expected section headings are HEADING_2 for that legacy style.
- Converts accidental native Docs bullets/numbering into visible manual numbering,
  matching some recent weekly-report exports and avoiding mobile/visual spacing drift.
- Resets all non-heading content to NORMAL_TEXT, Proxima Nova, 20pt spaceAbove,
  0pt spaceBelow, 100% line spacing.
- Adds missing "Pull Requests" under Accomplishments when absent.
- Preserves links by not rewriting linked text runs.

Important:
- This is NOT a final reference-format validator.
- A repair-helper PASS from this script must not be reported as final weekly-report PASS.
- Run reference/fingerprint validation separately for title style, heading style, native/manual
  list style, issue nesting, PR link ranges, and section-specific conventions.

Requires a valid Google Docs/Drive OAuth token at ~/.hermes/google_token.json.
"""

import json
import sys
import time
import urllib.request
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SECTION_HEADINGS = {
    "Issues",
    "Accomplishments",
    "Meetings/Events/Training/Conferences",
    "Key Metrics / OMTM",
    "Next Actions",
    "Technology, Business, Communication, Leadership, Management & Marketing",
    "Out of Office",
}
TITLE_PREFIX = "[Weekly Report:"
TOKEN_PATH = Path.home() / ".hermes/google_token.json"


def token():
    data = json.loads(TOKEN_PATH.read_text())
    creds = Credentials.from_authorized_user_info(data, data.get("scopes"))
    if not creds.valid:
        creds.refresh(Request())
        out = json.loads(creds.to_json())
        out.setdefault("scopes", data.get("scopes"))
        TOKEN_PATH.write_text(json.dumps(out, indent=2))
        data = out
    return data.get("token") or creds.token


def request_json(method, url, tok, payload=None):
    body = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        return json.loads(response.read().decode() or "{}")


def get_doc(doc_id, tok):
    return request_json(
        "GET",
        f"https://docs.googleapis.com/v1/documents/{doc_id}?includeTabsContent=true",
        tok,
    )


def tab_body(doc, tab_id):
    if tab_id:
        for tab in doc.get("tabs", []):
            if tab["tabProperties"]["tabId"] == tab_id:
                return tab["documentTab"]["body"]
    return doc.get("body") or doc["tabs"][0]["documentTab"]["body"]


def ptext(paragraph):
    return "".join(
        e.get("textRun", {}).get("content", "") for e in paragraph.get("elements", [])
    ).strip("\n")


def paragraphs(doc, tab_id):
    rows = []
    for element in tab_body(doc, tab_id)["content"]:
        paragraph = element.get("paragraph")
        if not paragraph:
            continue
        rows.append(
            {
                "start": element.get("startIndex"),
                "end": element.get("endIndex"),
                "text": ptext(paragraph),
                "paragraph": paragraph,
                "bullet": paragraph.get("bullet"),
            }
        )
    return rows


def batch(doc_id, tok, requests, chunk_size=20):
    for i in range(0, len(requests), chunk_size):
        chunk = requests[i : i + chunk_size]
        for attempt in range(4):
            try:
                request_json(
                    "POST",
                    f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate",
                    tok,
                    {"requests": chunk},
                )
                break
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(1.5 * (attempt + 1))


def bullet_conversion_requests(rows):
    counters = {}
    inserts = []
    deletes = []
    for row in rows:
        bullet = row.get("bullet")
        if not bullet:
            continue
        text = row["text"]
        deletes.append(
            {"deleteParagraphBullets": {"range": {"startIndex": row["start"], "endIndex": row["end"] - 1}}}
        )
        if not text.strip():
            continue
        list_id = bullet.get("listId", "default")
        level = bullet.get("nestingLevel", 0)
        levels = counters.setdefault(list_id, {})
        levels[level] = levels.get(level, 0) + 1
        for deeper in list(levels):
            if deeper > level:
                del levels[deeper]
        prefix = f"{'   ' * level}{levels[level]}. "
        if not text.lstrip().startswith(prefix.strip()):
            inserts.append({"insertText": {"location": {"index": row["start"]}, "text": prefix}})
    return deletes, sorted(inserts, key=lambda r: r["insertText"]["location"]["index"], reverse=True)


def ensure_pull_requests(doc_id, tab_id, tok):
    rows = paragraphs(get_doc(doc_id, tok), tab_id)
    for idx, row in enumerate(rows):
        if row["text"].strip() == "Accomplishments":
            nxt = rows[idx + 1] if idx + 1 < len(rows) else None
            if not nxt or nxt["text"].strip() != "Pull Requests":
                at = nxt["start"] if nxt else row["end"] - 1
                batch(doc_id, tok, [{"insertText": {"location": {"index": at}, "text": "Pull Requests\n"}}])
            return


def style_requests(rows):
    requests = []
    for row in rows:
        text = row["text"].strip()
        if row["start"] is None or row["end"] is None or row["end"] <= row["start"]:
            continue
        rng = {"startIndex": row["start"], "endIndex": row["end"] - 1}
        if text.startswith(TITLE_PREFIX):
            requests.append(
                {
                    "updateParagraphStyle": {
                        "range": rng,
                        "paragraphStyle": {"namedStyleType": "HEADING_1", "spaceAbove": {"magnitude": 20, "unit": "PT"}, "lineSpacing": 100},
                        "fields": "namedStyleType,spaceAbove,lineSpacing",
                    }
                }
            )
            continue
        if text in SECTION_HEADINGS:
            requests.append(
                {
                    "updateParagraphStyle": {
                        "range": rng,
                        "paragraphStyle": {"namedStyleType": "HEADING_2", "spaceAbove": {"magnitude": 20, "unit": "PT"}, "spaceBelow": {"magnitude": 0, "unit": "PT"}, "lineSpacing": 100},
                        "fields": "namedStyleType,spaceAbove,spaceBelow,lineSpacing",
                    }
                }
            )
            requests.append(
                {
                    "updateTextStyle": {
                        "range": rng,
                        "textStyle": {"weightedFontFamily": {"fontFamily": "Proxima Nova"}, "fontSize": {"magnitude": 16, "unit": "PT"}, "bold": True},
                        "fields": "weightedFontFamily,fontSize,bold",
                    }
                }
            )
        else:
            requests.append(
                {
                    "updateParagraphStyle": {
                        "range": rng,
                        "paragraphStyle": {"namedStyleType": "NORMAL_TEXT", "spaceAbove": {"magnitude": 20, "unit": "PT"}, "spaceBelow": {"magnitude": 0, "unit": "PT"}, "lineSpacing": 100, "indentStart": {"magnitude": 0, "unit": "PT"}, "indentFirstLine": {"magnitude": 0, "unit": "PT"}},
                        "fields": "namedStyleType,spaceAbove,spaceBelow,lineSpacing,indentStart,indentFirstLine",
                    }
                }
            )
            if text:
                requests.append(
                    {
                        "updateTextStyle": {
                            "range": rng,
                            "textStyle": {"weightedFontFamily": {"fontFamily": "Proxima Nova"}, "fontSize": {"magnitude": 11, "unit": "PT"}},
                            "fields": "weightedFontFamily,fontSize",
                        }
                    }
                )
    return requests


def validate(doc_id, tab_id, tok):
    rows = paragraphs(get_doc(doc_id, tok), tab_id)
    sections = set()
    unexpected_h2 = []
    bullets = 0
    problems = []
    placeholders = 0
    raw_urls = 0
    links = 0
    for idx, row in enumerate(rows):
        text = row["text"].strip()
        paragraph = row["paragraph"]
        style = paragraph.get("paragraphStyle", {})
        named = style.get("namedStyleType")
        placeholders += row["text"].count("(please insert here)")
        raw_urls += row["text"].count("https://") + row["text"].count("http://")
        if row.get("bullet"):
            bullets += 1
        if text in SECTION_HEADINGS:
            sections.add(text)
            if named != "HEADING_2":
                problems.append((idx, "section_not_heading_2", text, named))
        elif text.startswith(TITLE_PREFIX):
            if named != "HEADING_1":
                problems.append((idx, "title_not_heading_1", text, named))
        elif text and named != "NORMAL_TEXT":
            problems.append((idx, "body_not_normal_text", text[:80], named))
        if named == "HEADING_2" and text not in SECTION_HEADINGS:
            unexpected_h2.append(text)
        for element in paragraph.get("elements", []):
            text_run = element.get("textRun")
            if text_run and text_run.get("textStyle", {}).get("link"):
                links += 1
    repair_helper_pass = (
        len(SECTION_HEADINGS - sections) == 0
        and len(unexpected_h2) == 0
        and bullets == 0
        and len(problems) == 0
        and placeholders == 0
        and raw_urls == 0
    )
    return {
        "validation_scope": "legacy_manual_numbering_repair_helper_only_not_reference_format_validation",
        "repair_helper_status": "PASS" if repair_helper_pass else "FAIL",
        "final_weekly_report_verdict": "NOT_EVALUATED_BY_THIS_SCRIPT",
        "must_run_reference_validation": True,
        "warning": "Do not report repair_helper_status as final PASS; compare against the reference/fingerprint for title, headings, list style, nesting, and PR/link conventions.",
        "sections_found": len(sections),
        "missing_sections": sorted(SECTION_HEADINGS - sections),
        "unexpected_heading2_count": len(unexpected_h2),
        "native_bullet_paragraphs_remaining": bullets,
        "problem_count": len(problems),
        "problems": problems[:20],
        "placeholders": placeholders,
        "raw_urls_visible": raw_urls,
        "link_runs": links,
    }


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: repair_weekly_report_format.py DOC_ID [TAB_ID]")
    doc_id = sys.argv[1]
    tab_id = sys.argv[2] if len(sys.argv) > 2 else None
    tok = token()

    rows = paragraphs(get_doc(doc_id, tok), tab_id)
    deletes, inserts = bullet_conversion_requests(rows)
    if deletes:
        batch(doc_id, tok, deletes)
    if inserts:
        batch(doc_id, tok, inserts)

    ensure_pull_requests(doc_id, tab_id, tok)
    rows = paragraphs(get_doc(doc_id, tok), tab_id)
    batch(doc_id, tok, style_requests(rows))
    print(json.dumps(validate(doc_id, tab_id, tok), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
