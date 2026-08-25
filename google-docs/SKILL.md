---
name: google-docs
description: Create, edit, and publish Google Docs with professional formatting, tables, and internal links using natural language.
---

# Google Docs Skill

Use this skill for Google Docs publication, refresh, formatting repair, tabbed-doc updates, preview-to-live promotion, validation, and review-comment follow-up.

## Canonical OAuth profile and helper

For Google Docs tasks, use `/home/raymond-christopher/.hermes` as the canonical OAuth profile and the helpers in this skill's `scripts/` directory. The current canonical profile has `https://www.googleapis.com/auth/documents` and `https://www.googleapis.com/auth/drive` scopes and is suitable for Docs and Drive operations.

Do not use the broad `productivity/google-workspace` helper for a Docs-only task: that helper requests unrelated Gmail, Calendar, Sheets, and Forms scopes, which can cause a valid Docs token to fail refresh with `invalid_scope`.

Keep alternate profile directories intact unless explicitly asked to retire them. They are not candidates for automatic profile selection because their refresh tokens may be expired or revoked.

## Defaults

- Work from the user-named worktree or canonical checkout; do not silently switch trees.
- Publish only the Markdown subtree or doc family the user asked for.
- If the user asks to sync finalized PR/source Markdown into existing live Google Docs, compare source against live first, create/update previews for changed docs, and only promote previews that pass structure + visual validation. Use `references/multi-doc-pr-preview-to-live-sync.md`; do not live-sync multi-doc packages blindly.
- For any requested edit to a live doc, use a preview first: reuse the stable preview for that live doc when one exists, or copy the current live doc to create one when there is no reusable preview.
- For recurring/shared report templates such as monthly AIP/DX reports, “help me fill this doc” means create a copy/preview and fill that copy unless the user explicitly says to edit the live/original doc. These docs often have manual formatting that section replacement can damage.
- For email-style memos and plain business notes, keep the live result plain and readable: selective bold labels, normal prose, real hyperlinks, and no visible markdown tables or literal `**` / `|` / `#` markers in the rendered doc.
- For recurring/shared report templates such as monthly AIP/DX reports, “help me fill this doc” means create a copy/preview and fill that copy unless the user explicitly says to edit the live/original doc. These docs often have manual formatting that section replacement can damage.
- When the user asks to “improve,” “review,” “suggest,” “draft,” “fill,” or “what should change” in a live Google Doc, do not edit the doc directly unless they explicitly say to apply/update/edit the live doc. Provide a draft change list, separate Markdown draft, or copied preview first.
- If the user wants an opinion or review of a live Google Doc, inspect the doc comments/review state before answering when comments may be relevant. Do not say you reviewed inline or thread comments unless you actually fetched them.
- For a repository-grounded architecture review, read the target Doc first, then trace each claimed layer through the named codebases before suggesting changes. Distinguish clearly between current SDK/library behavior, backend/runner behavior, and proposed architecture. State whether the inspected checkouts are current with their tracked remotes; do not present a proposed remote-execution mechanism as an existing platform capability. Return a paste-ready bounded section and recommendation list, leaving the live Doc untouched unless explicitly asked to edit it.
- For technology sections in weekly reports or similar doc families, research current official sources first, then show alternatives before inserting any final text. Keep items short: title + URL reference, with only a one-line note if needed. See `references/weekly-report-technology-section.md`.
- Apply and validate edits in the preview, then stop at an explicit approval gate before copying anything to the live/original doc. A user saying “feel free to create a clone before refreshing” approves clone creation only; it is not approval to promote preview changes live.
- Prefer preview docs before live updates for structure-heavy, layout-sensitive, or multi-doc changes; direct live edits are only acceptable for trivial, low-risk text/link fixes or when the user explicitly asks to skip preview. If the preview exists because the user has not yet approved live changes, update the preview only and state that live was not touched.
- Keep one current reusable preview per live doc by default; do not create timestamped preview copies for every experiment unless isolation is required.
- In previews, cross-doc links should point to canonical live docs by default; preview links are allowed only for an explicit unpublished-doc-family review.
- Same-doc section references should use heading/bookmark links where practical, but regenerate or revalidate those anchors after live promotion because preview anchors are not final live anchors.
- Before final handoff, run link hygiene checks: no preview doc IDs in live docs, no trashed-doc IDs, no raw `.md` links, and no unlinked same-doc references where links are expected.
- Treat obvious large vertical gaps as layout defects even when PDF sparse-page checks pass; normalize heading/list/record spacing before live promotion.
- For boss-facing architecture/layering/comparison docs, prefer a horizontal or side-by-side layout when it improves scanability. See `references/horizontal-layering-format.md` for the compact table pattern.
- If the user points to a reference doc for "good formatting and diagrams," mirror that document's visual framing first, then adapt the wording. Do not preserve a stacked layout if the reference clearly uses a broader horizontal composition.
- **Reference-driven architecture diagrams:** before adapting a referenced Google Doc, retrieve its text *and* inspect every embedded image. When Drive export is unavailable but the Docs API can read the doc, call `documents.get(includeTabsContent=True)`, inspect `documentTab.inlineObjects` for every tab, and fetch each `imageProperties.contentUri` with the same authorized credential in memory. Do not print image URLs, OAuth values, or secrets.
- Build a semantic mapping before redesigning: identify the outer environment boundary, ingress/control plane, agent/runtime location, dependency placement, isolation boundary, event/result return path, and the meaning of every numbered option. A new hybrid or policy-routing diagram is a departure unless those concepts and option meanings are explicitly preserved; never describe it as continuity by implication.
- For Raymond's boss-facing architecture diagrams, keep the figure to **simple labelled boxes and connected arrows**. Put policy rationale, risks, dependency inventories, and caveats in numbered Markdown/Doc text immediately after the image. Use numbered lists for objectives and other scanable lists, with selective bold emphasis rather than long diagram text.
- Keep a local Markdown companion draft during iterative doc work when it helps review or reuse; state the absolute path so the user can open it directly, and keep it in sync with the current live/preview direction.
- When promoting one section from a local Markdown/audit draft into a live Google Doc, explicitly name the exact section heading, target placement, and what will be excluded before editing. If the user asks to proceed, insert only that reader-facing section, not the whole audit. Keep a visible reminder in the local MD of: source Google Doc URL, local full-draft path, and the exact section intended for live insertion.
- For PM/stakeholder follow-up sections derived from technical audits, strip code paths, GitHub line links, class/function names, and implementation-heavy proof from the live section. Use Docs-native heading styles, normal prose, selective bold labels, and bullets; keep detailed evidence in the local companion MD unless explicitly requested.
- For PM-facing follow-up sections, do not use generic bullet glyphs when the user wants structured scanability. Use explicit numeric or lettered labels for detail lists, start with a short `Summary`, then put `Details`, implication/remaining-risk sections, and a follow-up plan. If the Markdown draft has a follow-up table, create a native Google Docs table with numbered rows and bold header cells; do not leave a markdown-looking table in the live doc. Validate the exported section has no `*`/`-` generic bullets and that table rows are visible after insertion.
- For PM-facing skill/runtime follow-up sections, avoid `skill migration` when the customer already has working skills in another runtime such as OpenCode. Prefer `existing skill compatibility validation`, `existing skill reuse in AIP`, or `OpenCode-to-AIP skill compatibility` unless the work is truly a rebuild/migration. See `references/pm-followup-section-compact-formatting.md`.
- After inserting or replacing a Docs section, inspect raw paragraph styles for inherited `spaceAbove` values such as `24pt`; this often creates huge vertical gaps in the editor. Do not overcorrect to zero-spacing. Match the rhythm of nearby approved content first, remove only genuinely empty paragraphs, restore selective bold labels, and export/render PDF contact sheets for visual QA. If the section starts awkwardly mid-page, prefer a clean page break before the section over collapsing all spacing. See `references/pm-followup-section-compact-formatting.md`.
- For email-style memos and plain business notes, use plain prose with selective bold labels and real hyperlinks; do not leave visible markdown tables or literal `**`, `|`, or `#` markers in the rendered doc.
- Use the starter template in `templates/email-announcement-format.md` when you need a quick plain-email draft shape.
- Automated Docs/API/PDF audits are not final publication approval. For layout-sensitive docs, stop at a named human review gate after preview validation and ask the user/owner to inspect the Google Docs editor view before promoting to live.
- Preserve stable live doc IDs, URLs, tab IDs, native title/TOC/page-number shell, comments, and manual polish unless the user explicitly accepts replacing them. When source/PR Markdown must update a polished live doc, prefer a live-derived copy and in-place body-range patch over a fresh import; see `references/live-doc-style-assimilation.md`. For large or table/list/image-heavy docs, patch bounded sections incrementally and validate each class of content; do not assume whole-body structural cloning through the Docs API will preserve list numbering, tables, diagrams, or TOC correctness. See `references/live-derived-section-patch-previews.md`. If the user asks whether previews can be copied seamlessly into live later, test one small section first in a live-derived copy and avoid broad style overlays until PDF/contact-sheet QA proves they do not corrupt inline code, links, or numbered lists.
- For executive summaries and comparison appendices, prefer short high-level bullets only where they improve scanability; avoid long vertical bullet stacks for details that read better inline or in tables. When the user asks for bold/italic/formatting guidance, provide a separate Markdown draft with explicit emphasis choices instead of silently applying them. In polished executive docs, bold labels and key phrases only; avoid bolding whole recommendations, whole bullets, or full paragraphs.
- When the user wants list-style content in a Google Doc to be numbered, verify the rendered PDF shows real `1, 2, 3...` sequencing. If the Docs helper produces repeated `1.` auto-list markers or bullet dots, replace the section with explicit numbered text and `--no-simple-lists`, then export and visually re-check.
- For weekly-report cleanup specifically, use `references/weekly-report-pruning.md` as the narrow pattern: prune stale PR rows from the live doc, do not reformat the section, and verify the removed PR numbers are absent afterward.
- When the user says a Google Doc message/text is too small, treat it as a readability-and-content issue, not only a font-size issue: simplify wording first, enlarge body text conservatively, then re-export/contact-sheet QA because font and spacing changes can create orphan headings, split lists, or sparse extra pages.
- When the user asks to make a section more concise and fit it into one page, reduce structure before reducing font size: collapse multi-subsection explanations into one short opener, one compact table, and a few bullets; remove redundant examples/appendix detail from that section; then export a PDF and verify the section's start/end pages so you can confirm it truly fits on one page without creating blank pages or clipping elsewhere.
- For boss-facing documents that compare implementation formats or alternatives, structure the document as: summary first, one GDP Labs-style diagram per alternative, comparison table next, then details/implementation notes below. Do not bury the decision frame after the technical explanation.
- When the user asks for an executive-only/boss-facing preview, remove implementation-note, success-criteria, and technical-detail sections unless explicitly requested. Final QA should verify the exported PDF page count, no trailing blank page, no orphan technical section, and any requested numbered list renders as visible `1, 2, 3` without bullet dots.
- Keep code examples compact and Google Docs-compliant: prefer Drive Markdown import for native code blocks when regenerating a draft/preview, then run `docs_advanced.tighten_code_block_spacing(doc_id)` and validate visually so code blocks do not have excessive paragraph spacing.
- For before/after implementation snippets, preserve the documented caller pattern unless the user asks to change it. If the requested improvement is runtime auto-detection, the `After` snippet should often keep the same call shape and change only the variable value (for example `github_skill = ".../skills"` while keeping `skills=[github_skill]`).
- Keep local Markdown, preview docs, live docs, and PR branches as separate states; direct live edits do not update GitHub until source changes are committed and pushed.
- For risky live edits, first simulate the exact operation on a fresh copy of the current live doc. This includes structural table edits, section orientation changes, header/footer/page-number changes, TOC-adjacent changes, image/diagram placement, large style-range updates, and same-doc anchor/link regeneration. Promote only after the simulation export and raw-structure checks pass. Never use first-substring table matching such as "first table containing Time"; match tables by exact header cells.
- After a global font/readability pass on a polished live doc, explicitly audit code-like paragraphs because broad text-style updates can flatten monospace snippets into body prose. If the approved preview used compact monospace but not native Code Blocks, repair only those paragraph ranges and visually compare the exported live page to the preview instead of reimporting the whole document.
- Use the standard phase order: setup -> scope -> content -> diagrams/assets -> fit/orientation -> spacing/styles -> validation -> handoff.
- When the user asks for a proper/polished Google Doc from Markdown, do not merely paste or plain-populate raw Markdown. Use Drive Markdown import/update for native headings/tables/lists/code blocks, render diagrams as images, then run post-import polish and visual validation. See `references/polished-markdown-doc-publication.md`.
- For email-style memos or plain business notes, do not rely on markdown-looking tables or visible markdown markers in the final doc. Use plain prose, selective bold labels, and real hyperlinks instead.
- For Markdown-first docs where native tables/lists/code blocks matter, use Drive Markdown import/update; for memo-style docs, prefer plain paragraph formatting and targeted Docs styling instead of a markdown-shaped draft.
- For GDP Labs formatting targets, treat validation as mandatory: run validation loops and iterate autonomously when fixable; escalate to the user only when a decision is required (tradeoff, ambiguity, or policy/approval boundary).
- When removing stale items from a live Google Doc report, read the live document first, identify the exact paragraph ranges for the unwanted lines, and delete them from bottom to top with `deleteContentRange` so indices do not shift. Re-read the doc immediately after the edit and confirm the lines are gone before reporting success.
- For weekly-report style cleanup, keep the target section narrow: remove only the obsolete PR lines, preserve surrounding section headings and unrelated entries, and verify the edit by searching the live doc for the deleted PR numbers afterward.
- In doc QA, treat "closed/merged test PRs still listed" as a stale-data problem, not a formatting issue: prune the rows/paragraphs from the live doc rather than hiding them with commentary.
- For live tabbed daily-tracking docs updated from GitHub evidence, inspect `includeTabsContent=true` and reuse the existing blank/current top section instead of appending a markdown block. Preserve the tab's native heading, numbered-list objects, spacer paragraphs, and PR link runs; replace a stale date chip only after reading the raw paragraph structure, and verify by re-exporting the same tab. When the scope is sandbox-only, filter evidence before drafting: distinguish `[Sandbox – E2B on AWS]` AIP Helm integration from deploying the AWS infrastructure itself, and include only PRs whose body/files explicitly cover E2B/OpenSandbox/sandbox runtime behavior. Label a merged PR `[MERGED]` unless a separate release/deployment signal is verified; do not upgrade it to `[RELEASED]` from merge status alone.

