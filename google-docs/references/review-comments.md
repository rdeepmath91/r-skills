# Comments and Review Threads

## Before commenting
- Read the latest document state first.
- If possible, inspect existing threads before adding a new one.

## Comment strategy
- Prefer one concern per thread.
- Keep the comment short and specific.
- Reply in an existing thread when the same point is already being discussed.
- Match comment framing to the document owner/audience. For PM/product exploration docs, prefer product implications over implementation-heavy critique: "what does the reader/buyer/user need to understand?" rather than low-level verification details unless the claim materially affects product positioning.
- When a report has a stated scope, do not ask for broad additions just because related facts exist. Anchor comments to whether the missing item changes the intended product story, positioning, adoption model, or decision quality.
- When a reviewer objects to evidence phrasing, rewrite the live text to match the actual request/source of truth, not the artifact you inferred from. Example: say "Based on <team/vendor>'s request..." instead of referring to screenshots or chat artifacts unless the user explicitly wants those mentioned.
- If a comment changes the implementation source of truth (for example "no Notion review; open a GitHub PR instead"), update the document text and reply to the thread with the concrete change before resolving it.


## Anchoring pitfalls
- If exact anchors shifted or were deleted, the Drive comments API can show `Original content deleted`.
- That is still useful metadata, but it is not a reliable replacement for checking the current text.
- Drive comments are file-level; there is no explicit `tabId` on `comments.create`.
- For tab-scoped feedback in multi-tab docs, first read the target tab content (`includeTabsContent=true`) and anchor comments using quoted text that appears in that tab.
- Prefer distinctive quoted snippets (not generic headings) to reduce cross-tab mis-anchoring.
- Do not post comments with synthetic/custom anchor payloads (for example JSON heading anchors like `{\"r\":\"headings\"...}`) as a substitute for UI text highlights. These often create threads that appear as `Original content deleted` and are not bound to visible highlighted text.
- If the user asks for "highlight this exact phrase" quality, use manual-post mode: provide `Anchor snippet` + `Comment to post`, and have the user highlight text in Docs UI before posting.

## Verification
- Compare the thread, the quoted content, and the current doc text before deciding whether a comment still matters.
- Run an anchor-presence audit before closure: for each unresolved comment, count exact `quotedFileContent.value` matches in the target tab text.
  - `>=1` match: anchor still present; continue with normal intent/placement checks.
  - `0` match: treat as stale-anchor risk (content likely edited or moved). Re-anchor using a nearby distinctive snippet from current text before claiming the comment is addressed.
- Verify which artifact the reviewer is actually reading: local markdown, preview doc, or live shared tab.
- If only source/preview changed and the live tab has not been updated yet, say that explicitly instead of implying the review comment is already fixed everywhere.
- For tab-scoped runs, validate the latest posted comments by checking: author, created time, and `quotedFileContent.value` matches text unique to the intended tab.
- In multi-tab docs, run a cross-tab uniqueness check for every planned anchor snippet; if any snippet appears in another tab, replace it with more distinctive target-tab text before finalizing.
- Also do a section-placement sanity check (print nearby lines around each anchor in the target tab) so comments land in the intended subsection, not just the correct tab.
- Run an anchor-intent sanity check before finalizing: the highlighted text and the comment objective must match (for example, do not attach scoring-taxonomy feedback to a readability line just because both are in the same tab).
- If intent and anchor do not match, move the anchor to a better nearby target line and add a short `Placement note` in the manual comment pack.

## API anchoring limitation (Docs comments)

- In practice, `drive.comments.create` can post comments but may fail to create stable Docs UI-style text highlights (`kix.*` anchor + `quotedFileContent`) for new comments.
- If created comments show no `quotedFileContent` or appear as `Original content deleted`, treat them as unanchored for review workflow purposes.
- Re-trying with ad-hoc JSON anchor payloads (for example `{"r":"headings"...}`) is non-deterministic and should not be relied on for production review passes.

## API-assisted hybrid mode (recommended fallback)
Use this when API posting works but reliable text anchoring does not.

- Post comment text via API with explicit placement metadata in the body:
  - target section heading
  - exact text to highlight
  - the comment draft
- Keep one concern per comment and start with a recognizable prefix (for example `[API-assisted hybrid target]`).
- Human reviewer then re-anchors in Docs UI by highlighting the specified text and posting/moving the comment content.
- Before handoff, verify each posted comment is present by `commentId` + content prefix and report count.

## Manual-post mode (no API comments)
Use this when the user wants to post comments themselves.

- Do not create comments via API.
- Produce a local markdown “comment pack” with:
  - target doc URL + target tab id/title
  - one section per comment: `Anchor snippet` + `Comment to post`
