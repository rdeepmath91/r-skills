# Agent Skills quick-check survey recap notes

Use this as session-specific context when summarizing the Agent Skills Knowledge Quick Check results or updating the related slide-outline Google Doc.

## Form context

- Form ID: `16cZ45TWqsfzrm-_JtHYvK-JaPcCnh5p92kOhPTNAW0A`
- Edit URL: `https://docs.google.com/forms/d/16cZ45TWqsfzrm-_JtHYvK-JaPcCnh5p92kOhPTNAW0A/edit`
- Public URL: `https://docs.google.com/forms/d/e/1FAIpQLSdNXU4szs4NuDeOOQ5ypiPk3crBKXUVFY8P1zRZjtgS78nuPg/viewform`
- Helper directory: `/home/raymond-christopher/.hermes/skills/productivity/google-forms`

## Recap workflow

1. Load `google-forms`.
2. Fetch current form and responses:
   ```bash
   cd /home/raymond-christopher/.hermes/skills/productivity/google-forms
   python3 scripts/gform.py get 16cZ45TWqsfzrm-_JtHYvK-JaPcCnh5p92kOhPTNAW0A > /tmp/agent_skills_form_current.json
   python3 scripts/gform.py responses 16cZ45TWqsfzrm-_JtHYvK-JaPcCnh5p92kOhPTNAW0A > /tmp/agent_skills_form_responses_current.json
   ```
3. If response export times out, retry once with a longer timeout.
4. Aggregate single-select answers by exact label.
5. Flatten checkbox answers and report each option as `count / total responses`.
6. Normalize obvious role drift, especially `Data Developer` vs `Data Developer (DD)`, while noting if raw labels differed.
7. Cluster free-text answers into themes rather than dumping all responses once response count is large.

## Slide-oriented deliverable

When Raymond says the recap is for slides/content, produce a slide-content pack, not a raw report:

1. Audience snapshot.
2. Adoption / usage signal.
3. Current use cases.
4. Biggest learning needs.
5. Free-text workflow themes.
6. What this changes for the session outline.
7. Optional appendix with raw counts.

## Known useful interpretation for the Agent Skills outline

If the same pattern holds at larger `N`:

- If most respondents have already used skills, keep “what are Agent Skills?” short.
- If many have created/edited skills, treat the audience as mixed: power users plus newer users.
- If CLI remains dominant, explicitly include non-CLI paths: AIP / GLChat, IDE/editor, and web chat.
- If `when repeated work should become a skill` ranks high, add a decision-criteria slide.
- If `how teams should share and maintain skills` ranks high, add ownership, review cadence, stale-skill retirement, and anti-sprawl guidance.
- Use free-text examples as demo anchors: PR/code review, docs/specs, weekly reports, CI/CD/config boilerplate, meeting scheduling, l10n/i18n, Google Docs reader/writer, incident triage.

## Privacy

- Do not print response IDs in the final recap.
- Do not expose respondent names or emails if the form later starts collecting identity.
- Include URLs from free text only if they are relevant and non-sensitive.