- For email-style memos or plain business notes, do not rely on markdown-looking tables or visible markdown markers in the final doc. Use plain prose, selective bold labels, and real hyperlinks instead.
- For Markdown-first docs where native tables/lists/code blocks matter, use Drive Markdown import/update; for memo-style docs, prefer plain paragraph formatting and targeted Docs styling instead of a markdown-shaped draft.
- For GDP Labs formatting targets, treat validation as mandatory: run validation loops and iterate autonomously when fixable; escalate to the user only when a decision is required (tradeoff, ambiguity, or policy/approval boundary).

## Minimum Setup (hand this to first-time users)

1. Python environment
   - Use a virtualenv (repo venv is fine). Do not install into system Python.
2. Required packages
   - `python -m pip install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib httplib2`
3. Google APIs + scopes
   - Enable Docs API and Drive API.
   - OAuth scopes: `https://www.googleapis.com/auth/documents`, `https://www.googleapis.com/auth/drive`.
4. Auth bootstrap
   - `python <skill-root>/scripts/setup.py --check`
   - If unauthenticated: run `--client-secret`, then `--auth-url`, then `--auth-code`.
5. Smoke validation
   - `python <skill-root>/scripts/docs_api.py --help`
   - `python -m py_compile <skill-root>/scripts/*.py`

