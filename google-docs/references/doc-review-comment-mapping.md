# Google Doc review -> section-mapped comment workflow

Use this when user asks for feedback/comments on an existing Google Doc and wants exact placement guidance.

## Goal
Return actionable comments in this format:
- where to comment (section heading + exact highlighted text)
- comment text to paste

## Steps
1. Read doc content:
   - `python scripts/docs_api.py get <DOC_ID> --md`
2. Get heading map with offsets:
   - `python scripts/docs_api.py headings <DOC_ID>`
3. Build comment list grouped by heading hierarchy.
4. For each comment, include:
   - `Where to highlight:` exact phrase from the section
   - `Comment:` paste-ready wording
5. If presentation/deck content is involved, include timing guidance only when user provides session length.

## Output pattern
- Keep comments specific and minimal.
- Prefer phrasing edits that preserve intent.
- For mixed technical/non-technical audiences, prioritize plain-language clarity and audience framing in titles.

## Pitfalls
- Do not give generic suggestions without location anchors.
- Do not invent section names; use headings from `docs_api.py headings`.
- Do not claim live Google comment insertion unless actually performed via API/tooling.