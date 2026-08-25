# Presentation Outline Refresh

Use this reference when polishing a Google Doc that contains a presentation outline, workshop plan, brownbag/session plan, slide notes, or intake-form recommendation.

## Why this matters

Presentation outlines often look acceptable in Markdown but become hard to review in Google Docs/PDF because headings, auto-numbered lists, tables, and code fences interact badly with pagination. Treat these docs as layout-sensitive previews, not as simple text refreshes.

## Workflow

1. Work in the preview doc first.
   - Reuse the current preview for the live/original doc when available.
   - Do not promote to the live/original doc until the user explicitly approves the preview.

2. Make the outline reviewable before styling.
   - Use a short document title and short session/workshop titles.
   - Keep front matter compact: status, schedule, owner, and one recommendation line are usually enough.
   - Remove draft clutter such as alternative-title lists unless the user explicitly wants an ideation appendix.
   - Move long reference lists near the end.

3. Prefer scan-friendly blocks over wide tables.
   - Convert dense session-comparison tables into compact session cards or bullets when PDF readability matters.
   - Convert conceptual 2x2 matrices into labeled bullets if a table would wrap or split badly.
   - Keep tables only when row/column comparison is the point and the exported PDF remains readable.

4. Avoid Google Docs numbering surprises.
   - For slide/presenter notes, prefer explicit labels such as `Slide 1 — Title` over relying on one long ordered list across many headings.
   - For form sections, use `Question 1 — Prompt`, not slide labels.
   - For compact survey-signal or appendix summary blocks where visual bullets matter more than semantic list objects, consider literal `•` bullets with `replace-section --no-simple-lists`; this avoids Docs/API auto-list conversion failures where every line renders as `1.`.
   - After upload, export or inspect text to verify accidental label collisions are absent, for example `Slide 1 — What is your role?` should be zero if it belongs to the form.

5. Make visuals/illustrations first-class slide content.
   - For presentation outlines, do not stop at a generic `Visual:` label. Add per-slide `Visual / illustration direction` that tells the deck builder the layout pattern, objects, emphasis, and what not to overcomplicate.
   - Add paste-ready `Suggested visual copy` for the slide canvas, especially for concept-heavy slides.
   - Add `Alternative speaker line` options when wording or framing may be reused by the presenter.
   - Treat visual guidance as part of presentability, not optional decoration. A strong outline should explain what each slide should look like, not only what it should say.

6. Keep code snippets compact.
   - Use only the smallest code sample that proves the point.
   - Replace code blocks with prose markers when the exact syntax is not essential.
   - Watch for split code fences, orphan closing braces, lone option bullets, or one-line carryovers at page tops.
   - If Google Docs renders an indented note as a code-like block or labels it `None`, normalize indentation and convert supporting snippets into normal bullets.

7. Add page breaks intentionally.
   - Break before major sessions/workshops.
   - Also break before relevant standalone review sections such as `Form / Survey Recommendation`, success criteria, references, or appendices when the user wants them reviewable as separate sections.
   - Prefer parent-section breaks (`Form / Survey Recommendation`, `Top-Level Slide Outline — Session 1`, `Detailed Presenter Notes — Session 1`) over child-item breaks (`Question 6`, one slide note, one code snippet). Child breaks often create sparse orphan pages.
   - When adding page breaks to fix one orphan, re-audit later pages: a break before a child item such as Question 2 can strand the tail of Question 1 on a near-blank page. Prefer breaking before the parent section/question, or remove optional trailing bullets that create detached list tails.
   - Do not chase every top-of-page continuation in long presenter notes. If the page remains readable and has enough context, report it as a minor continuation; overfitting page breaks can create blank pages and worse list tails.
   - Do not add decorative page breaks that create sparse pages without improving reviewability.

8. Use numbering and highlights for reviewer readability.
   - Use numbered lists for sequence, decision packages, success criteria, survey/question lists, references, and step-like recommendations.
   - Keep nested answer options or role/platform options as bullets when numbering would make form metadata noisy.
   - Add short `Highlight:` callouts at major decision points: executive direction, session snapshots, form/survey guidance, and other sections where the reviewer needs the main takeaway before details.
   - When a user explicitly asks to update the outline/doc with an outreach email tied to the form/session, add a `Default Email Draft` subsection near the form recommendation so the doc carries the send-ready copy and approved session titles.
   - If the user only asks to improve a pasted email draft, answer with the revised email copy first. Do not update Google Docs, Forms, or source files unless the user asks to edit in place or the thread context clearly says the draft should be committed to the doc.

9. Adapt session outlines from survey results when available.
   - Treat survey recap as slide-content input, not just appendix data. Add a compact `Survey Signal and Implications` section near the top when results materially change emphasis.
   - If most respondents already have hands-on exposure, shorten pure “what is this?” intro content and shift time toward applied patterns.
   - If `when repeated work should become a skill` ranks high, add a dedicated decision-criteria slide: repeated workflow, inconsistent execution, consistency needs, multi-tool steps, costly mistakes, stable enough process.
   - If `how teams share and maintain skills` ranks high, add ownership, review, sharing, stale-skill retirement, and anti-sprawl guidance.
   - Replace generic examples with examples named in free-text responses when safe: PR review, docs/specs, weekly reports, CI/CD/config boilerplate, i18n/l10n, Google Docs workflows, incident triage, meeting scheduling.
   - Call out interface skew. If usage is CLI-heavy but the audience includes AIP/GLChat, IDE, web chat, PM, DD, or design surfaces, explicitly include non-CLI demo paths so the outline does not imply skills are terminal-only.
   - For workshop/session 2, start from workflow selection and qualification before authoring mechanics: pick repeated work, decide if it deserves a skill, define trigger/input/output/owner, draft, test on examples, and decide where it lives.

## Validation checklist

Before handoff:

- Re-read headings and title style after upload.
- Export Markdown/text and check for stale status/date strings, removed audience buckets, duplicate draft labels, malformed code fences, and blank-heading artifacts.
- Export PDF and render contact sheets.
- Classify contact-sheet findings using `references/preview-validation.md`: blocker, medium, cosmetic.
- Fix blocker/medium issues that are mechanical: blank pages, unreadable tables/code, split code blocks, orphan code fences, wrong numbering, severe orphan headings.
- For long presenter-note docs, distinguish true blockers from acceptable flow: a fully blank page, orphan heading with no body, split code block, or single detached bullet on an otherwise empty page is a blocker; a page that starts with continuation bullets but then contains substantial related content is usually a minor issue unless the user requested publication-grade pagination.
- Report minor continuation or sparse-page tradeoffs separately when they remain readable.
- Check unresolved Google Docs/Drive comments if the doc is review-facing.

## Handoff wording

State clearly:

- which preview doc was updated
- whether the live/original doc was also updated, and only say yes when the user explicitly approved live promotion or has an established doc-specific live-update preference
- key structural/readability changes
- validation counts or concrete checks performed
- remaining human-editor review gate if native TOC, footer page numbers, or publication shell items were not added by the refresh flow
- unresolved live comments, if any, and whether they were left untouched because comment resolution was outside scope