Detailed setup and troubleshooting live in:
- `references/setup-index.md`
- `references/setup-and-dependencies.md`
- `references/auth-and-setup.md`

## GDP Labs compliance essentials

Use this before publishing anything marked as production-ready:

1. Start from `references/gdp-labs-publication-baseline.md`.
2. Run validation from `references/validation-workflows.md` (including visual/page audit when layout matters).
3. Follow guardrails in `references/operating-rules.md` (no silent live-doc replacement, keep IDs/tabs/shell unless approved).
4. For preview -> live promotion, use `references/live-doc-promotion-and-page-audit.md`.
5. Record what was validated and what was intentionally skipped in handoff notes.
6. Iteration policy: when checks fail and the fix is mechanical/safe, revise and re-run validation before handoff; when multiple acceptable outcomes exist or guardrails may be crossed, pause and ask the user to choose.

## Use-Case Router

| User intent | Start here | Also check |
| --- | --- | --- |
| First-time setup, missing packages, OAuth, environment readiness | `references/setup-index.md` | `references/setup-and-dependencies.md`, `references/auth-and-setup.md` |
| Publish or refresh Markdown into Google Docs | `references/publish-index.md` | `references/command-recipes.md`, `references/markdown-pipeline.md`, `references/polished-markdown-doc-publication.md` |
| Create a Markdown preview when helpers fail from limited Drive scope, or when Mermaid must become an inline image | `references/drive-file-scope-mermaid-preview-parity.md` | Load token stored scopes directly, Drive-import Markdown, render Mermaid to PNG, insert image at final size, then run source-parity and visual QA as separate gates |
| Create a polished/boss-facing Google Doc from Markdown with tables, code snippets, and diagrams | `references/polished-markdown-doc-publication.md` | Use Drive Markdown import for native formatting, render diagrams as images, tighten code spacing, then PDF/contact-sheet visual QA; for dense schema/table previews with Mermaid image insertion, live-style overlays, or split ERDs, see `references/markdown-preview-diagram-polish-case-notes.md` |
| Create or validate polished GDP Labs docs | `references/validation-index.md` | `references/gdp-labs-publication-baseline.md`, `references/operating-rules.md` |
| Create a quick researched comparison/list as a Google Doc with live links, prices, or options | `references/quick-research-brief-docs.md` | Use concise assumptions, filtered decision tables, volatile-price caveats, explicit preference-aware ranking, checked-but-excluded alternatives, and export/heading/tail cleanup verification before handoff |
| Edit one existing doc section, link family, image, or style range | `references/editing-index.md` | `references/editing-in-place.md`, `references/table-and-element-limitations.md` |
| Edit a comparison section so it is strong but non-adversarial | `references/neutral-comparison-section-editing.md` | Draft first unless explicitly told to apply live; preserve reviewer-requested headings and clarify terms like `replaces`; use boundary/ownership language, high-level bullets, and a simple concept diagram for executive readers |
| Preserve a polished live doc while adding approved preview/source content, or ensure preview content can be copied seamlessly into live later | `references/validation-index.md` | `references/live-doc-promotion-and-page-audit.md`, `references/live-doc-style-assimilation.md`, `references/live-style-shell-pr-sync.md`, `references/live-derived-section-patch-previews.md`; compare common heading `namedStyleType` values from `Executive Summary` downward and fix shifted preview heading levels before handoff. For polished docs, prefer live-derived bounded section patches over full imported-preview style overlays or whole-body structural cloning. |
| Recover after accidentally editing a live/shared Google Doc instead of a copy | `references/live-doc-accidental-edit-recovery.md` | Stop live edits, inspect Drive revisions by exported sentinels, restore from clean DOCX revision, then create the working copy |
| Work with multi-tab Google Docs | `references/editing-index.md` | `references/multi-tab-operations.md` |
| Render Mermaid, Graphviz, HTML, or local images | `references/publish-index.md` | `references/mermaid-images.md` |
| Repeated refreshes for a stable doc family | `references/publish-index.md` | `references/refresh-wrapper-pattern.md` |
| Preview QA, layout review, page audit, or final validation | `references/validation-index.md` | `references/preview-validation.md` |
| Reply to or verify Google Docs/Drive review comments | `references/validation-index.md` | `references/review-comments.md` |
| Handle timeouts, quota errors, flaky imports, or large docs | `references/setup-index.md` | `references/reliability-and-timeouts.md` |
| Change tables, TOC, page numbers, smart chips, or tricky structural elements | `references/editing-index.md` | `references/table-and-element-limitations.md` |
| Add or preserve Google Docs native Code Blocks | `references/editing-index.md` | `references/native-code-blocks.md` |
| Need direct commands or helper usage | `references/publish-index.md` | `references/command-recipes.md`, `references/api-lessons.md` |
| Extract a section from a live Doc to mirror formatting from a reference Doc | `references/editing-index.md` | Use `docs_api.py headings`, `section-range --heading`, and `export DOC_ID --format md` (doc ID is positional; not `--document-id`; format is `md`, not `markdown`) |
| Read/review a large Google Doc with embedded images | `references/command-recipes.md` | Export to a temp Markdown file first, then use search/read on targeted headings; direct terminal output can be swamped by base64 image data and truncate the useful sections. |
| Read a Google Doc when `docs_api.py export` fails with `invalid_scope` but the token has read-only Docs/Drive scopes | `references/read-only-token-doc-export.md` | Build credentials using the stored token scopes and Drive export directly; do not escalate to a write token for read-only review. |
| Read a Google Doc when the default Hermes token refreshes but the file returns `404` / no permission | `google-api-oauth-management` → `references/oauth-inventory-and-target-doc-access.md` | Audit project `.env` OAuth token families, decode base64 tokens in-process, test target file access with Drive `files.get`, and use the working token for read-only export without printing secrets. |
| Read a Google Doc when Drive metadata returns `404` but a configured full-scope token may still access it through the Docs API | `references/direct-docs-api-access.md` | Use `docs_api.py get DOC_ID --md` with the configured `HERMES_HOME`; treat a Drive `404` as a Drive visibility result, not proof that the Docs API cannot read the document. |
| Triage a Google Doc link that cannot be read because access may be private/unshared | `references/doc-access-denial-triage.md` | Check helper export, read-only token export, public export/sign-in behavior, and report Drive 404 as `not found or no permission` rather than deleted. |
| Review a live appendix/section and check whether diagrams were already improved in prior sessions | `references/appendix-review-and-prior-asset-check.md` | Export both Markdown/text and PDF, render the affected pages, then search session history for prior local diagram assets before saying whether improvements were attempted or promoted live. |
| Review a Google Doc and return paste-ready comment suggestions tied to exact sections/highlights | `references/editing-index.md` | `references/command-recipes.md`, `references/slide-outline-review-checklist.md`, `references/review-comments.md`; for comments that tag Raymond, list Drive comments first, filter unresolved @mention threads, read the quoted section, then create a manual comment pack unless asked to post. If the user provides a repo URL/reference, use `references/repo-grounded-doc-comment-review.md`: inspect the repo and keep final comments scoped to the tagged section/appendix unless the user broadens scope. |
| Check/improve a pasted security email or boss-facing response against a Google Doc finding and local repo evidence | `references/security-response-from-doc-and-repo-evidence.md` | Export the doc as Markdown, verify implementation/default claims in repo and git history, avoid secret values, and frame guard-disabling only as bounded compatibility/break-glass exception |
| Explain or troubleshoot Google Docs/Drive eSignature requests for Google Workspace users | `references/esignature-workflow.md` | Check plan/admin availability first; distinguish eSignature workflow from certificate-based digital signature |
| Review whether a Google Doc about an external AI platform/vendor is current and aligned with an internal stack | `references/vendor-stack-comparison-review.md` | Use `docs_api.py export DOC_ID --format md`; verify current vendor facts from official docs/news/pricing/model pages and internal-stack claims from local repo/docs evidence |
- Polish or refresh a presentation outline, workshop plan, brownbag/session plan, slide notes, intake-form recommendation, or slide visual draft assets | `references/validation-index.md` | `references/presentation-outline-refresh.md`, `references/presentation-slide-visual-drafts.md`, `references/preview-validation.md`; for the Agent Skills sharing-series example, see `references/agent-skills-sharing-series-notes.md`. For slide visual draft assets, keep text large enough to read, match the deck's existing visual system before adding flair, and use real source snippets/examples instead of generic invented examples. |
| Fill Raymond's monthly Developer Experience / AIP report from recent repo work | `references/aip-monthly-dx-report-fill.md` | Work in a preview/copy unless live edits are explicitly approved, reuse prior-month format from session history, audit GitHub at team/repo level rather than Raymond-only using `references/aip-monthly-github-audit-pattern.md`, group evidence by AIP themes, preserve native heading/list styles, and use `references/aip-preview-reset-and-validation.md` if a preview needs to be reset from live after formatting regressions. |
| Draft/revise executive docs about parent-folder skill linking, SkillBuilder, or skill-creator-like flows | `references/agent-skill-folder-linking-exec-docs.md` | Use compact prose, explain one top-level folder link + GitHub PR feedback loop, and validate PDF/contact sheet for Markdown leakage or page spillover |
| Boss-facing reply or short doc that should mirror a reference doc's clean diagram-led framing | `references/boss-reply-diagram-formatting.md` | Simplify bullets, keep the code snippet, replace horizontal layering tables with an inserted diagram image, and verify the exported doc before handoff |
| Align executive summary email with technical exploration report across two Google Docs | `references/executive-summary-email-alignment.md` | Decision-first email structure, recommendation parity, constraint transparency, observability-layer preservation, concept mapping, next-steps priority, link hygiene |
| Refresh a multi-doc architecture/design/implementation package from repo evidence and publish preview docs first | `references/publish-index.md` | `references/multi-doc-architecture-preview-packages.md`, `references/multi-doc-pr-preview-to-live-sync.md`, `references/live-style-shell-pr-sync.md`, `references/preview-validation.md`, `references/reliability-and-timeouts.md` |
| Need cross-cutting rules and anti-patterns | `references/validation-index.md` | `references/operating-rules.md`, `references/api-lessons.md` |

