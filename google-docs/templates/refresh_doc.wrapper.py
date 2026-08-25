#!/usr/bin/env python3
"""
Generic refresh wrapper starter for repeated Google Docs preview refreshes.

This file is intentionally project-agnostic:
- no hardcoded doc IDs
- no hardcoded headings
- all per-project values loaded from JSON config

Pair with templates/refresh_doc.config.example.json.
"""

import argparse
import json
import os
import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd), check=True)


def run_capture(cmd: list[str], cwd: Path) -> str:
    print("$", " ".join(cmd))
    cp = subprocess.run(cmd, cwd=str(cwd), check=True, stdout=subprocess.PIPE, text=True)
    return cp.stdout


def load_config(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "docs" not in data or not isinstance(data["docs"], dict) or not data["docs"]:
        raise ValueError("Config must include non-empty 'docs' map")
    return data


def main() -> int:
    p = argparse.ArgumentParser(description="Config-driven docs refresh wrapper starter")
    p.add_argument("--config", required=True, help="Path to JSON config")
    p.add_argument("--repo-root", default=".", help="Repo root for relative source paths")
    p.add_argument("--doc-key", default="", help="Refresh a single key from config.docs")
    p.add_argument("--python", default="python3", help="Python executable with google deps")
    args = p.parse_args()

    cfg_path = Path(args.config).resolve()
    repo_root = Path(args.repo_root).resolve()
    cfg = load_config(cfg_path)

    skill_root = Path(os.environ.get("GDOCS_SKILL_ROOT", "")).resolve() if os.environ.get("GDOCS_SKILL_ROOT") else None
    if not skill_root:
        # Common local default when OpenCode skill path is symlinked to Hermes skill path.
        skill_root = Path.home() / ".config" / "opencode" / "skill" / "google-docs"

    if not (skill_root / "scripts" / "docs_api.py").exists():
        raise FileNotFoundError(f"google-docs skill scripts not found under {skill_root}")

    keys = [args.doc_key] if args.doc_key else list(cfg["docs"].keys())

    for key in keys:
        item = cfg["docs"][key]
        doc_id = item["doc_id"]
        source = (repo_root / item["source"]).resolve()
        if not source.exists():
            raise FileNotFoundError(f"Missing source for {key}: {source}")

        print(f"\n=== refresh: {key} ===")
        # Minimal baseline: in-place markdown refresh + export.
        # For full deterministic image/orientation sequence, extend this wrapper
        # with your preferred project-local pass ordering.
        run(
            [
                args.python,
                str(skill_root / "scripts" / "docs_api.py"),
                "update",
                doc_id,
                "--md",
                str(source),
            ],
            cwd=repo_root,
        )

        out_md = repo_root / f"{key}_preview_latest.md"
        md_text = run_capture(
            [
                args.python,
                str(skill_root / "scripts" / "docs_api.py"),
                "get",
                doc_id,
                "--md",
            ],
            cwd=repo_root,
        )
        out_md.write_text(md_text, encoding="utf-8")

    print("\nRefresh pass complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
