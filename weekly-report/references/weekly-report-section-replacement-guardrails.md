# Weekly report section replacement guardrails

Use this after any weekly-report edit where one section is replaced from another source, especially `Issues` from `AIP Current Issues`.

## Lessons from the 28 Jun–04 Jul 2026 report

### Copy the whole source section when asked for the latest issue tab

If Raymond says to copy the updated issue(s) from the latest `AIP Current Issues` tab, do not insert only the one item that was discussed in the chat. Re-read the latest source tab and copy all top-level issue items in that tab into the weekly report's `Issues` section.

Verification target:

- top-level issue count in weekly report equals top-level issue count in the source tab
- issue titles match source tab wording, except for explicitly requested status updates
- nested detail lines are preserved under their parent issue

### Preserve the next section heading

When replacing a section body, never include the next heading paragraph in the deletion range. The safe range is:

- start: first paragraph after the current section heading
- end: `startIndex` of the next section heading

After editing, explicitly re-read and verify these heading styles:

- `Issues` = `HEADING_1`
- `Accomplishments` = `HEADING_1`
- `Pull Requests` = `HEADING_2`

This catches the failure mode where `Accomplishments` becomes body text after replacing `Issues`.

### Normalize mixed source numbering

`AIP Current Issues` may mix native Google Docs bullets with manual visible labels such as `4.` / `a.` / `b.`. When copying to the weekly report:

1. Treat native bullet nesting as authoritative where present.
2. For unbulleted lines, parse manual `^\d+\. ` as top-level and `^[a-z]\. ` as nested details.
3. Insert without visible manual labels, then use Docs `createParagraphBullets` with `NUMBERED_DECIMAL_ALPHA_ROMAN` so the weekly report has native `1 / a / i` structure.

### Verify visually, not only by export text

Drive text export can show the correct words while mobile Docs formatting is broken. For section replacement repairs, export the PDF and inspect the first affected page/contact sheet. Pass criteria:

- `Accomplishments` renders as a large heading parallel to `Issues`
- four source issues, when expected, render as four top-level numbered items
- nested details render as `a / b / c` under each item
- no placeholder remains in the edited section

### Metrics block placement

If Raymond says "for accomplishments" but the pasted content is clearly a metrics block (`📊 GLChat Weekly Report`, bug counts, performance report, GL AIP report), place it in `Key Metrics / OMTM`, not under `Accomplishments`. Preserve the supplied hierarchy/indentation and bold only headings/subheadings.

When terminal output shows mojibake for emoji, verify using UTF-8 byte decode or Docs/PDF rendering before assuming the document is corrupted; Drive export may still contain the correct emoji.
