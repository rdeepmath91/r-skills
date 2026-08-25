# Google Docs API — Index

This file is now an index so the skill stays split into small focused documents.

## Where to look
- `references/setup-and-dependencies.md` — minimum Python, OAuth, and external CLI setup by workflow
- `references/auth-and-setup.md` — OAuth credential creation, token refresh, revoke, and troubleshooting
- `references/operating-rules.md` — cross-cutting defaults, state boundaries, and anti-patterns
- `references/publishing-scope.md` — scope rules and cross-link rewriting
- `references/markdown-pipeline.md` — import/update behavior and code blocks
- `references/editing-in-place.md` — deterministic heading-based section edits, link rewrites, and image-only updates
- `references/mermaid-images.md` — Mermaid rendering and image placement
- `references/refresh-wrapper-pattern.md` — local wrapper pattern for repeated preview refreshes with project-specific layout rules
- `references/multi-tab-operations.md` — tab structure, listing comments via Drive API, deleting tabs
- `references/review-comments.md` — comment-thread handling
- `references/live-doc-promotion-and-page-audit.md` — preview-to-live promotion guardrails and PDF page-density/visual-occupancy audits
- `references/validation-workflows.md` — validation boundaries and minimum checks by workflow
- `references/reliability-and-timeouts.md` — API retries, timeouts, and large-doc handling
- `references/command-recipes.md` — copy/paste operational commands
- `references/table-and-element-limitations.md` — what the API cannot do with tables, TOC, page numbers, smart chips

## Why this is split up
- The top-level skill should stay short.
- Big one-file guides are harder to scan and easier to drift.
- Small topic files make it clearer which instructions are operational vs reference material.

## Rule of thumb
If you are about to write a long procedure, move it to a topic file and leave only the summary here.

## Reusable helper scripts
- `scripts/setup.py` — OAuth setup and readiness checks
- `scripts/docs_api.py` — create/update/read/export/headings/section-range operations
- `scripts/docs_table_tools.py` — inspect tables and insert rows by strict header/anchor matching
- `scripts/preview_post_refresh_audit.py` — structural audit after a refresh
- `scripts/render_pdf_contact_sheets.py` — contact sheets for page-by-page visual QA of exported PDFs
- `scripts/render_html_assets.py` — deterministic HTML -> tightly cropped PNG rendering for handcrafted diagrams
