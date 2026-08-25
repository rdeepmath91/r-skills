# Native Code Blocks in Google Docs

Use this reference when a user asks to add, preserve, or validate Google Docs native Code Blocks in an existing polished document.

## Bottom line

There are two separate capabilities:

1. **Create native Code Blocks from Markdown import** — works through Google Drive import/update.
2. **Create a new native Code Block at an arbitrary insertion point with Docs API** — not supported by the public Docs API.

Docs API can edit/fill an already-created native Code Block. It cannot reliably create a brand-new native Code Block in normal existing text.

## Public API reality

The public Google Docs API discovery schema exposes requests like `insertText`, `updateTextStyle`, `updateParagraphStyle`, `insertTable`, `insertInlineImage`, and related structural edits. It does **not** expose:

- `insertCodeBlock`
- a `codeBlock` structural element
- a paragraph style that turns text into a native Code Block
- a text style that turns text into a native Code Block
- a public range-copy request from one Google Doc into another

Apps Script documentation also does not expose a public `CodeBlock` element type. Apps Script copying may still be worth an experiment, but treat it as unproven.

## Native Code Block structure observed through API

Imported/native Code Blocks currently appear through the Docs API as normal paragraphs/text runs with private/internal markers:

- native block boundary marker: `\ue907`
- marker is in the Unicode Private Use Area
- first code paragraph may start after or near a `\ue907` marker
- closing boundary may appear as a marker-only paragraph or prepended to the following normal paragraph
- syntax highlighting appears as many token-level `textRun`s with colors
- code text commonly uses `Roboto Mono`, usually `9pt`

Do not treat `\ue907` as a public contract. It is useful for validation/counting, not for creation.

## Verified behavior from probes

### Drive Markdown import creates native Code Blocks

Probe:

1. Upload Markdown as `text/markdown` with target MIME `application/vnd.google-apps.document`.
2. Include a fenced Markdown block:

````markdown
```python
PLACEHOLDER_CODE_LINE
print('kept')
```
````

Observed:

- resulting Doc contained `\ue907` native markers
- code text used `Roboto Mono` 9pt
- code block context existed before any Docs API edit

### Whole-doc Drive update from Markdown also creates native Code Blocks

Drive `files.update` / upload to an existing Google Doc ID with Markdown can replace the document body while preserving the file ID/URL and creating native Code Blocks.

Use only for drafts/previews or when the user explicitly accepts replacement risk. It can reset or break:

- manual page/layout polish
- native TOC shell
- page numbers
- headers/footers
- section orientation
- comments
- heading IDs
- links that target existing heading anchors
- manual table/image/spacing fixes

For a live-doc replacement that needs native Code Blocks and images/diagrams:

1. Build a single canonical Markdown source with fenced code blocks and explicit image placeholders such as `DIAGRAM_ANCHOR_*`.
2. Create or update a preview doc via Drive Markdown import first.
3. Replace image placeholders in the preview with uploaded/inserted images using the Docs API helper, then validate that placeholders are gone and inline image count matches expectation.
4. Validate preview content before touching live: native marker count, expected snippet text, banned wording absent, heading/anchor placeholders absent.
5. Only after user approval, run the same Markdown update against the live doc ID and repeat image placeholder replacement.
6. Re-run the same validation on live, and also check Drive comments/replies state when comment preservation or resolution status matters. Whole-doc update may disturb comment anchors even if comment threads still exist.

This preview-then-live replay pattern is safer than hand-editing live first because it proves the Markdown import creates native Code Blocks and gives you a deterministic validation checklist before accepting the replacement risk.

### Docs API can edit inside an existing native Code Block

Probe:

1. Drive-import Markdown with a fenced code block containing `CODE_BLOCK_PLACEHOLDER`.
2. Locate the placeholder with Docs API.
3. Replace only the placeholder using `deleteContentRange` + `insertText`.

Observed:

- native marker count stayed unchanged
- replacement text appeared inside the existing native block context
- multiline replacement also worked
- inserted multiline text retained Roboto Mono 9pt context