- For product/PM exploration reviews, include a short `What I mean` note when the user is calibrating the comment before posting. Keep the posted comment itself concise and product-oriented.
- Ensure all anchor snippets are target-tab-specific (unique to that tab when possible).
- If a snippet is shared across tabs, rewrite the anchor to a nearby line unique to the target tab.
- Confirm readiness by reporting target-tab match count (for example, `10/10 in target tab, 0/10 in other tabs`).
- Do not rely on previously captured comment IDs for cleanup/export; list current comments first and verify by author + `quotedFileContent.value` because IDs/threads may have changed or been edited since the last run.

## Repo-grounded tagged comment review
Use this when a tagged Google Doc comment asks Raymond for review and a repository URL is provided as reference.

- Treat the comment anchor as the scope boundary. If the thread is anchored to Appendix A, keep final comments Appendix A-only; use related sections only as supporting context.
- Inspect the referenced repo before drafting comments. Verify default branch, current commit, actual paths/imports/dependencies, and whether the doc’s proposed paths still exist.
- Prefer repo-specific comments over generic architecture/process advice. Promote mismatches such as “doc proposes new registry but repo already has a plugin manager,” “resolver imports AIP directly,” or “UI path in doc no longer exists.”
- Return simple paste-ready comments sorted by impact. Default shape: `Highlight` + `Comment`; add `Why` only when the user asks for evaluation.
- See `references/repo-grounded-doc-comment-review.md` for the full workflow and checks.

## Tagged-comment review workflow
Use this when the user asks to “see the comment that tags me” / “review the section I was tagged on” / “provide some reviews.”

1. List Drive comments with replies and `quotedFileContent`; save the raw JSON to `/tmp` for local inspection.
2. Filter comments by the user's known handles/emails plus direct `@` mention text, then separate unresolved mention threads from other unresolved threads.
3. Read the current document text around the quoted anchor before drafting feedback. Do not rely on comment text alone.
4. Unless the user explicitly asks to post, default to manual-post mode: create a paste-ready local comment pack with one concern per comment, each with `Anchor snippet` + `Comment to post`.
5. In the handoff, state which thread tagged the user, which unresolved comments did not tag them, what section was reviewed, and the local path to the comment pack.
6. Keep the suggested comments decision/usefulness-oriented for strategy docs: governance gates, ownership, risk controls, validation criteria, rollback/incident paths, and ambiguous split boundaries usually matter more than line-level implementation nits.

## Before/after replacement mode (for reviewer threads)
Use this when the reviewer asks for exact edit instructions like "quote full before and full after".

- Do not answer with abstract guidance only.
- For each open thread, provide:
  - `Where to edit` (exact heading path)
  - `Before` (verbatim current text block from the live target tab)
  - `After` (full replacement text, ready to paste)
- Prefer replacing one complete bullet/paragraph block, not fragmented phrases.
- If the requested "before" text is not found verbatim in the target tab, say that explicitly and provide the nearest unique anchor snippet before drafting the replacement.
- Keep terminology aligned with the active review rubric (status enum, scoring bands, scope language) so reviewers can resolve threads without interpretation.

## API reply + resolve workflow (Drive API)
Use this when the user asks to "address all comments", "reply all", or "close resolved threads" after a doc refresh.

1. List current comments first and build the active unresolved set.
   - `drive.comments().list(... includeDeleted=false)`
2. Post a textual reply per thread.
   - `drive.replies().create(fileId=DOC_ID, commentId=COMMENT_ID, body={"content": "..."}, fields="id")`
3. Resolve the thread with a second reply action.
   - `drive.replies().create(fileId=DOC_ID, commentId=COMMENT_ID, body={"action": "resolve", "content": "Resolved."}, fields="id")`
4. Re-list comments and verify counts before reporting done.
   - report `total_comments`, `resolved_count`, `unresolved_count`

Notes:
- In some environments, `replies.create` requires explicit `fields` (for example `fields="id"`) or returns HTTP 400.
- Do not use `drive.comments().update(..., {"resolved": true})` as the primary resolve mechanism; it may succeed as API call shape but leave threads unresolved in Docs.
- Always verify post-action state with a fresh `comments.list` (and spot-check individual comment IDs).
- If threads remain unresolved after API resolve attempts, report the limitation and switch to manual UI resolve instructions.
- Keep reviewer voice consistent: when the author made updates, reply from reviewer perspective (for example "Thanks, this now reads clearer") rather than "Implemented" wording.
- If policy is to keep disagreements open, skip step 3 for those threads and report them separately.
