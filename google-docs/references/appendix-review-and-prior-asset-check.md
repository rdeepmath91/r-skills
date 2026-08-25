# Appendix review and prior asset check

Use this when a user asks whether a live Google Doc appendix/section can be improved, especially when diagrams may have been iterated in earlier sessions.

## Workflow

1. Export the live Google Doc, not just the source draft.
   - Use Markdown/text export for targeted content review.
   - Use PDF export for rendered layout review.
   - For tabbed docs, confirm the tab ID/title first when available.

2. Locate the exact appendix/section.
   - Search exported Markdown/text for the appendix heading and adjacent headings.
   - Read the exported section plus the surrounding page/section boundary so table splits and carry-over pages are visible.

3. Render the affected PDF pages.
   - Convert only the relevant pages to PNG first, then run visual QA on those pages.
   - Check for: tiny or low-contrast diagrams, cropped labels, dark-theme diagrams inconsistent with the doc style, dense tables, row splits across pages, orphaned headings, and missing synthesis/caption text.

4. Search session history for prior improvement attempts before concluding none happened.
   - Look for the appendix title, diagram filename, doc ID, and key terms from the section.
   - Prior work may have produced local assets or a draft recommendation without inserting it into the live doc.

5. Compare prior assets against the live rendered doc.
   - If a better local diagram/source exists but the live PDF still shows the old image, say that clearly: the diagram was improved as an asset, but not promoted/inserted into the live doc.
   - Name the local asset paths plainly so a future update can reuse them.

6. Return a prioritized improvement list.
   - Separate content/tone improvements from rendered-layout improvements.
   - For diagrams, include whether the issue is conceptual clarity, styling consistency, readability, sizing, cropping, or live-doc promotion.

7. If the user asks to improve the appendix after review, prefer a compact replacement that preserves the user's source intent.
   - Use the user's existing paragraph/framing as the base instead of inventing a new thesis.
   - Make the answer progressive: short core framing sentence, component responsibility, runner/operational boundary, orchestration-stack role, then final implication.
   - For executive appendices, remove meta sections like “recommended wording” or “suggested heading changes” once the recommendation has been incorporated; they are useful during review but often create page spillover in the final appendix.
   - Keep the final appendix to the smallest complete unit that answers the question, commonly one page with a readable diagram and concise explanation.

8. For ecosystem diagrams that clarify platform boundaries, use the diagram to encode ownership rather than implementation detail.
   - Show the operating platform/boundary as the outer frame.
   - Put server/control-plane and worker/execution-plane concepts inside that boundary when relevant.
   - Show third-party orchestration as a pluggable stack inside the operating boundary, not as a competing product unless that is the intended claim.
   - Show the subject workflow as one runnable workload among other workload types when the point is “operated by the platform.”
   - Use a light, document-native visual style and export the affected page for visual QA before handoff.
   - If a component capability is challenged by the user/stakeholder, replace broad labels with concrete capabilities the component actually handles. For example, do not put access control inside a Prefect box unless the source/stakeholder explicitly supports it; prefer concrete Prefect-owned boxes such as deployments, schedules, work pools/workers, run state, retries/logs.
   - Keep diagram text compact: no subtitle or long takeaway banner when the surrounding prose already explains the nuance. After removing text, tighten the canvas/container height so the fit-check does not leave a large empty lower half.

9. When the appendix is resolving overloaded terminology, lead with the ambiguity instead of product comparison.
   - If stakeholders point out that two systems use the same word (for example `pipeline`), explicitly define each meaning before any table of strengths.
   - Avoid headings like `X replaces Y` when the desired message is `same word, different layers`; prefer `What X Adds Beyond Y`, `When X Is the Better Workflow Layer`, and `When Y Is the Better Execution Layer`.
   - If examples are agent-heavy, add a scope sentence: the examples focus on LLM-heavy/agentic workflows because those are where the terms are confused; the underlying layer may still be broader.
   - For Prefect-vs-GL-Pipeline wording, a useful distinction is: Prefect pipeline = scheduled, distributed, durable data workflow/job; GL Pipeline = in-process step graph for a single live workflow/reasoning execution; GL Runner = production boundary that operates runnable executions.
   - When distinguishing two orchestration layers, avoid narrowing a general-purpose workflow layer to only agents/LLMs unless the section is explicitly about agentic examples. Use broader wording such as workflow steps, dependencies, state transitions, inputs/outputs, and calls to tools, services, models, or agents.
   - Avoid headings such as “X replaces Y” when the intended thesis is complementary layers or different responsibilities. Prefer “What X adds beyond Y,” “When X is the better workflow layer,” or “When Y is the better execution layer.”
   - If the live doc still contains a dark Mermaid-style diagram with literal `\\n` labels or tiny labels, treat that as a promotion gap: a better GDP Labs HTML/SVG asset may exist locally but still needs insertion into the live doc.

## Common findings to call out

- “Replaces” headings can undermine a non-adversarial comparison even if the prose says the components are complementary.
- Dense appendix tables often need a short decision-rule block before the tables and a closing synthesis after them.
- A table row split across pages can make the next page start mid-sentence; recommend keeping that row together or splitting earlier.
- Dark Mermaid-style diagrams can look out of place in polished GDP Labs docs if the rest of the document uses the lighter GDP Labs visual language.
