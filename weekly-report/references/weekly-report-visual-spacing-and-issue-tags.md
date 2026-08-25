# Weekly report visual spacing, source issue tags, and security issue updates

Use this when Raymond asks to refine a weekly report after visual review or asks that Issues be copyable from `AIP Current Issues`.

## Formatting lessons

- Add visual breathing room with paragraph style, not manual blank lines.
- Keep `Issues` immediately after the title with `spaceAbove: 0`.
- Set later top-level `HEADING_1` sections to about `spaceAbove: 12pt`:
  - `Accomplishments`
  - `Meetings/Events/Training/Conferences`
  - `Key Metrics / OMTM`
  - `Next Actions`
  - `Technology, Business, Communication, Leadership, Management & Marketing`
  - `Out of Office`
- Set `Pull Requests` (`HEADING_2`) to about `spaceAbove: 6pt`.
- Use paragraph spacing rather than blank paragraphs so page flow stays stable and trailing blank pages are less likely.
- For contact-sheet validation, prefer a fresh temp output directory (timestamped) instead of `rm -rf` cleanup; deletion approval can interrupt the workflow.

## Issues source-of-truth rule

When adding GitHub tags/links to the weekly report's `Issues` section, update the source tab too:

- Source doc: `AIP Current Issues`
- Use the latest matching child tab for the report week, e.g. `June 2026` -> `Week 4 Jun 2026`.
- Add/link `#PR` or `#issue` markers in the source tab first or in the same pass, then copy/reflect them into the weekly report.
- This keeps future copy/paste from the source doc clean.

## GitHub tag lookup pattern

- Search recent PRs/issues in the relevant repo and across GDP-ADMIN when the source note gives only a bare number.
- A bare `#1022` in the AIP issue source may point to another repo; verify with org-wide search before linking.
- Prefer exact PRs/issues mentioned by the source text:
  - BYOK registration fixes: `GDP-ADMIN/ai-agent-platform` PRs `#1357`, `#1332`.
  - Agent building requirements: `GDP-ADMIN/glaip-sdk` issue `#1022`.

## Security issue grouping and status accuracy

For security-related weekly issues, do not mark the whole grouped item `[Done]` just because related PRs merged. First inspect the parent/roadmap issue and open follow-ups, then choose the status:

- `[Done]` only when the parent issue/follow-up validation is closed or the user explicitly confirms no further testing is needed.
- `[Testing]` when implementation PRs are merged but DSO/security validation is still checking whether the penetration path remains possible.
- `[WIP]` when implementation work or required follow-up issues are still open.

For the `/accounts` + custom-tool security journey, status changed over time. Use the latest validation state from the source issue/doc, not the historical example below:

```text
[SOLVED] Harden /accounts and custom tool security paths #2114
    /accounts and custom-tool hardening PRs are merged (#2113, #2140, #2138, #2159).
    Secret-forwarding and MCP/secret-policy fixes are merged (#2132, #2142, #2144).
    Security assessment for GL AIP v0.2.49 is complete: the previously reported account-creation, local disk execution, and sandbox issues were remediated; no findings were identified within the assessment scope, so the /accounts endpoint can be unblocked.
```

Historical transition rule:

- Use `[Testing]` while DSO/security validation is still checking whether the penetration path remains possible.
- Change to `[SOLVED]` only after the security assessment result says the relevant findings were remediated/no findings remain in scope and `/accounts` can be unblocked.

Link markers:

- `#2114` -> `GDP-ADMIN/ai-agent-platform` issue.
- `#2113`, `#2140`, `#2138`, `#2159`, `#2132`, `#2142`, `#2144` -> `GDP-ADMIN/ai-agent-platform` PRs.

## Validation

After editing both docs:

1. Re-read `AIP Current Issues` latest week tab and verify issue lines + link metadata.
2. Re-read the weekly report and verify:
   - placeholders = 0 unless explicitly left blank
   - raw visible URLs = 0
   - issue tag markers linked
   - PR section still has exactly one linked final `#N` marker per row
3. Export the weekly report to PDF and render contact sheets with `google-docs/scripts/render_pdf_contact_sheets.py` using a fresh output directory.
4. Fail validation on blank trailing pages, obvious large gaps, or broken page flow.
