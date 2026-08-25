# One-time gathering feedback forms

Use this when building a lightweight post-event Google Form from a participant roster and slide/event sections.

## Recommended structure

Keep the form in a few short conceptual sections rather than one long wall or one section per agenda item:

1. **Data Peserta**
   - Role dropdown, e.g. `DF`, `DL`, `DM`, `CT`, `Other`
   - Group/date dropdown from the roster, e.g. `Bekasi 27`, `Pulo Gadung 1`, etc.
   - Name dropdown with all confirmed participant names sorted A-Z.
   - Exclude cancelled rows, blank summary/totals rows, and rows without a name.
   - If the roster has `Extra pax` values but no guest names, add explicit options such as `Extra pax — <host name>` for each extra pax so the dropdown covers the sheet's headcount, not only named rows.
   - Add a fallback option such as `Other / Nama belum ada di list`.
   - Follow with an optional short-answer field: `Kalau nama kamu belum ada di list, tulis di sini`.

2. **Overall Feedback**
   - If the user asks for actual Google Forms rating mode, create separate `rating` items rather than putting the scale in the form description or using a grid.
   - For 1-5 rating items, use `scaleMax: 5`, `ratingIcon: STAR`, `lowerLabel: "1 — Sangat kurang"`, and `upperLabel: "5 — Sangat baik"`.
   - Keep the form description short; do not place the full `1 = ... 5 = ...` scale block at the top when the scale belongs on rating questions.
   - Questions can cover overall satisfaction, theme relevance, comfort to interact/share, flow, and duration fit.
   - If the user explicitly wants every intermediate phrase visible at once, use a multiple-choice grid with columns `1 — Sangat kurang`, `2 — Kurang`, `3 — Cukup`, `4 — Baik`, `5 — Sangat baik`.

3. **Feedback per Section Acara**
   - Mirror the same rating format selected for Overall Feedback.
   - Rows/questions should map to event sections visible in the deck/agenda, e.g. Games Time, Praise & Worship, testimony/sharing, Q&A, Small Group.

4. **Kesan & Saran**
   - 1 required paragraph: most memorable part and why.
   - 1 optional paragraph: what to improve next time.
   - 1 optional paragraph: one action the respondent wants to start after the gathering.
   - Prayer request only if the team is prepared to handle it privately and follow up.

## Dynamic name filtering

Native Google Forms cannot dynamically filter a name dropdown based on Role + Group/date selections. The closest Google Forms approximation is section routing: Role -> Group/date -> a filtered name dropdown section. This works but creates many sections for every role/group combination.

For one-time gatherings, prefer the simpler form: role dropdown + group/date dropdown + all confirmed names A-Z + `Other / Nama belum ada di list` fallback. It is faster for respondents and easier to maintain.

## Access pattern

Responder access can be public while edit/results access remains private:

- Public responder link: Forms settings must allow anyone with the link to respond.
- Private edit/results: share the edit form or linked response Sheet only with selected people.
- Do not enable respondent summary charts/text responses unless results should be public to respondents.

## Verification checklist

Before handing off a form link:

1. `get` the form through the helper and confirm title, description, question count, and item titles/types.
2. For dropdown completeness, do not rely on `get` alone because it only exposes item titles/types, not choice labels. Fetch the public responder HTML and confirm every expected dropdown option string appears there; especially verify all roster names, `Extra pax — ...` options, and `Other / Nama belum ada di list`.
3. Open/fetch the responder link unauthenticated. A `401`/Google sign-in page means it is not public-ready, even if the form was created successfully.
4. Verify form ownership by opening an edit URL and checking the top-right account, or by confirming the Drive file is visible to the intended account. OAuth tokens do not determine ownership when using the Apps Script web-app flow; the deployment account does.
5. If the created form title comes back blank, treat it as deployed Apps Script code mismatch or stale deployment. Redeploy the known-good `appscript_code.gs` from the intended account before creating the final form.
6. If `rating` creation fails with `Unknown question type: rating` or scale questions read back as `MULTIPLE_CHOICE`, redeploy the current Apps Script Web App and rerun a small rating probe before regenerating the production form.