## Script Entrypoints

Every primary script listed here should support `--help` as a no-side-effect readiness check. After running compile/help checks inside the skill tree, remove generated `__pycache__/` directories before committing or syncing.

| Script | Use |
| --- | --- |
| `scripts/setup.py` | OAuth setup, token check, revoke |
| `scripts/publish_pipeline.py` | Folder-based Markdown publish |
| `scripts/docs_api.py` | Create, update, read, headings, section-range, replace-section, export |
| `scripts/docs_advanced.py` | Images, orientation, spacing, tabs, low-level structured edits |
| `scripts/docs_table_tools.py` | Inspect tables and safely insert rows by strict header/anchor matching |
| `scripts/render_html_assets.py` | HTML diagram to tightly cropped PNG |
| `scripts/render_pdf_contact_sheets.py` | PDF page contact sheets for visual QA |
| `scripts/preview_post_refresh_audit.py` | Deterministic post-refresh preview audit |

Reference for native Google Docs Code Block constraints and placeholder workflow: `references/native-code-blocks.md`

Reference for section-mapped review comments: `references/doc-review-comment-mapping.md`

## Tab URL vs. screenshot-target reconciliation

When a user gives a tabbed Google Doc URL but identifies the intended insertion point from a screenshot, do not assume the URL tab is the target. Read the requested tab with `includeTabsContent=True`, then search every tab for a distinctive phrase from the screenshot (for example, the numbered action-item text). If the URL tab is empty or does not contain the pictured section, report the mismatch and ask which tab to use. If the user explicitly directs the pictured item or an interactive clarification expires, use the exact matching tab, make only the bounded requested edit, and state the tab title in the handoff. Preserve the supplied URL tab and sibling tabs untouched.

