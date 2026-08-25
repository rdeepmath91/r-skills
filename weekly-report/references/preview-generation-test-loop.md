# Weekly report preview-generation test loop

Use this when the user wants another agent to test whether the `weekly-report` skill can create and validate a weekly report without touching the live doc.

## Test intent

Keep the prompt small. The point is to test whether the agent loads the skill, creates a safe preview copy, generates/fills the report, validates it against the reference/fingerprint, repairs safe mechanical issues in the preview, and revalidates.

Do not restate all formatting rules in the prompt; those belong in the skill. The test should reveal whether the skill itself is sufficient.

The test must declare its mode:
- `generate-from-sources`: tests real report generation; live doc is template/reference only.
- `copy-and-repair`: tests restoration/format repair; does not prove generation.
- `validate-only`: audits a doc without edits.

Do not claim generation was tested if content was copied from the already-filled live doc.

## Minimal prompt template

Prefer copying `templates/preview-generation-test-prompt.md` when available. Keep the task prompt generic: use `<REPORT_SUBJECT>` / "report subject" placeholders in reusable instructions instead of hard-coding a personal name into skill details.

```text
Load and follow the `weekly-report` skill, including its linked deterministic validation guidance.

This is a test run. Do not edit the live/original doc.

Live/original doc to copy:
<DOC_URL>

Reference/sample formatting doc:
<REFERENCE_DOC_URL>

Target report:
[Weekly Report: <REPORT_SUBJECT>] <START_DATE> - <END_DATE>

Task:
1. Create a fresh copy/preview of the live/original doc, or create a new preview doc from the live template if Drive copy is unavailable.
2. Rename the preview:
   [TEST Weekly Report: <REPORT_SUBJECT>] <START_DATE> - <END_DATE>
3. Fill the preview using the `weekly-report` skill in `generate-from-sources` mode.
4. Validate the preview using the skill's final verification checklist and deterministic validation guidance.
5. If validation finds mechanical formatting/link/list issues, fix the preview and validate again.
6. Do not touch the live/original doc.

Important:
- Do not invent unavailable data.
- If a source is unavailable, mark that section as needing input.
- Keep the feedback loop inside the preview only: generate -> validate -> repair preview if safe -> revalidate.
- State whether content was generated from sources or copied from the live doc/template.
- `repair_weekly_report_format.py` may be used as a repair helper, but it is not a final PASS oracle.

Final response:
- Preview copy URL:
- Live/original edited? yes/no:
- Content generated from sources or copied from live/template?:
- Validation pass/fail:
- Sections filled:
- Sections needing input:
- Issues found on first validation:
- Fixes applied after validation:
- Remaining failures/risks:
- Recommendation: safe to apply to live? yes/no + why
```

## Pass/fail criteria

A repair script returning PASS is not enough. The final verdict must compare the preview against the deterministic contract and the reference doc.

PASS requires:
- fresh preview/copy doc, not a reused prior preview unless explicitly requested
- live/original doc untouched
- placeholder/raw URL checks pass
- section order present and correct
- heading styles match the reference/fingerprint
- list style and nesting match the reference/fingerprint
- PR rows have exactly one visible final `#N`
- PR links are only on the final trailing `#N`
- unavailable data is marked as needing input, not fabricated

FAIL if:
- the agent only copies already-filled live content while claiming generation was tested
- the validation oracle is only `repair_weekly_report_format.py`
- remaining formatting mismatches are labeled “minor” when they violate the reference style contract
- Issues nesting is flattened when the reference uses nested numbering
- native/manual list style differs from the reference and was not explicitly accepted

## External audit handoff

If the user wants a second-pass audit, the generating agent should include enough detail for another agent to independently validate:
- preview doc ID/URL
- live doc ID/URL
- reference doc ID/URL
- previous-week doc ID/URL if used
- exact validation command(s)
- list of first-pass failures and repairs
- remaining failures

The auditor should not trust the generator's PASS label; it should read back Docs API structure and compare against the reference/fingerprint.
