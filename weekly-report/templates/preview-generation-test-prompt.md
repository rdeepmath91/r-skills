# Weekly report preview generation test prompt

Copy this prompt when asking another agent to test weekly-report generation in a safe preview. Replace bracketed values and keep the prompt short so the skill itself carries the detailed rules.

```text
Load and follow the `weekly-report` skill, including its deterministic validation guidance.

This is a test run. Do not edit the live/original doc.

Mode: generate-from-sources.

Report subject: <REPORT_SUBJECT>
Target report title:
[Weekly Report: <REPORT_SUBJECT>] <START_DATE> - <END_DATE>

Live/original doc to copy or use as template/reference only:
<LIVE_DOC_URL>

Reference/sample formatting doc:
<REFERENCE_DOC_URL>

Task:
1. Create a fresh preview copy/doc.
2. Rename it:
   [TEST Weekly Report: <REPORT_SUBJECT>] <START_DATE> - <END_DATE>
3. Fill the preview using the `weekly-report` skill.
4. Validate against the skill's deterministic contract and the reference formatting doc.
5. If validation finds safe mechanical formatting/link/list issues, repair the preview only and revalidate.
6. Do not touch the live/original doc.

Important:
- Do not use the already-filled live doc as the data source for report content.
- Do not invent unavailable data; mark those sections as needing input.
- `repair_weekly_report_format.py` may be used as a repair helper, but not as the final PASS oracle.
- Use generic subject wording in reusable notes; do not hard-code the report subject's personal name into skill details.

Final response:
- Preview URL:
- Preview doc ID:
- Live/original edited? yes/no:
- Mode actually performed:
- Content generated from sources or copied from live?:
- Verdicts: CONTENT_PASS/FAIL, FORMAT_PASS/FAIL, DATA_GENERATION_PASS/FAIL or NOT_TESTED, FINAL_PASS/FAIL:
- Sections filled:
- Sections needing input:
- First validation failures:
- Fixes applied in preview:
- Remaining failures/risks:
- Safe to apply to live? yes/no + why:
```