## Common Pitfalls

0. **Recurring shared reports should be filled in a copy first.**
   - Monthly AIP/DX reports, weekly reports, and similar shared templates may have manual formatting that range-based section replacement can damage.
   - If the user says “help me fill this doc” or points to a live report URL, create a copy/preview and fill that copy unless they explicitly approve live edits.
   - If you accidentally edit the live doc, stop immediately and use `references/live-doc-accidental-edit-recovery.md`: verify clean Drive revisions by exported sentinel text, restore the live doc from a clean DOCX revision, then create the draft copy from the restored live doc.

1. **Do not use `docs_api.py update` blindly on documents with native tables or images.**
   - Its paragraph-by-paragraph `_clear_document` path can delete trailing paragraphs, leave table structures behind, then fail with `Invalid deletion range`. A failed command may therefore have partially mutated the document.
   - Before a whole-body refresh, save a content export plus permissions/comments fingerprint and simulate the exact operation on a private copy.
   - For Markdown-first table/image-heavy previews, prefer a validated Drive Markdown/DOCX revision import that preserves the target file ID. After any failure, compare the live export to the baseline and restore or publish a fully validated revision immediately; never infer “unchanged” from the retained title alone.

2. **Cannot resize existing inline images via API.**
   - The Google Docs API does not support `updateInlineObjectProperties`.
   - Once an image is inserted, its display size can only be changed in the Google Docs editor (Image options → Size & Rotation).
   - Prevent this by computing the correct size at insertion time: `docs_advanced.insert_image(..., width_pts=..., height_pts=...)`.
   - Recommended portrait max: `440pt` wide; landscape max: `620pt` wide.

