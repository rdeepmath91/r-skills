# AIP Monthly DX Report Fill

Use this when Raymond asks to fill a monthly Developer Experience / AIP Google Doc from recent repo work.

## Trigger

- User gives a Google Doc like `Developer Experience (DX) <Month> <Year>` and asks to fill AIP/GLAIR content.
- User references the previous month as the desired format.
- Source evidence should come from GitHub PRs/issues across AIP-related repos, not memory alone.

## Source order

1. Export the target Google Doc via `docs_api.py export DOC_ID --format md` and inspect headings/placeholder structure.
2. Search prior sessions for the previous monthly AIP/DX fill when Raymond says “like last month”. Reuse the shape, not stale content.
3. Query GitHub activity for the report month across the relevant org/repos, not only Raymond's activity. Use `references/aip-monthly-github-audit-pattern.md`:
   - start broad with GDP-ADMIN repos updated during the month;
   - identify AIP/GLAIR-relevant repos and contributors;
   - treat created/merged-in-month PRs as achievement evidence and updated/open PRs as active-risk/next-step evidence;
   - always include core repos `GDP-ADMIN/glaip-sdk`, `GDP-ADMIN/ai-agent-platform`, `GDP-ADMIN/gl-runner`, and `GDP-ADMIN/gl-sdk` when they have month activity;
   - include adjacent repos such as GLChat, GL Connectors, smart-search/crawl, model-accuracy-benchmarking, and prompt-template only when their PRs materially affect AIP/GLAIR runtime, SDK, tools, evals, or product surface.
4. Before editing the preview, answer “what are you aiming to fill?” with the proposed sections/themes and evidence scope so Raymond can correct the narrative before formatting-sensitive writes.
5. Group evidence by themes rather than listing every PR:
   - `/goal` / agent command orchestration
   - context compaction
   - streaming/final-response reliability
   - image/vision artifacts
   - A2UI / HITL interaction
   - model usage / model routing
   - skills, tools, MCPs, filesystem
   - CLI/TUI developer workflow
5. Preserve non-AIP sections unless the user explicitly asks to fill them.

## Editing workflow

- Do not edit the live/original AIP monthly report directly unless Raymond explicitly says to apply changes to live. “Help me fill this doc” means create or reuse a preview/copy first, then edit the preview only.
- Before filling, show the intended section content at the outline/theme level when Raymond asks about scope or evidence. This catches “not only me, but in the repo” corrections before the doc is touched.
- Avoid whole-section `replace-section` for large nested report sections such as `Executive Summary` and `GLAIR` unless you can preserve native Google Docs list objects, heading styles, and paragraph spacing. Plain text or Markdown-derived replacement can convert real nested lists into sparse normal paragraphs with manual numbering.
- Preferred fill path:
  1. Export the live doc and inspect headings/placeholder structure.
  2. Copy the restored/current live doc to a preview, or reset the reusable preview from live before filling.
  3. Fill by replacing placeholder text inside existing list items, or clone style/list properties from nearby template paragraphs when inserting new items.
  4. Keep report content compact and theme-grouped; do not paste long Markdown bullet stacks into the Docs editor/API.
- If `replace-section` is unavoidable, first simulate it on a fresh copy and validate rendered layout before sharing. Use plain text section files only after deciding how native headings/lists will be restored; `--no-simple-lists` avoids repeated auto-list `1.` issues but does not preserve nested Google Docs list formatting by itself.
- If links matter, apply links with a follow-up Docs API styling step after the section body is stable. Raw URLs in executive monthly reports are a formatting smell unless the template already uses them.
- After editing the preview, export the Doc again and verify:
  - target sections changed;
  - AIP content contains the expected month-specific themes;
  - literal escaped Markdown markers like `\#\#`, `\*\*`, and `\`` did not appear;
  - placeholders remain only in sections intentionally left untouched;
  - PDF page count and contact-sheet density are close to the live/template;
  - heading/style counts, bullet counts, and nested-list structure still match the template shape where expected.
- If preview formatting regresses, use `references/aip-preview-reset-and-validation.md` to preserve the broken filled copy, reset the reusable preview from live, and restart from the clean template.

## Output style

Final handoff should be short and state:

- live doc link;
- sections changed;
- evidence sources/themes used;
- sections intentionally left untouched.

Do not narrate every PR unless Raymond asks for the audit trail.