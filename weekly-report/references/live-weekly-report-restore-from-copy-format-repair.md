# Live weekly report restore from filled copy + previous-report format repair

Use this when the report subject restores the live weekly report template, has a separate filled copy, and asks to make the live doc follow a previous report's convention/formatting.

## Scenario

- Live doc was restored to a blank/template state but should keep its stable URL/ID.
- Filled content exists in a copy/backup doc.
- the report subject points to a previous filled report as the formatting sample.
- Goal is not to re-gather data; goal is to transfer the filled content into the live doc while matching the sample report's Google Docs structure.

## Procedure

1. Read all three Docs through the Docs API:
   - live target
   - filled copy/source
   - previous sample/reference
2. Inspect paragraph structures, not only text export:
   - `namedStyleType`
   - paragraph bullets and `nestingLevel`
   - link runs
   - body font family
   - blank heading leaks
3. Build the live doc body from the filled copy, but shape it like the sample:
   - title: `TITLE` when the sample uses `TITLE`
   - main section headings: `HEADING_1`
   - `Pull Requests`: `HEADING_2`
   - body/list text: `NORMAL_TEXT`, Proxima Nova, 11 pt when explicitly set
   - remove the template guide note (`Please refer to this guide...`)
   - remove helper/audit paragraphs that were useful for validation but should not appear in the report, e.g. `Strict audit summary: ...`
4. Restore numbered lists where the filled copy was flattened or accidentally converted to bullets:
   - Match the sample's native numbered style, not dot bullets: top level `1.`, level 1 `a.`, level 2 `i.`.
   - Use Docs API `createParagraphBullets` with `bulletPreset: NUMBERED_DECIMAL_ALPHA_ROMAN` for Issues, PRs, Meetings, Next Actions, and Technology list blocks.
   - Build each section's numbered-list block separately so PRs, Meetings, Next Actions, and Technology each restart at `1.`.
   - Issues commonly need sample-style nested numbering: top issue at level 0, context at level 1, details at level 2.
   - Out of Office in the sample may be plain manual numbering (`1. Out of office on ...`) rather than native bullets.
5. Link hygiene:
   - Preserve existing PR/article links from the filled copy.
   - PR links should remain only on final trailing `#123` markers.
   - Remove unlinked duplicate PR/issue references in PR titles before the final linked marker, such as `(#1555) #1556`, `fix #1365 — ... #1449`, or `for #1386 #1508`; keep only the linked final marker.
   - No raw visible URLs in the body.
6. After creating numbered lists, run a repair pass to delete numbering/bullets from any headings or blank paragraphs. Docs API bullet creation can accidentally absorb adjacent headings/blank spacer paragraphs if ranges are too broad; use paragraph ranges ending before the last paragraph newline when possible.
7. Validate the live doc:
   - placeholder count = 0
   - guide note absent
   - raw visible URL count = 0
   - PR link count and bad link text check (`#\d+` only for PR section)
   - headings match sample convention (`TITLE`, `HEADING_1`, `HEADING_2` for Pull Requests)
   - no blank heading leaks
   - no headings or blank paragraphs have bullets
   - body text has Proxima Nova where detectable
8. Export visual proof when possible. If Drive `files.export` returns `appNotAuthorizedToFile` under `drive.file`, use the Docs export endpoint directly:
   - `https://docs.google.com/document/d/<DOC_ID>/export?format=pdf`
   - send the bearer token in the request header.

## Pitfalls

- Do not blindly paste the filled copy into the live doc; the copy may have content but not the previous-report bullet nesting or heading convention.
- Do not leave validation prose in the final report. Remove audit-summary/helper paragraphs unless the user explicitly wants them.
- Do not assume weekly report section headings are always `HEADING_2`; older/sample reports may use `TITLE` for the report title, `HEADING_1` for main sections, and only `HEADING_2` for `Pull Requests`.
- Do not rely on text export to catch formatting damage. API structure must be inspected for heading styles, bullets, links, and font runs.
