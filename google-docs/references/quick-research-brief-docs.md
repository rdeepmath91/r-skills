# Quick research brief docs

Use this when the user asks for a short researched comparison/list and wants it compiled into a Google Doc, especially with live links and prices/options.

## Workflow

1. Clarify only task-shaping ambiguity.
   - Ask for missing dates, route direction, preferred scope, or destination assumptions when they materially change the search.
   - If there is an obvious interpretation, proceed and state the assumption in the doc.

2. Gather live source data.
   - Prefer official/search aggregator pages for volatile data such as flights, hotels, prices, events, or availability.
   - For dynamic pages, browser snapshots can expose visible result summaries.
   - If the accessible tree is noisy, inspect `aria-label` values in the page DOM; Google Flights result cards often encode price, airline, departure/arrival airports, times, dates, duration, and selection text in labels.
   - Extract the source URL (`location.href`) or use stable search links when the dynamic URL is long or brittle.

3. Filter against the user's constraints before writing.
   - Build the table around actual decision constraints, not every result.
   - Include near-miss rows only when useful, and label them clearly (`Ideal`, `Nearby`, `Borderline`, `Fallback`).
  - For travel, separate outbound and return legs and rank a short recommendation summary before full tables.
  - Preserve and operationalize user travel preferences when ranking, not only hard constraints. If the user says they prefer a nearer airport, less-painful departure time, or similar convenience factor, make that ranking logic explicit in the relevant section and re-sort options accordingly; keep buffer/cheapest options as fallbacks when they conflict with the stated preference.
  - For flight options, include the public flight code/flight number in the recommendation summary and detailed table when available. If the primary booking/search source omits it, cross-check via airline pages or flight-tracker snippets and add a checkout-confirmation caveat.
  - If the user asks whether other airlines/options were checked, explicitly scan the visible result set for plausible alternate carriers (e.g., Pelita Air on Indonesian domestic routes) and include them as recommended, nearby, or “checked but outside window” rather than silently omitting them.
  - When the user asks whether later/earlier relaxed-window options are cheaper, add a short explicit price-check note in the relevant leg section. State the relaxed window, compare the best current recommendation against the checked later/earlier alternatives, and say plainly whether cheaper options only appear outside the user's practical timing window.
  - If the scope expands from flights into accommodation, keep hotels as a separate recommendation block/table with area fit, price/night, total stay price, rating when available, links, and a concise note explaining when each option is worth booking.
  - For hotel budget caps, confirm whether the cap is per-night or total-stay. If the user clarifies it is per-night, re-rank toward better comfort/reliability within the nightly cap rather than continuing to optimize for the cheapest possible total.
  - When the user asks for a hotel “mid alternative” or “lowest standard I can still sleep on,” stop optimizing only for lowest price/distance. Add an explicit comfort floor recommendation using neutral signals: recognizable chain/brand, Google rating and review count, star/class signal, office distance, and price band. Label options as `Comfort pick`, `Mid alternative`, `Lowest sleepable standard`, and `Budget fallback` so the decision is clear.