3. **Empty paragraph gaps around images create vertical spacing defects.**
   - Markdown import or API insertion often leaves empty `NORMAL_TEXT` paragraphs between images and captions or between consecutive images.
   - Detect them by scanning for paragraphs with no text and no image that sit between structural elements.
   - Fix from bottom to top via `deleteContentRange` so indices do not shift while you work.

4. **Tab rename requires `updateDocumentTabProperties`, not `updateDocumentTab`.**
   - The correct request name is `updateDocumentTabProperties` with `fields: "title"`.
   - To reparent a tab under a `Legacy` parent, use `fields: "parentTabId,index"`.
   - See `references/multi-tab-operations.md` for the exact REST payload.

5. **Native TOC cannot be refreshed via API.**
   - After heading changes, the native Table of Contents must be refreshed manually in the editor (right-click TOC → Update table of contents).
   - Plan for this in every handoff that touched headings.

6. **Contact sheets are the fastest way to visually QA long docs.**
   - Do not open 80+ pages one by one.
   - Export PDF, then run `render_pdf_contact_sheets.py` to get tiled thumbnails.
   - Spot-check flagged pages individually.

22. **`docs_api.py export` writes to stdout; redirect output yourself.**
   - The export command shape is `python scripts/docs_api.py export DOC_ID --format md` (or `html`/`txt`).
   - It does not accept `--output`; use shell redirection when saving locally: `python scripts/docs_api.py export DOC_ID --format md > /tmp/doc.md`.
   - For large docs with embedded images, export to a temp file first, then inspect targeted headings/sections to avoid terminal truncation.

