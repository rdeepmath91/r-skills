# Validation Workflows

Use this reference when deciding what must be checked before calling a Google Docs task done.

## Validation Boundaries

Keep these checks separate in status reports:

| Boundary | Proves | Does not prove |
| --- | --- | --- |
| Setup readiness | interpreter, dependencies, OAuth scopes are usable | document content is correct |
| Source alignment | local Markdown/source and generated doc structure match | live doc layout is readable |
| Docs structure | headings, tables, links, images, tabs, styles, and orientation landed | PDF export has no visual defects |
| PDF/visual artifact | pages are readable, not blank, and not visibly broken | GitHub PR contains the source changes |
| Human editor review | Google Docs editor surface looks acceptable to the owner/reviewer | source or live docs were updated unless separately verified |
| Semantic/content review | wording, terminology, and decisions are correct | Docs API formatting is stable |
| PR/source state | commit and push include intended source files | direct live edits happened |
| Organization publication baseline | organization-specific shell, naming, TOC, page-number, orientation, figure-placement, and reporting conventions meet that baseline | semantic/product correctness or PR/source state |
| Skill integrity | skill scripts compile and runtime path is correct | a specific document was updated |

Do not claim one boundary from another. Example: a clean live PDF audit means the live doc renders cleanly; it does not mean the PR branch was pushed.

For layout-sensitive publication work, make the human editor review explicit in the handoff. State whether it is pending, passed by the user, or explicitly skipped by the user.

## Setup Readiness

Run before any API write in a new environment or after dependency/auth errors:

```bash
python3 <skill-root>/scripts/setup.py --check
```

If packages are missing, use `references/setup-and-dependencies.md` and install into the selected virtualenv, not an externally managed system Python.

## Markdown Publish Or Refresh

Minimum structural checks:

1. headings survived import with the expected mapping
2. tables survived import
3. lists kept ordered/unordered semantics from source
4. links do not point to stale `.md` paths when published Docs URLs are expected
5. code blocks follow the chosen mode: native Code Blocks from Drive import/placeholders, or explicitly accepted styled code panels
6. when native Code Blocks are required, `\ue907` marker/block count matches expectations before/after edits
7. inline image count matches expected rendered assets
8. plain-text/PDF output has no visible raw Markdown artifacts such as image links, `|---|` separators, raw fences, placeholders, duplicated front matter, or literal `**` / table-pipe syntax in email-style memos
9. plain-text/PDF output has no visible raw Markdown artifacts such as image links, `|---|` separators, raw fences, placeholders, or duplicated front matter

Useful commands:

```bash
python3 <skill-root>/scripts/docs_api.py get <doc_id> --md
python3 <skill-root>/scripts/docs_api.py get <doc_id> --raw --fields '<narrow-field-mask>'
python3 <skill-root>/scripts/docs_api.py export <doc_id> --format txt > /tmp/doc-visible.txt
python3 <skill-root>/scripts/preview_post_refresh_audit.py --docs name=<doc_id>
```

Treat Markdown export as a source-alignment artifact, not final visual proof. Native Google Docs headings, images, tables, and code blocks are serialized back into Markdown syntax by `--format md`, so visible-text export, raw Docs structure, PDF export, and contact sheets are required for polished publication claims.

## Diagram And Image Validation

Check both structure and render quality:

1. no raw Mermaid fences, HTML source, image placeholders, or private glyph artifacts remain
2. `inlineObjects` contains the expected images
3. for docs with an organization publication baseline, apply that baseline's figure/page checks; for GDP Labs docs, use `references/gdp-labs-publication-baseline.md`
4. presentation-grade diagram assets are assumed style-approved before insertion; this workflow validates only their Google Docs placement, sizing, orientation, and inserted-view readability

For long docs, use contact sheets instead of only spot checks:

```bash
python3 <skill-root>/scripts/render_pdf_contact_sheets.py --inputs /path/to/doc.pdf --out-dir /tmp/page_audit_sheets
```

## Preview QA

Use `references/preview-validation.md` for general layout rules. If the target has an organization publication baseline, also apply that baseline. For polished GDP Labs docs, use `references/gdp-labs-publication-baseline.md`.

Before spending time on PDF export, image fit, or page-level layout, verify preview identity against the requested source package:

1. read the preview title and headings with `docs_api.py headings <doc_id>` or a narrow Docs API read
2. compare the preview title/headings to the supplied Markdown/source headings
3. check expected inline image count when diagrams/assets are part of the package
4. if the preview is clearly unrelated or stale, stop and report a source/preview mismatch instead of continuing layout claims

At minimum, verify:

