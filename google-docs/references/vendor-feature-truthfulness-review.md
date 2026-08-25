# Vendor feature truthfulness review

Use when reviewing a Google Doc about a specific external product feature, especially when the doc includes adoption/customization recommendations and existing Google Docs comments.

## Evidence pattern

1. Export the live doc first with `docs_api.py export DOC_ID --format md`.
2. List Drive comments before drafting feedback when the user mentions existing comments.
   - Use Drive `comments.list` with `includeDeleted=false` and fields for `id`, `author`, `resolved`, `quotedFileContent.value`, `content`, and `replies`.
   - Compare each unresolved comment's quoted text against the exported current doc text.
   - Treat zero matches as stale-anchor risk: the comment may still be valid, but the quoted content has moved or been edited.
3. Verify the vendor feature from primary sources in this order:
   - Official docs for user-facing behavior and prerequisites.
   - Official release notes/tags for feature introduction date and current version status.
   - Official PRs/issues only for implementation details when release/docs are ambiguous.
   - Repo tree/raw files for concrete file paths, defaults, shortcuts, bundled config/flow files, and implementation artifacts.
4. For JavaScript/Docusaurus docs, strip scripts/styles and normalize visible text; direct HTML snippets often hide useful content in rendered article text.
5. For internal adoption claims, require internal evidence: repo tag/commit, package/Docker version, lockfile, screenshot/version endpoint, or local source path. Do not accept the doc's own assertion as proof.

## Review hygiene

- Separate upstream feature truth from internal adoption truth.
- Flag exact wording problems: quoted phrases not used by sources, unsupported “headline feature” claims, date mismatches, and maturity overclaims.
- Soften unproven absolutes: prefer “not guaranteed until validated” over “zero knowledge” / “only understands.”
- Distinguish customization, retrieval/RAG, and fine-tuning. Do not call prompt/tool/flow edits “retraining.”
- If recommending “never suggest X” behavior, require evaluation or guardrails; prompt instructions alone are not guarantees.
- For adoption docs, force a structure that answers: what the feature is, what it takes to adopt internally, risks/challenges, recommendation/validation plan.

## Output shape

Produce a local Markdown review unless the user explicitly asks to edit/comment live:

- Executive verdict.
- Sources checked.
- Claim-by-claim validation table.
- Review against existing comments, including resolved/unresolved and stale anchors.
- Recommended document changes.
- Paste-ready comment pack with exact anchor snippets.

Do not post API comments by default; anchoring can be unreliable. Use manual-post mode or API-assisted hybrid only when requested.