23. **Read-only or limited-Drive Google tokens can fail if helper scopes are broader than the token.**
   - Symptom: `setup.py --check`, `docs_api.py get`, or `docs_api.py export` fails during refresh with `invalid_scope: Bad Request`, even though `~/.hermes/google_token.json` has usable Docs scopes such as `documents` or `documents.readonly`.
   - Cause: the helper loads credentials with hardcoded broad scopes (`documents`, `drive`), so Google rejects refresh for tokens consented with narrower Drive scopes such as `drive.readonly` or `drive.file`.
   - Fix for read-only review or Docs-API-only feasibility checks: load credentials using the scopes already stored in the token JSON, then call Docs `documents.get` directly; for Drive export/copy/import, re-authenticate with the needed Drive scope rather than assuming file access is missing.
   - Keep exported security-sensitive docs in `/tmp`, redact secrets before summarizing, and avoid pasting exploit bodies or credential-like output into chat.

23. **Read-only Google tokens can fail if helpers force write scopes.**
   - If `docs_api.py export` fails with `invalid_scope: Bad Request`, inspect the token's stored scopes before assuming Google auth is broken.
   - A token scoped to `documents.readonly` + `drive.readonly` can still read/export docs, but refreshing it with forced `documents` + `drive` write scopes can be rejected.
   - For read-only review, use the stored token scopes and Drive export directly; see `references/read-only-token-doc-export.md`.
   - Do not switch to a broader write token just to read a doc unless the user explicitly approves that scope escalation.

