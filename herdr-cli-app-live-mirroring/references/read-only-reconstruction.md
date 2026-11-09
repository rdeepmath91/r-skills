# Fresh-context, read-only discovery and reconstruction

## Choose the verification tier

1. Metadata audit: source/native catalogs, exact attachment argv and relevant process tree, source-pane identity, app layout/labels. No terminal screenshots or reads. This can establish a bound live viewer, not conversation contents or working input.
2. Live-view acceptance: metadata plus authorized screen inspection. Do not inspect credential/setup screens merely because a tab is labelled as an agent. Reading the whole viewport can expose secrets.
3. Fresh setup acceptance: independently exercised install/authentication/registration, creation, interaction/ownership, cleanup and recovery. A read-only audit of pre-existing connections does not test these operations.

A fresh-context audit of this workflow successfully reconstructed existing remote and WSL mappings using installed documentation and live metadata, but required the discovery/join guidance below. It did not test installation, input delivery, reboot recovery or lifecycle-status synchronization. Do not present that audit as end-to-end migration validation.

## Discover executables without private context

Start with `command -v herdr hc herdr-core herdr-app` on Unix. Missing native aliases in WSL do not mean the Windows app is absent. A bounded Windows metadata query is:

    Get-CimInstance Win32_Process |
      Where-Object { $_.Name -in @('herdr-app.exe', 'herdr-core.exe') } |
      Select-Object Name,ExecutablePath

Invoke via `powershell.exe -NoProfile -NonInteractive -Command ...` when working in WSL. Pass a structured argument list, not untrusted interpolated shell text. Translate discovered Windows executable paths with `wslpath -u` or an equivalent validated conversion. Do not print all process command lines or environments.

Locate the generated app guide using the actual Windows profile path. Typical Windows paths are under the user's `.config/herdr-app/`; native core config can be under `%APPDATA%/herdr-core/`. Inspect discovered paths, not an assumed username.

Read the actual binaries' `--help`, `--skill`, and version output. Use existing `hc machine ls` connections for bounded remote metadata via `hc exec --on NATIVE_MACHINE ...` where authorized; `hc exec` starts a short metadata subprocess but must not change remote state. Never call `machine add --install` just to obtain inventory.

## Source identity and denominator

Collect source workspaces, tabs, panes and recognized agents. A pane with missing agent kind or `unknown` status is unclassified, not necessarily a shell. Keep it outside the recognized-agent denominator but report it separately.

Record initial and final source inventories. Compare both pane IDs and legacy terminal IDs; inventory survival does not prove an unchanged OS process or conversation unless those identities were also checked.

Source keys must be `(verified machine/account endpoint, legacy session, pane_id)`. Pane IDs repeat across machines and sessions. Use source labels for presentation only. Join remote native names to legacy profiles using verified account/host/session metadata; do not assume equal labels prove equal endpoints. SSH aliases can be inspected with `ssh -G ALIAS`, projecting only hostname, user, port and any relevant nonsecret routing settings.

## Native mapping recipe

For every live native terminal associated with the in-scope app spaces:

1. Read `hc get EXACT_TERMINAL` and `herdr-app ls`.
2. Inspect actual foreground argv, not just the root agent name. Login-shell wrappers are expected remotely; PowerShell wrappers are expected for Windows-to-WSL views.
3. Extract only an exact legacy invocation of `herdr [--session SESSION] agent attach PANE`, with a known source executable and verified host/account. Do not infer mappings from tab names, title strings, cwd alone, or agent kind.
4. Bind native space/tab IDs from layout to the core's `herdr.space`/`herdr.tab` labels, accounting for the remote `machine/` prefixes on app-visible IDs.
5. For Windows wrappers, compare the exact quoted command, then query only immediate descendants of the relevant launcher PID:

       Get-CimInstance Win32_Process |
         Where-Object { $_.ParentProcessId -in @(VERIFIED_LAUNCHER_PIDS) } |
         Select-Object ProcessId,ParentProcessId,Name,CommandLine

   Confirm the child wsl.exe selects the intended distro, legacy executable, session and pane. In Linux, inspect only relevant `/proc/PID/cmdline`, cwd and parent metadata to confirm the attachment exists. Avoid broad environment dumps; if session overrides must be checked, project only the specific HERDR session/config/socket variables and do not collect unrelated values.
6. Some pre-existing remote views omit `--session`. Verify effective default-session binding through installed session-list metadata and narrow process/config context. If multiple sessions or unresolved overrides exist, report the session as unknown rather than forcing a match. New viewer payloads should include an explicit session.
7. Count matches, duplicates and unmatched entries in code. One source with two viewers is a duplicate mapping, not two agents. Exclude finished native terminals explicitly, and distinguish the generic nested-TUI fallback terminal from a one-pane attachment.

Minimal record shape:

    {
      "source_machine": "verified endpoint/profile",
      "source_session": "explicit or verified-effective session",
      "source_pane": "exact pane id",
      "source_terminal": "legacy terminal identity",
      "native_machine": "native name or local",
      "native_space": "exact app id",
      "native_tab": "exact app id",
      "native_terminal": "exact core address",
      "verification": {
        "metadata_bound": true,
        "screen_checked": false,
        "input_checked": false,
        "lifecycle_reported": false
      }
    }

Keep private identities in the audit artifact, not the public skill. An audit artifact may use a scoped scratch directory with 0700/0600 permissions; a production source-to-view registry should be durable. Avoid retaining raw terminal screens when metadata is sufficient.

## Report precise results

State the observed inventory boundary and timestamp. Report recognized source agents, mapped source agents, unclassified source panes, native live attachment views, duplicates/unmatched native viewers, and lifecycle-reporting views separately. Name any gap without automatically repairing it. Changes during the audit require a refresh or an explicit unstable-inventory qualification.

A passing metadata reconstruction means another agent could discover the mapping without conversation history. It does not imply the user approved new installations or repairs, and does not establish full initial-setup portability.