1. source and preview match in structure and order
2. organization publication-baseline checks apply when relevant; GDP Labs docs use `DOC1-DOC8` from `references/gdp-labs-publication-baseline.md`
3. report non-DOC preview findings using the severity table below

Classify findings:

| Severity | Examples | Required action |
| --- | --- | --- |
| Blocker | blank page, unreadable diagram/table, wrong orientation | fix before handoff |
| Medium | orphan heading, split table/code, highly sparse carry-over page | fix unless tradeoff is documented |
| Cosmetic | mild underfilled page or readable awkward break | fix only if it affects review confidence |

## Organization-Specific Publication Baselines

Keep organization-specific shell and reporting rules out of the general workflow unless the target doc belongs to that organization.

- For polished GDP Labs docs, use `references/gdp-labs-publication-baseline.md` and report findings with `DOC1-DOC8` labels.
- For non-GDP docs, use the general validation boundaries above unless the user provides a different publication baseline.
- Do not duplicate org-specific details such as footer format, title-shell fields, or report labels in this general workflow file.

## Live Doc In-Place Edit

After the final live write:

1. re-read the target heading or tab range
2. confirm the edit happened exactly once or within the intended range
3. verify sibling tabs or unrelated sections were not touched when that matters
4. export the live PDF if formatting, page breaks, section breaks, images, large sections, or trailing paragraphs changed
5. audit PDF pages using text density plus visual occupancy

For preview-to-live missing-section promotion, also verify:

1. source/preview headings expected in live are present
2. inserted ranges contain only the expected promoted headings
3. heading-style pollution did not turn inserted body paragraphs into headings
4. code/table/list formatting is native Docs formatting, not literal Markdown syntax

## Review Comment Validation

Before replying to or resolving comments:

1. identify whether the reviewer commented on source, preview, or live doc
2. verify the exact surface has the fix
3. verify the linked/commented section still exists and is readable
4. only then post the reply or resolution

## PR And Source Validation

Use Git validation separately from Docs validation:

1. check worktree state
2. confirm intended source files are committed
3. confirm branch tracking and remote push state
4. confirm the open PR uses the branch you pushed

Do not report live Docs updates as PR updates unless the source changes were committed and pushed.

## Final Source/Live Content Drift Check

Use this after repeated direct live edits to polished docs, especially before merging the source PR or sending stakeholder links.

1. Run the normal source/live heading and marker verifier.
2. Add a normalized body comparison against the PR/source Markdown for the docs being sent.
3. Ignore expected live-only shell content such as title page, version-control table, native TOC, page numbers, and Docs-only link anchors.
4. Ignore rendered diagram source when Mermaid/HTML was intentionally converted to images.
5. Do not ignore prose/table/code wording drift. Patch live text back to source when a paragraph differs only because of older wording or a partial previous edit.
6. Add exact critical-marker checks for the user's explicit request items, for example required section headings, API paths, event names, or terminology.
7. Report expected differences separately from real drift. Expected differences include formatting, pagination, code-panel styling, Google Docs anchors, and live-only metadata.

This check prevents subtle live/source divergence such as split words around section breaks, stale cross-reference prose, older wording that survived in live, or punctuation mismatches in stakeholder-visible sections.

## Skill Integrity Validation

Run after editing this skill:

```bash
python3 -m py_compile <skill-root>/scripts/*.py <skill-root>/templates/*.py
for s in setup.py docs_api.py docs_advanced.py docs_table_tools.py publish_pipeline.py preview_post_refresh_audit.py render_html_assets.py render_pdf_contact_sheets.py; do
  python3 <skill-root>/scripts/$s --help >/tmp/help_$s.txt
done
```

If a script lacks a no-side-effect `--help` path, add it before calling the skill ready. After compile/help checks, remove generated `__pycache__/` directories before committing or syncing.

When both local and repository/PR copies of the skill exist, do not assume sync from commit history. Compare the file trees byte-for-byte while ignoring `__pycache__/` and `.pyc` artifacts; only report "synced" when there are no local-only, repo-only, or content-different files. If local has newer durable best practices, copy those specific files into the PR copy, rerun reachability + script checks, commit, push, and re-check parity.

When both Hermes and OpenCode expose the skill, also verify the OpenCode path resolves to the Hermes skill directory and file parity is preserved.

## Real API Smoke Test

Use this only when script wiring changed or auth behavior is uncertain:

1. create a throwaway doc with `docs_api.py create`
2. update it with a tiny Markdown file
3. read it back with `docs_api.py get --md`
4. delete or trash the throwaway artifact according to workspace policy
5. rerun read and confirm expected not-found behavior

If any smoke-test step fails, fix the setup or script wiring before touching important docs.
