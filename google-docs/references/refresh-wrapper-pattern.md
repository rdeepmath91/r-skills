# Refresh Wrapper Pattern

Use this pattern when a doc family needs repeated preview refreshes with the same deterministic layout rules.

This pattern is for **refresh mode**, not for small in-place edits to an already-polished live doc.

Do not use a preview refresh wrapper as a default live-promotion tool when the live doc has a preserved native formatting shell. Preview wrappers regenerate structure; polished live docs often need manual copy/paste or targeted in-place patches instead.

## When to use it

Use a local refresh wrapper when all of these are true:

1. the docs are regenerated repeatedly from local Markdown
2. the family has stable preview doc IDs
3. the family needs per-doc layout rules such as selected landscape sections or page-break preferences
4. you want deterministic refreshes without making the shared skill project-specific

Do **not** move project-specific heading names, preview IDs, or tab IDs into the shared skill. Keep those in the local wrapper.

## What belongs in the local wrapper

Keep only project-local values there:

- preview/live doc IDs
- source file paths
- `landscape` section ranges
- `page_break_before` heading lists
- any known per-doc image-width overrides for specific figure families

## What belongs in the shared skill

Keep only reusable behavior in the shared skill/reference set:

- markdown import sequence
- Mermaid/image insertion pattern
- bottom-up image insertion
- bottom-up orientation application
- code-block spacing normalization
- preview validation rules
- timeout/retry guidance

## Minimal wrapper config example

Prefer a data file (JSON/YAML) over hardcoding project values into the script.
A reusable wrapper can load this config at runtime and keep the script generic.

Starter files now included directly in this skill (self-sufficient baseline):
- `templates/refresh_doc.config.example.json`
- `templates/refresh_doc.wrapper.py`

Copy and adapt in your repo:

```bash
mkdir -p .tmp_gdocs_preview
cp <skill-root>/templates/refresh_doc.config.example.json .tmp_gdocs_preview/refresh_doc.config.json
cp <skill-root>/templates/refresh_doc.wrapper.py .tmp_gdocs_preview/refresh_doc.py
chmod +x .tmp_gdocs_preview/refresh_doc.py
```

Then run:

```bash
GDOCS_SKILL_ROOT=<skill-root> \
python3 .tmp_gdocs_preview/refresh_doc.py --config .tmp_gdocs_preview/refresh_doc.config.json --repo-root .
```

CLI contract notes (validated):
- `docs_api.py update <doc_id> --md <file>` is the supported markdown update command.
- `docs_api.py get <doc_id> --md` writes markdown to stdout (no `--output` flag).
- Wrappers should capture stdout and write local artifact files explicitly.

Config example:

```json
{
  "docs": {
    "architecture": {
      "doc_id": "<preview-doc-id>",
      "source": "docs/architecture.md",
      "landscape": [
        ["Architecture Drivers And Requirement Mapping", "Review Scope And Maturity"],
        ["Appendix A: Supporting Boundary Views And Flows", "Observability And Correlation Flow"]
      ],
      "page_break_before": ["Appendices"]
    },
    "requirements": {
      "doc_id": "<preview-doc-id>",
      "source": "docs/requirements-and-use-cases.md",
      "landscape": [
        ["Visual At A Glance", "Canonical Contract Invariants"]
      ],
      "page_break_before": [
        "Success Criteria And KPIs",
        "Functional Requirements"
      ]
    }
  },
  "live_link_map": {
    "architecture.md": "https://docs.google.com/document/d/...",
    "requirements-and-use-cases.md": "https://docs.google.com/document/d/..."
  },
  "shared_doc_link_map": {
    "https://docs.google.com/document/d/<old>": "https://docs.google.com/document/d/<new>"
  }
}
```

## Deterministic wrapper sequence

For each doc:

1. read canonical local markdown
2. strip the top title if the pipeline treats it as the doc title rather than body content
3. replace Mermaid/image lines with tokens
4. render diagrams locally
5. update the existing preview doc in place from markdown
6. wait for token anchors to appear in the imported doc
7. insert images from bottom to top
8. remove placeholder tokens
9. apply configured landscape sections from bottom to top
10. run code-spacing cleanup
11. export markdown/pdf/raw for verification
12. for long docs, generate contact sheets from the exported PDF and do a blocker/medium/cosmetic page audit

Reusable audit helper:

```bash
python3 <skill-root>/scripts/render_pdf_contact_sheets.py \
  --inputs /path/to/doc.pdf \
  --out-dir /tmp/page_audit_sheets
```

## Source-first fixes vs Docs-side fixes

Prefer source/content fixes when:

- a diagram is readable only if the labels are shorter
- a tall flowchart should become `LR` instead of `TD`
- a heading-only page exists because the heading lacks a short intro sentence
- a final page is nearly empty because a tiny note should be merged upward

Prefer local wrapper config when:

- a specific section repeatedly needs landscape
- the same headings repeatedly need page breaks before them
- the same doc family repeatedly has known page-flow expectations

Prefer Docs-side post-passes only when:

- the issue is a formatting artifact introduced by import
- the source should stay unchanged
- the operation is stable and low-risk (for example spacing normalization)

## Preview-to-live guardrail

Before pointing a wrapper at a live doc ID, confirm the user's intent:

1. If the user wants the live doc to look exactly like the preview and accepts losing manual live polish, a live refresh can be appropriate.
2. If the user wants to preserve title, TOC, page numbers, comments, section polish, or manually adjusted layout, do not live-refresh from Markdown by default.
3. If only a subset changed, promote by targeted in-place section edits or ask the owner to copy/paste approved preview sections manually.
4. After any live write, export the live PDF and run a page-by-page text + visual occupancy audit.

## Performance notes

What is usually slow:

1. Drive markdown import/update
2. waiting for imported token anchors to appear
3. uploading + permissioning + inserting each image
4. large paragraph-style post-passes

What is usually not the bottleneck:

- Mermaid rendering once the command is stable

## Hygiene / artifact retention

Wrappers often accumulate huge local artifacts and become hard to maintain.
Keep only:

- `rendered_preview_docs_v2/` (or one canonical render dir)
- `*_preview_latest.{md,pdf,raw.json}`
- current run logs needed for troubleshooting

Prune regularly:

- legacy render dirs (for example `rendered_preview_docs/`)
- duplicate `*_preview_current.*` snapshots
- one-off fitcheck/quickfix image dumps once validated

This cuts local clutter and avoids confusing old outputs with current state.

## Avoid these in wrappers

- hardcoding local-only paths into the shared skill
- top-down orientation application
- broad `deleteContentRange` cleanup against uncertain paragraph ranges
- republishing the whole live multi-tab doc when only one tab changed
- using project-specific heading names in the shared skill instead of the wrapper config

## Real-run validation checklist (before claiming wrapper is good)

Use a throwaway doc and run a full live API cycle once:

1. Create a temporary doc with `docs_api.py create`.
2. Run the wrapper update pass against the real doc ID.
3. Export markdown with `docs_api.py get <doc_id> --md` and verify expected anchors/content.
4. Delete the throwaway doc (Drive delete) and verify `docs_api.py get` returns 404.

Why this matters: compile/help smoke catches syntax and CLI shape, but only a live run catches command wiring and API-contract drift.

### CLI contract notes (easy to get wrong)

- `docs_api.py update` uses `--md` (not `--md-file`).
- `docs_api.py get --md` writes markdown to stdout; if you need a file, capture stdout and write it in the wrapper.
