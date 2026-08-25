# Event feedback visual reporting from Google Forms

Use this when the user asks for an executive PDF/report from a one-time event feedback form, especially when the form includes ratings plus free-text reflections or prayer/pastoral-care inputs.

## Workflow

1. Fetch form structure first so the report uses the real question set:
   - `get` confirms title, responder URL, question count, and item types.
   - Note which questions are `RATING`, `MULTIPLE_CHOICE`, `TEXT`, or `PARAGRAPH_TEXT`.
2. Fetch responses with a generous timeout. Apps Script response export may take more than a minute even for modest response counts.
   - If using the deployed web app directly, POST JSON and handle the 302 redirect manually: `requests.post(..., allow_redirects=False)` then `requests.get(Location)`.
   - If the initial response returns only the helper action list, verify that the POST body/action key matches the deployed helper's contract.
   - If response export times out, retry with a longer timeout before falling back to a linked response sheet.
3. Normalize responses:
   - Ratings: parse numeric strings and compute average, distribution, top-box (`5`), and top-2-box (`4–5`).
   - Single-select: count each selected option once.
   - Free text: preserve non-empty answers separately; remove placeholder-only values such as `-` only for summary counts, not from raw appendix if exactness matters.
   - Checkbox answers may need flattening if exported as lists or comma-joined strings.
4. Create an executive visual report, not just raw tables:
   - Cover with response count, overall score, duration fit / strongest signal, and free-text count.
   - Executive summary: what worked, what to improve next.
   - Audience snapshot: role and group/date distribution.
   - Score dashboard: rating averages plus stacked rating distribution.
   - Duration or logistics readout when present.
   - Qualitative themes with clearly labeled heuristic/theme coding.
   - Representative quotes.
   - Appendix with all qualitative inputs.
5. Privacy handling:
   - Omit participant names from public appendices unless the user explicitly asks for named rows.
   - Keep role/group context when useful.
   - Prayer requests and pastoral-care inputs are sensitive; include a discretion note and avoid over-broadcasting the raw file.
6. Visual production pattern:
   - Static HTML with inline CSS and SVG charts is sufficient and portable.
   - Render to PDF with `wkhtmltopdf --enable-local-file-access` when available.
   - Generate a PNG contact sheet with `pdftoppm` + PIL and visually QA before delivery.
   - Check for split/blank pages, clipped charts, unreadable appendix tables, and placeholder/error text (`undefined`, `NaN`, `lorem`, etc.).

## Durable lessons

- A form can have a public responder URL but still require the editable form file ID for helper/API access; use the `/forms/d/FORM_FILE_ID/edit` ID, not the `/forms/d/e/1FAIpQL.../viewform` published ID.
- The deployed Apps Script helper can be account-bound and may not expose all Forms settings; do not claim email collection or anonymity unless verified separately.
- If the Python helper script is missing locally, direct POST to the `GFORMS` URL loaded from `.env` is a valid fallback. Never print the secret web-app URL.
- For event feedback, free-text questions are often the most valuable part of the report. Explicitly report response coverage for each free-text field, then separate representative quotes from the full appendix.