4. Write a concise Markdown source file.
  - Put the recommendation summary / executive summary near the top, before detailed tables. For travel comparisons, include the user's top 3 picks per direction/leg in that summary. If the scope includes accommodation or another booking category, include a top 3 for that category too.
  - Use the highest heading level for the document title (`#` -> Google Docs Title), then `##` for major sections such as Executive Summary / Flights / Hotels / Links / Notes, and `###` for subsections such as Outbound / Return. Keep headings short; avoid date ranges, route detail, or explanatory clauses in headings when the body already provides them.
  - Prefer concise numbered recommendation lists for the executive summary when each pick needs multiple links; wide summary tables with link columns often wrap badly in Google Docs/PDF.
  - When updating an existing travel/booking doc, do not just patch plain text. Re-apply Google Docs-native formatting on every update: native headings, hyperlink text instead of visible raw URLs, native tables for assumptions/options/booking links when applicable, and layout settings suitable for those tables.
   - Move assumptions below the executive summary when the user needs a fast decision-first doc, while still keeping the assumptions before detailed analysis if possible.
   - Include only the sections that support a booking decision: prepared date, source caveat, top picks, concise assumptions/notes, filtered option lists/tables, compact links, and final booking checks. Remove duplicate decision tables, repeated long links in every row, and verbose methodology once the core options are clear.
   - If the user wants the doc to look attributable or shareable, add a short attribution line near the top such as `Analysis by: <name>` rather than burying authorship in metadata or the final chat response.
   - For volatile prices, explicitly say prices can change and final checkout may differ due to bags/seats/payment fees; for lodging, also note nightly caps, breakfast, cancellation policy, taxes/fees, and HR/company-policy checks.
   - For hotel “sleepability” advice, put a short prose recommendation before the hotel table. State the cheapest option you would still recommend as the floor, one mid alternative between premium and budget, and why cheaper options are demoted. Avoid vague “decent” labels without evidence; cite rating/class/brand/distance/price signals.
   - Keep shareable reports free of personal-preference wording unless the user explicitly wants it included. Do not write lines like “preference applied,” “avoid X vendor/group,” or name personal restaurant tastes. Steer recommendations through neutral decision criteria instead: timing fit, airport convenience, operational predictability, price, office proximity, central access, budget cap, and fallback status.
  - Use links that remain useful after handoff: aggregator search, airline/vendor pages, hotel search pages, and direct booking sites where appropriate. When applicable, attach practical links to each recommended pick, not only a generic links section.
  - If a link is only a generic route/date/area search and does not reliably reopen the exact quoted fare, hotel, or price, do not put it in every option row or executive-summary pick. Keep option rows focused on airline/hotel, time, price, and decision rationale; move generic links into a separate `Booking Links` section with an explicit caveat that the user must select the matching option from the table.
  - For flight docs, verify every final link opens the intended route/date result page. Google Flights often cannot reliably deep-link to a single selected flight card, so label those as route/date searches and tell the user to select/filter the airline and time from the table. Avoid handing off generic airline/OTA home/search URLs unless they are intentionally fallback links.
  - Emphasize the decision fields that the user scans first. For travel briefs, bold departure/arrival times and prices in the executive summary, decision table, and detailed option tables.

5. Publish with the right conversion path.
   - For quick internal notes, `publish_pipeline.py <tmpdir>` is acceptable.
   - For boss-facing docs or table-heavy comparison docs, prefer Drive Markdown import/update (`files.update` with `mimetype='text/markdown'`) so tables become native Google Docs tables instead of visible raw Markdown.
   - If updating an existing doc, preserve the existing doc ID when possible and treat Drive import as whole-document body replacement.

6. Polish table-heavy docs after import.
   - Use landscape orientation and narrow margins when tables have many columns.
   - Style header rows, tighten paragraph spacing, and reduce table font/padding only enough to avoid wrapping or clipping.
   - If a wide table forces ugly layout, split the content into a short recommendation/decision table plus separate outbound/return/detail tables instead of one massive table.
   - For travel tables with multiple booking sources, keep verbose descriptive links in the executive summary and route-specific link section, but shorten repeated table-link labels to compact labels like `GF` and `Tiket` to prevent link columns from exploding page count or wrapping every row.
   - After Drive Markdown import/update, verify and repair heading promotion if needed. Some imports may map `#`/`##`/`###` to `HEADING_1`/`HEADING_2`/`HEADING_3` instead of `TITLE`/`HEADING_1`/`HEADING_2`; restyle the document title and major/subsection headings through Docs API before handoff.
   - If a short final notes section creates a trailing blank PDF page, compress it into an earlier caveat/source paragraph or remove redundant notes. Do not leave a mostly blank or fully blank last page just to preserve low-value caveats already covered elsewhere.

