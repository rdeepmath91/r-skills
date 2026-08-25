# Weekly report cron log troubleshooting

Session-derived notes for the `weekly-report` cron job.

## What to inspect

- Cron output lives under `~/.hermes/cron/output/61638bd56cfa/` for the weekly report auto-fill job.
- Confirm the job name before debugging. The weekly report job and the Gmail digest job are separate cron jobs and can fail for different reasons.
- For a failed weekly report run, read the most recent `.md` output file first, then inspect the auth/token files referenced by the prompt.

## Observed failure pattern

- The weekly report job can fail during Google auth/token setup before any doc editing happens.
- In the captured logs, the failure was not a plaintext password leak. It was an OAuth/token problem.
- The report job used the report automation skill to gather PRs, metrics, meetings, and report text, then stopped at Google auth blockers.

## Token checks that mattered

- `~/.hermes/google_token.json` may only have `drive.file`, which is enough for docs the app created but not enough for broad Drive search or copying the live report.
- `~/.hermes/google_forms_token.json` can fail refresh with `invalid_client`.
- `~/.hermes/google_workspace_full_token.json` can fail refresh with `invalid_grant`.
- If Gmail is unavailable from the current token, do not claim Gmail was searched; fall back to Drive search and say Gmail is unavailable.

## Practical takeaways

- Do not expect report logs to contain a password; look for scope/token errors instead.
- If the cron job name says `Weekly report auto-fill and validation`, you are in the report automation path, not Gmail digest.
- Use the current token scopes as the first diagnostic step before assuming the report logic is broken.

## User-facing verification rule

When Raymond asks whether the weekly report cron ran, do not stop at `cronjob list` / `last_status: ok`. Read the latest output file under `~/.hermes/cron/output/61638bd56cfa/`, extract the target Google Doc title and URL from the `## Response` section, then verify the actual Doc content with Docs API readback before answering if he asks for the result. A useful answer should include:

- the document URL and title
- whether the relevant sections were filled, not just that the cron exited successfully
- remaining placeholder count, especially whether Technology/Business is still `(please insert here)`
- PR/meeting/key-metrics counts when present
- any validation caveat from the output, such as Drive metadata/export being blocked while Docs API readback succeeded

If the output timestamp differs slightly from `last_run_at`, prefer the newest file from the cron output directory rather than constructing a filename from `last_run_at`.
