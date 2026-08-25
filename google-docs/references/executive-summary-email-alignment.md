# Executive Summary Email ↔ Technical Report Alignment Pattern

**Context**: Converting a detailed technical exploration report into a concise executive summary email for stakeholder review, where both documents live as separate Google Docs.

## Pattern Overview

| Element | Technical Report | Executive Email |
|---------|------------------|-----------------|
| **Audience** | Technical contributors, future reference | Decision-maker (e.g., Pak On, engineering lead) |
| **Length** | Full detail (10+ sections) | 1 screen / ~200 words |
| **Lead** | Executive Summary section | **Recommendation in subject line + first paragraph** |
| **Structure** | Chronological: setup → scenarios → findings | Decision-first: recommendation → key concepts → next steps |
| **Cross-link** | Self-contained | Links to report by title (not "this document, Tab 1") |

## Alignment Rules (from June 2026 Agent Skills / LangSmith case)

1. **Recommendation parity** — Email's "No direct adoption required" = Report's "Do not replace AIP observability with LangSmith"
2. **Constraint transparency** — Must include the `lm_invoker` model-path limitation (key blocker from report)
3. **Sentry/OpenSearch framing** — Preserve the observability-layer split (Run History / Sentry / OpenSearch) — don't collapse
4. **Concepts worth evaluating** — Map 1:1 from report's prioritized recommendations (recs 4–6 → degraded-success, trace tree, filtering)
5. **Next steps priority order** — Match report's implied priority (degraded-success first, filtering second, trace tree third)
6. **Link text** — Use report's exact title as link anchor; remove misleading "(this document, Tab 1)" when docs are separate

## Formatting Preferences (User-Stated)

- **Concise but not overly shortened** — First draft was rejected as "much shorter now"; final version matched original email length
- **No markdown artifacts** — No literal `**`, `|` table pipes, `#` headers in rendered doc
- **Selective bold** — Only on concept titles (Degraded-success visibility, Visual trace exploration, Advanced filtering)
- **Real hyperlinks** — `#1375` linked to GitHub issue; report title linked to report doc
- **Plain prose** — No visible markdown tables or bullet stacks; inline lists preferred

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| "Comprehensive coverage" overclaim | Use "covers the core execution data" / "most of the core" (report language) |
| Truncating the `lm_invoker` constraint | Always complete: "...and it did not provide the same model-level visibility for AIP's `lm_invoker` path" |
| Referencing wrong doc/tab | Verify doc IDs; link by title, not relative location |
| Missing action item reference | Include action item # (e.g., #1375) in opening context |

## Verification Checklist

Before sending alignment:
- [ ] Email recommendation matches report's top-level decision
- [ ] Key constraint (model path) is stated completely
- [ ] Observability layer split (Run History / Sentry / OpenSearch) preserved
- [ ] 3 concepts map to report's prioritized recs 4–6
- [ ] Next steps ordered by report's implied priority
- [ ] Report link uses exact title, points to correct doc ID
- [ ] No markdown artifacts in rendered email
- [ ] Bold only on concept titles
- [ ] Action item # linked and in opening line

## Related References

- `references/boss-reply-diagram-formatting.md` — diagram-led framing for boss-facing docs
- `references/agent-skills-sharing-series-notes.md` — Agent Skills series context
- `references/presentation-outline-refresh.md` — refresh workflow for outlines/notes