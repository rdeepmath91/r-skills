# Local WSL agents as individual Windows native-app tabs

## Discovery

Verify the actual WSL distribution, Linux user/cwd, legacy session and pane IDs. `WSL_DISTRO_NAME` may be absent from a tool daemon; that does not prove the shell is not WSL. Use `wsl.exe --list --quiet` or another permitted system lookup and handle UTF-16 output correctly.

Find the actual legacy binary with `command -v herdr`. Read local `herdr agent list`, `workspace list`, and `tab list --workspace LIVE_ID`. Recheck current pane and session identity. Retain the original nested-TUI tab as fallback.

Read `herdr-app commands` for the installed `space.new`/`tab.new` schema. Supply explicit machine `""` to document that this is a local space. In the tested app, scripted `space.new` defaults to local; interactive keys and clicks follow the focused space's machine. Do not claim that scripts implicitly follow another client's remote selection; verify the installed command contract.

## Payload

Create a local native space, keeping a Windows-valid folder for core while selecting the Linux working directory inside wsl.exe:

    {
      "name": "SOURCE_WORKSPACE_LABEL",
      "machine": "",
      "folder": "C:\\Users\\WINDOWS_USER",
      "tab": "SOURCE_TAB_LABEL",
      "argv": [
        "C:\\Windows\\System32\\wsl.exe",
        "--distribution", "DISTRO_NAME",
        "--cd", "/home/LINUX_USER/SOURCE_CWD",
        "--exec", "/absolute/linux/path/herdr",
        "--session", "SOURCE_SESSION",
        "agent", "attach", "SOURCE_PANE_ID"
      ]
    }

These are placeholders. Discover actual paths, do not assume Windows is installed at C:\\Windows. Pass the payload as one encoded argument using a structured subprocess argv. Reuse the returned space ID for subsequent `tab.new` commands; preserve source tab names and use explicit source pane IDs.

This opens a live viewer, not a new Hermes/Codex instance. It requires no local SSH daemon and no extra Linux core endpoint.

## Windows launcher wrapping is expected

The tested native app wrapped explicit local argv as:

    powershell.exe -NoExit -Command "& '...wsl.exe' '...'"

Thus `hc get` may show PowerShell as root and foreground, not wsl.exe/herdr. Do not fail verification solely because root argv differs from the requested array.

Verify the wrapper's exact command against properly quoted requested arguments; verify its child wsl.exe command through bounded `Win32_Process` parent/child inspection; then confirm the corresponding Linux `/proc` argv is the intended legacy attachment for the session and pane. Inspect only relevant process metadata, not full environment dumps.

Combine process identity with a bounded `hc read TERMINAL --lines 0`, source-pane survival, and native layout readback. Never accept a generic live PowerShell shell as proof of a successful attachment. Do not submit draft user input as a test.

Native lifecycle status may remain null, just like remote live attachments. Report that limitation. The source process remains under WSL terminal Herdr, so Windows/WSL shutdown still interrupts it; this viewing arrangement does not provide uninterrupted execution across reboot.