24. **`drive.file` does not grant general access to arbitrary shared Docs.**
   - A valid, refreshable token with `documents` plus `drive.file` can still receive Drive `404` for a document ID it did not create or open through that OAuth app. Treat that as a resource-visibility/sharing constraint, not proof that the document was deleted.
   - For ordinary Docs/Drive review and editing, connect the helper with a Desktop OAuth client and both `documents` and full `drive` scopes. Enable the Google Docs API and Google Drive API in the client project, then run `setup.py --client-secret <desktop-client.json>`, `setup.py --auth-url`, and `setup.py --auth-code <returned-url>`.
   - Validate the connection using `setup.py --check`, then probe the target file's Drive metadata before claiming access. Never paste OAuth client secrets, authorization codes, redirect URLs containing codes, or tokens into chat.
   - If the user only wants read-only access, prefer a read-only-scoped token where it has target-file visibility; use full Drive scope only when the intended operation or the account's sharing setup requires it.

## Visual QA Workflow (for preview validation)

After automated structure checks pass:

1. Export each doc to PDF via Drive API (`files().export_media(..., mimeType="application/pdf")`).
2. Generate contact sheets:
   - Contact sheets: `python <skill-root>/scripts/render_pdf_contact_sheets.py --inputs /path/to/doc.pdf --out-dir /tmp/page_audit_sheets`
     - In approval-gated environments, avoid destructive cleanup such as `rm -rf /tmp/page_audit_sheets`; use a fresh timestamped output folder instead.
3. Scan sheets for:
   - blank pages (blockers)
   - heading-only pages (medium)
   - oversized diagrams / images (medium)
   - large vertical gaps (medium)
4. For flagged pages, open the editor or extract the specific page with `pdftoppm -png -f N -l N`.
5. Fix what you can via API (empty paragraphs, spacing), then list what requires manual editor action.
6. Hand off with two lists: "fixed programmatically" and "needs manual editor action".

## Keep This File Lean

- Put phase-specific workflow details in `references/*.md`.
- Put reusable mechanics in scripts or templates, not in prose-only instructions.
- Keep project-specific doc IDs, heading names, layout ranges, and page-break rules in local wrapper/config files.
- When adding a durable lesson, update the owning reference file and this router only if a new branch is needed.