This is the key practical workaround.

### Docs API inserted fenced text does not convert

Probe:

1. Create a normal Google Doc.
2. Insert this text with `documents.batchUpdate().insertText`:

````markdown
```python
print('new via api')
```
````

Observed:

- native marker count stayed `0`
- literal backticks remained plain text
- no native Code Block was created

### Docs API inserted private markers are stripped

Probe:

1. Insert `\ue907print(1)\ue907` with `insertText`.

Observed:

- native marker count stayed `0`
- final visible text was only `print(1)`
- private marker was stripped by the API/import layer

### Docs API read-and-recreate transfer does not preserve native Code Blocks

Probe:

1. Drive-import a Markdown snippet doc so Google creates a real native Code Block.
2. Read the source paragraph/text-run structure through Docs API.
3. Insert the exposed text, including `\ue907`, and reapply matching text styles into a separate target doc.

Observed:

- source contained `\ue907` markers and syntax-token text runs
- target ended with `0` `\ue907` markers because `insertText` strips Private Use Area characters
- target became a styled monospace panel, not a native Code Block

Do not implement “copy code block from doc A to doc B” by reading Docs API structure and recreating it. Public Docs API has no range-copy operation that preserves this internal structure.

### Whole-file copy preserves native Code Blocks

Drive file copy of a Google Doc preserves native Code Blocks because it duplicates the document file itself. This is different from copying content into another existing doc. Whole-file copy is useful for preview/simulation, but it does not solve targeted insertion into a polished live doc.

## Supported workflows

### A. API-only, template-driven: native placeholders

Use this when the doc family can be templated.

1. Create/import a polished shell with native Code Block placeholders.
2. Use stable placeholder text, e.g. `CODE_BLOCK_PLACEHOLDER_001`.
3. Keep each placeholder inside a real native Google Docs Code Block.
4. Later, locate placeholder text with Docs API.
5. Replace only the placeholder range with the target code.
6. Validate:
   - expected placeholder is gone
   - expected code exists
   - native marker count is unchanged
   - surrounding title/TOC/page-number/layout shell remains intact

This is the safest API-based way to “add” code content while preserving native Code Block behavior. It requires preallocated slots.

### B. API-only, arbitrary insertion: styled code panels

Use this when there is no existing native placeholder and no UI/manual step is allowed.

- Insert the code as text.
- Apply readable styling: shaded paragraph/table cell, `Roboto Mono`, 9pt, compact spacing.
- For code paragraphs, set `spaceAbove=0pt`, `spaceBelow=0pt`, and `lineSpacing=100` so the block does not look like loose prose.
- When matching an existing preview/live style, inspect the preview first. Some previews use compact monospace paragraphs without native Code Block markers or shading; in that case match the preview style instead of adding a new gray panel that changes the visual language.
- For polished live docs, prefer targeted code-paragraph restyling over whole-doc reimport when only code styling regressed. Whole-doc reimport can reset typography passes, diagram placement, captions, comments, headings, and recent wording fixes.
- Apply paragraph shading as well as monospace text styling when the target style uses shaded panels; plain monospace text without a shaded panel is usually not visually acceptable in polished docs unless it is intentionally matching the approved preview.
- For before/after examples, keep the call shape identical when the product behavior is auto-detection rather than API change. Change only the meaningful value, such as `github_skill = ".../skills/<skill-name>"` before and `github_skill = ".../skills"` after, while preserving `skills=[github_skill]`.
- Do not claim it is a native Google Docs Code Block.
- Report the limitation in handoff if native Code Blocks were requested.

### B2. Repairing flattened code styling in polished live docs

Use this when a live Google Doc has already been polished and only the code-looking paragraphs regressed, often after a global font/readability pass.

1. Compare the live doc against the approved preview by reading raw Docs structure, not only visual PDF output:
   - count native private markers (`\ue907`) in both docs
   - inspect fonts on code-like paragraphs (`Agent(`, `skills=[`, import snippets, indented code lines, etc.)
   - check whether the preview is actually native Code Block or just monospace styling
