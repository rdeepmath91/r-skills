# Google Forms response results analysis

Use this when the user asks to check current form results, summarize early responses, or convert Google Forms results into slide/workshop content. For the Agent Skills quick-check form specifically, pair this with `references/agent-skills-quick-check-recap-notes.md`.

## Reliable workflow
1. Load the form skill and use the deployed helper as source of truth.
2. Fetch responses with a generous timeout; small response sets can still exceed 60s because Apps Script redirects and response export can be slow.

```bash
cd /home/raymond-christopher/.hermes/skills/productivity/google-forms
python3 scripts/gform.py responses FORM_ID > /tmp/form_responses.json
```

If it times out, retry once with a longer timeout rather than reporting failure immediately.

3. Aggregate by question:
   - Single-select: count each string answer once.
   - Checkbox/multi-select: flatten each list and count each selected option independently.
   - Free text: list non-empty answers separately; do not over-aggregate unless the user asks for themes.

4. For status confidence, optionally run `get` too and report current `questionCount`, `responderUri`, and whether stale questions are absent.

## Summary format that worked well
Keep it decision-oriented:

1. Total responses.
2. Form health/state: question count, stale questions gone, public link if relevant.
3. Key findings by question with counts and percentages.
4. Short interpretation: what the session/training should emphasize.
5. Free-text examples as bullets.

## Visual PDF / executive report format
When the user asks for a full PDF result, visual charts, executive summary, scores, or qualitative inputs from an event feedback form, do not stop at a chat summary. Use `references/event-feedback-visual-reporting.md` and produce a local artifact:

1. Fetch live form structure and responses.
2. Aggregate ratings, selected options, and free-text response coverage.
3. Build a static HTML report with inline SVG charts.
4. Convert to PDF.
5. Render a contact sheet and visually QA layout before delivery.
6. Include free-text appendix with privacy-sensitive fields handled carefully.

## Slide-content recap format
When the user says the results are for slides, a deck, a workshop outline, or a live session document, do not deliver only a raw survey report. Convert the result into a slide-content recap pack:

1. Audience snapshot: who answered, normalized role buckets, and any audience skew.
2. Adoption/usage signal: what share has used, created, or never used the thing being surveyed.
3. Current use cases: top existing workflows, with counts and percentages.
4. Biggest learning needs: top selected needs, with a concise interpretation.
5. Free-text themes: cluster concrete examples instead of dumping all answers.
6. Session implications: what to add, remove, shorten, or emphasize in the slide outline.
7. Optional appendix: raw counts for validation, clearly marked as appendix material.

## Visual PDF report pattern
When turning Google Forms results into a PDF, especially for community/event feedback:

1. Pull live form metadata and responses, then save raw JSON/CSV locally for reproducibility.
2. Aggregate scores and free-text separately. Preserve all meaningful qualitative inputs, but remove participant names from appendices unless the user explicitly asks for attribution.
3. If the user requests design alternatives, generate one-page style samples first using the same real survey data. Include a contact sheet so the user can compare quickly.
4. For Indonesian community contexts, use simple hybrid English-Indonesian copy rather than formal executive wording. The report should feel useful for leaders who need action, not like a corporate board deck.
5. Make the main narrative pages large and readable: bigger titles, card titles, body, and chart labels. Keep appendix smaller only when needed.
6. Reduce wasted space with 2-column grids, grouped charts, action cards, and leader-takeaway strips. A sparse page is a design defect unless the page is intentionally a cover/divider.
7. Run PDF + contact-sheet QA and inspect for: blank/sparse pages, cropped margins, inconsistent column alignment, tiny body text, chart rendering failures, and appendix overflows.

For Agent Skills survey results, the most useful transformation is usually:
- keep basic definitions short if most respondents have hands-on exposure;
- add a “when repeated work should become a skill” decision slide if that need ranks high;
- add team sharing/maintenance guidance if that need ranks high;
- use respondent free-text examples as demo anchors;
- call out interface skew, especially when usage is CLI-heavy but the session should include AIP/GLChat, IDE, and web-chat surfaces.

## Pitfalls
- Do not assume response identity/email collection settings; current helper may not expose them. Only state respondent counts and submitted answers.
- Normalize obvious label variants in the interpretation, but preserve raw counts if the exact option labels differ. Example: `Data Developer` and `Data Developer (DD)` can be interpreted together while still noting the raw split if useful.
- Native inline `Other: ____` answers may appear as custom labels in response exports (for example `Claude websites` or `Exploration`). Treat them as real respondent-provided option values and call them out as `Other` when summarizing.
- Because checkbox questions allow multiple selections, percentages are per respondent and can sum over 100%.
