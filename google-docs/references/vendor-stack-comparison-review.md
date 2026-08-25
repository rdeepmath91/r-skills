# Vendor/status comparison review for Google Docs

Use when a user asks whether a Google Doc about an external AI platform/vendor is current and aligned with an internal stack.

## Workflow

1. Export the source Doc as Markdown with `docs_api.py export DOC_ID --format md`.
   - If the export includes embedded base64 images and the terminal output is huge, use the text/headings from the export and avoid copying image payloads into notes or responses.
2. If the user mentions existing comments, list Drive comments before drafting feedback and compare `quotedFileContent.value` against the current exported text. Treat zero matches as stale-anchor risk, not as proof that the reviewer concern is gone. For the detailed feature-review pattern, see `references/vendor-feature-truthfulness-review.md`.
3. Identify the document's main claims and date/version before researching.
4. Check current vendor status from primary sources first:
   - Official product pages.
   - Official docs.
   - Official pricing/model pages.
   - Official announcement/news pages.
   - Official release notes/tags for feature introduction dates and version status.
   - Official PRs/repo tree/raw files for implementation artifacts such as bundled config files, shortcuts, or internal flow definitions.
5. Use reputable secondary sources only to clarify maturity/launch status (for example public preview, beta, control-plane architecture), not as the sole source for claims.
6. Compare against internal stack evidence from local docs/repos, not memory alone. For GLChat/AIP-style reviews, useful evidence includes:
   - Tech stack summary files.
   - Message/agent execution contract docs.
   - Prior comparison notes if present.
   - Local README/docs for SDK/runtime examples.
   - Repo tag/commit, package/Docker version, lockfile, screenshot/version endpoint, or local source path for claims about the current internal baseline.
7. Separate findings into:
   - Still aligned.
   - Missing/latest vendor updates.
   - Overstated or stale claims.
   - Comparison to internal stack.
   - Recommended doc edits.

## Claim hygiene

- Preserve nuance around maturity: use “public preview”, “beta”, “implemented/documented enough to evaluate”, “designed for production-grade”, or “marketed as” when sources do not prove production readiness for the user's internal stack.
- Distinguish hosted control plane from customer-run workers/data plane; do not equate hybrid deployment with fully self-hosted or air-gapped.
- For connector counts and pricing, expect public pages to change. Verify immediately before finalizing.
- For internal-stack claims, avoid broad absolutes like “any model”, “any connector”, “fully offline”, “already present”, “no merge required”, or “all PII removed” unless the checked code/docs prove the exact scope.
- Separate vendor-feature truth from internal-adoption truth. A feature can be real upstream while still unproven or unready in the internal fork.
- Do not put paraphrases in quotation marks unless the checked source uses that exact wording.
- Distinguish customization, retrieval/RAG, and fine-tuning; prompt/tool/config edits are not “retraining”.
- Treat prompt-only behavioral constraints such as “never suggest native components” as goals requiring evals/guardrails, not guarantees.

## Output shape

Prefer a concise executive verdict followed by bullets/tables:

- Verdict: aligned / partially aligned / not aligned.
- Top current updates missing from the Doc.
- Internal stack overlap and gaps.
- High-impact edits to make the Doc defensible.

Name the sources checked at a high level, but avoid dumping long excerpts unless the user asks for citations.