7. Verify before handoff.
   - Export as `txt` or `md` and confirm the title, assumptions, recommendation summary, and key tables landed.
   - Run `docs_api.py headings DOC_ID` after heading changes and verify the intended promotion: document title is `TITLE`, major sections are `HEADING_1`, and subsections are `HEADING_2` or lower.
   - After repeated whole-document `docs_api.py update` operations, inspect the exported tail or raw structure for trailing empty paragraphs / blank heading artifacts. If they appear, delete the trailing empty range from the last real paragraph to the document end with a Docs API `deleteContentRange`, then re-export and re-run `headings`.
   - For table-heavy docs, inspect Docs structure for native table count and confirm there are no raw Markdown table separators such as `| --- |`.
   - Confirm applicable links are actual hyperlink text, not visible raw URLs. Count links in paragraphs/table cells when practical, and export to Markdown to check for escaped link brackets (`\\[` / `\\]`) or raw booking URLs in the final link section.
   - Export to PDF, render a contact sheet, and visually check for raw Markdown artifacts, clipped tables, blank pages, orphan headings, unreadable text, whether key emphasis such as bold times/prices survived import/export, and whether long tables continue cleanly across pages.
  - When the user specifically asks to remove/check empty pages, verify both the raw Docs structure and the PDF export. Raw structure: use `docs_api.build_service('docs','v1').documents().get(documentId=DOC_ID).execute()` and scan paragraph elements for `pageBreak` entries and blank paragraphs; the `docs_api.py get` command returns simplified content and is not enough for this. PDF structure: export through Drive `files().export_media(..., mimeType='application/pdf')`, run `pdfinfo` for page count, then `pdftotext -layout` and split on form feed (`\f`) to confirm every rendered page has nonblank text. Do not try to delete the required final document newline; Google rejects deleting the segment-ending newline and it does not by itself create a blank page.
  - When adding sections to an existing doc, re-check the later pages too; table continuation, links sections, and final notes can regress after earlier layout changes even if the first contact sheet looks good.
- If the user asks to change page orientation after handoff, apply the orientation update immediately, re-export to PDF, verify page size/orientation with `pdfinfo`, then rerun contact-sheet visual QA. Do not rely on the Docs editor setting alone.
   - Open or fetch the final linked URLs, not only the source Markdown links. For dynamic search links, verify the resolved page intent is route/date/scope-correct and use honest link labels such as `Google Flights — outbound route/date search` when exact-item deep links are not stable.
   - After direct Docs API text/link repairs, export as Markdown and run a focused hygiene scan before handoff: no escaped link brackets like `\\[` / `\\]`, no raw long booking URLs visible in the final link section, no blank headings, and no trailing formatting garbage after the last real note.
   - When adding prose adjacent to a Markdown table and re-importing/updating the whole Google Doc, place the prose before the table or use a direct Docs API paragraph insertion outside the table boundary. A blank line after a table can still be interpreted by Google Docs export/import as part of the table, turning the prose into a one-cell table row; verify by exporting Markdown and checking the note does not start with `| Note text`.
   - Fetch Drive metadata for `webViewLink` when available.
   - In final response, give the doc link and only the top recommendations; avoid dumping the full table again.

## Pitfalls

- Do not claim booking availability beyond what the source showed; volatile fares may disappear.
- Do not expose private decision logic as personal preference in a report meant to be shared. For example, avoid naming a disliked airline group or specific restaurant preferences in the prose; rank the preferred options higher using defensible neutral labels such as `Best overall`, `Cleanest timing`, `Operationally predictable`, `Central access`, or `Fallback`.
- Do not imply a search-result link is an exact option/flight deep link unless you verified it reopens that exact item. If the platform only preserves route/date, say that plainly and make the table carry the exact airline/time/price.
- Do not overfit to a single airport if the user uses a city/suburb name. State airport assumptions and include alternatives when requested.
- Do not treat earliest arrival as automatically best when the user values airport convenience or avoiding very early mornings. Rank the option that best balances stated preferences and constraints, then label earlier/cheaper options as buffer or price fallbacks.
- If a user asks for “all alternatives,” include all practical alternatives within the constraint window, not every flight across the day.
- If an alternate carrier only has flights outside the requested window, still record it briefly as checked-but-too-late/too-early so the omission is explainable.
- When hotel budgets are discussed, avoid ambiguous “under cap” language until the unit is clear: per night vs total stay changes ranking and should be stated in the doc.
- Google Flights accessible labels may repeat each result several times (`Select flight`, `Leaves...`, `Flight details...`). Deduplicate by price + airline + route + depart/arrive time.