2. If the preview has no native markers and only uses monospace paragraphs, do **not** reimport the whole live doc just to fix code styling.
3. Patch only the code-like paragraph ranges in the live doc:
   - set `weightedFontFamily` to `Roboto Mono` or the preview's monospace font
   - preserve the user's minimum readable size target when one exists, unless the preview explicitly uses smaller code
   - set compact paragraph spacing (`spaceAbove=0pt`, `spaceBelow=0pt`, `lineSpacing=100`)
   - include all lines in the block, not only the first/most distinctive line: opening call, arguments, closing parens/braces, assignment lines, and indented lines
4. Avoid whole-doc Drive Markdown reimport/update unless native Code Blocks are explicitly required and the user accepts live-polish replacement risk.
5. Export PDF and visually compare the repaired live page to the preview page before handoff. Check for gray highlight artifacts, clipping, overflow, page-count changes, and large gaps.

### C. Whole-doc Markdown import/update: drafts and previews only

Use this when regenerating a draft/preview from source Markdown and losing live polish is acceptable.

- Keep fenced Markdown code blocks if native Code Blocks are desired.
- After import/update, inspect marker count or visual export.
- Do not use this directly against polished live docs unless the user explicitly approves replacement risk.

### D. Browser/UI automation: promising but not yet productized

Use only as an experiment or with explicit user approval.

Options:

1. **Direct editor command**
   - open target doc in a logged-in browser
   - insert/select code text
   - apply Google Docs UI Code Block command/building block
   - verify marker count increased

2. **Snippet-doc copy/paste**
   - Drive-import a temporary Markdown snippet doc with native Code Blocks
   - open snippet and target docs in Google Docs UI
   - copy native Code Block from snippet
   - paste into target insertion point
   - verify marker count increased
   - trash snippet doc

This is the most plausible way to insert brand-new native Code Blocks into already-polished docs without whole-doc replacement, but it depends on browser session stability and UI behavior.

### E. Manual editor pass

Use when native Code Blocks are required and automation is too risky.

- Use API for safe text/structure updates first.
- Leave clear markers/comments for code-block locations.
- Ask the owner/editor to apply native Code Block formatting in Google Docs UI.
- Verify after manual pass when possible.

## Decision table

| Requirement | Recommended path |
| --- | --- |
| New draft doc from Markdown, native Code Blocks desired | Drive Markdown import with fenced blocks |
| Existing polished doc, preallocated code slots exist | Fill native placeholders with Docs API |
| Existing polished doc, arbitrary new native block required | UI automation experiment or manual editor pass |
| Existing polished doc, API-only required | Styled code panels, not native Code Blocks |
| Existing live doc can be fully replaced | Drive `files.update` from Markdown, with explicit user approval |

## Validation checklist

Before calling a doc publication-ready when code blocks matter:

- [ ] Decide whether native Code Blocks are required or styled code panels are acceptable.
- [ ] If native placeholders are used, verify expected placeholder count before edit.
- [ ] After edit, verify placeholder text is gone and expected code text exists.
- [ ] Verify native marker count (`\ue907`) is unchanged for placeholder-fill workflows, or increased by expected amount for UI/manual insertion workflows.
- [ ] Verify code text remains monospace (`Roboto Mono` / equivalent) and compact enough in PDF/contact sheet.
- [ ] If whole-doc Markdown replacement was used, explicitly confirm the user accepted live-polish reset risk.
- [ ] Report any manual/UI steps still required.

## Policy

- Do not retry impossible pure-Docs-API creation paths once this reference applies.
- Do not insert raw `\ue907` markers as a conversion strategy.
- Do not read native Code Blocks from one doc and recreate them in another with Docs API `insertText`; the marker is stripped and native structure is lost.
- Do not tell users that fenced Markdown inserted with Docs API will become native Code Blocks.
- Do not use whole-doc Markdown replacement on polished live docs unless explicitly approved.
- Prefer native placeholders for repeatable doc families.
- For arbitrary new native blocks, choose UI/manual workflows or styled-panel fallback.
