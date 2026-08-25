# Sandbox Daily Tracking from Cross-Repo PRs

Use this when drafting a GL Sandbox daily update from `ai-agent-platform`, `glaip-sdk`, or related repositories.

## Scope gate

Include only work with a direct sandbox contract or operational effect:

- E2B or OpenSandbox runtime behavior
- sandbox lifecycle, leasing, expiry, filesystem, templates, or custom-tool execution
- sandbox provider configuration in AIP/SDK
- AIP Helm/runtime configuration that connects AIP to a sandbox deployment

Exclude generic agent, model-client, document-agent, skills, or tool-union work unless the PR evidence explicitly shows a sandbox impact. Do not include an item merely because tests happened to run inside a sandbox.

## Discovery workflow

1. Read the live tracking document first and identify its date, section shape, and existing carry-over items.
2. Search both open/WIP and merged PRs for the target date across all named repositories.
3. Do not rely only on title/body keyword searches such as `E2B`, `AWS`, or `helm`. Also inspect recently merged PR file paths for deployment and Helm changes; operational PR titles may look like credential/config maintenance.
4. Read each candidate PR body, changed files, merge time, review state, mergeability, and checks.
5. Separate statuses precisely:
   - `MERGED`: merged in GitHub, but not necessarily released or deployed
   - `WIP`: draft, review-required, changes-requested, conflicting, or CI-pending/failing
   - `RELEASED` / `DEPLOYED`: use only with separate release or live-deployment evidence
6. Produce paste-ready text first. Do not edit the live tracking Doc unless explicitly asked.

## Labeling

Use labels that state both sandbox provider and owning surface:

- `[Sandbox – E2B] [AIP Runner]`
- `[Sandbox – OpenSandbox] [AIP Platform]`
- `[Sandbox – OpenSandbox] [GL AIP SDK]`
- `[Sandbox – E2B on AWS] [AIP Helm Deployment]`

Avoid ambiguous labels such as `[AIP – E2B]`; they do not explain whether the work is runtime behavior, SDK support, infrastructure, or deployment configuration.

## Infrastructure versus consumer configuration

Do not say an AIP PR “deployed E2B on AWS” when it only updates AIP Helm values, domains, or credentials to consume an E2B environment deployed elsewhere.

Preferred wording:

> Connected the AIP development runner to the new self-hosted E2B deployment by updating its Helm configuration with the new domain and credentials.

Then cite the PR and mention verified flows from its body. State clearly that the PR integrates AIP with the deployment rather than provisioning the AWS infrastructure itself.

## Output shape

1. `Current Issues / Notes`: sandbox-only WIP/blockers with exact live state.
2. `Achievements Today`: sandbox-only merged work; avoid release/deployment claims without evidence.
3. `Next Action Items`: review, rebase, CI, merge, release, deployment, or live validation steps grounded in the PR state.

When a broad AIP item is excluded, do not append an “optional broader AIP work” list if the user requested sandbox-only reporting.