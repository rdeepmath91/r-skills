# Slide Outline Review Checklist (Impact-First, Mixed Audience)

Use this when reviewing presentation-outline docs in Google Docs where the audience includes technical and non-technical participants.

## Review goals

- Keep the deck general-purpose and role-agnostic.
- Prioritize business/user impact before implementation details.
- Keep internal stack/runtime details (for example local-vs-remote runtime specifics) out of the main deck unless explicitly requested.

## Comment format to return to user

For each suggestion, provide:

1. **Highlight target** (exact heading/phrase to select in doc)
2. **Action type**: `remove` / `replace` / `adjust`
3. **Paste-ready comment text**

This prevents ambiguity and speeds up manual commenting.

## Required checks before suggesting edits

1. Pull current headings from the live document tab(s).
2. Pull comment list and unresolved status.
3. Map each recommendation to an exact existing heading/text so user can find it quickly.

## Common rewrite moves for this deck type

- Title: keep the central concept explicit when the session is meant to build shared vocabulary (for example keep “Agent Skills” in a Session 1 title).
- For two-session technical/non-technical splits, simplify Session 1 audience labels (for example “All”) and make Session 2 attendance expectations explicit (required vs optional groups).
- If each session has a different ETA, do not leave a single doc-level ETA that implies both sessions share one date. Put the schedule in the session package table and repeat each ETA in that session's snapshot for quick scanning.
- "Why" slide: convert technical claims into outcomes (rework, onboarding, consistency).
- Tools/API/MCP/connector comparisons: group them as the capability layer (“what the agent can touch”) and contrast with skills as the method layer (“how the agent should work”). A 2x2 matrix — with/without capabilities vs with/without skills — is often clearer than a taxonomy table.
- "Risk" slide: replace warning-heavy tone with a decision guide (when to use vs skip).
- Setup/implementation slides: compress to adoption path and move command-level detail to notes.
- Hero demo: score by accuracy, consistency, repeatability, missed-rule reduction, and review effort first; efficiency metrics are secondary. For Agent Skills talks, a strong demo is “long pasted instruction vs short request + skill.”
- Technical follow-up slides: include small real code snippets when the point is ease of adoption; push full setup, production versioning, and extended examples into GitBook/cookbook docs or a third hands-on session.
- For long multi-session outline docs, separate the reviewer-facing slide list from the implementation detail: first add a **Top-Level Slide Outline** with one line per slide, then a **Detailed Slide Content / Presenter Notes** section with bullets, demos, snippets, visuals, and speaker notes.
- For presentation presentability, require per-slide visual guidance in the detailed notes: `Visual / illustration direction`, `Suggested visual copy`, and optional `Alternative speaker line`. Generic labels like “Visual: scorecard” are usually not enough for a deck builder; specify the layout pattern, objects/cards/flows, emphasis, and paste-ready wording.
- After expanding visual guidance, re-run the PDF/contact-sheet audit. More visual notes often change pagination and can create detached list tails, orphan headings, or code/snippet separation that did not exist before.
- When a page break creates a near-blank page with only trailing list items, move the break to the parent slide/question or remove the optional trailing bullet; do not leave contextless option tails such as final role/platform choices on their own page.
- When a doc contains multiple full sessions, start each session on a new page in the preview doc so reviewers see clean boundaries. Prefer native Google Docs page breaks inserted before the session headings; verify the page-break count after upload/export where tooling allows.

## Pitfalls

- Do not assume earlier comments are already implemented; re-check unresolved threads.
- Do not propose broad edits without specific highlight anchors.
- Avoid recommending internal architecture/runtime content in a general-purpose deck.
