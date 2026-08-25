# Setup And Dependencies

Use this reference before running Google Docs scripts in a new environment, after `ModuleNotFoundError`, or when a workflow needs extra render/audit tooling.

## Minimum Setup Sequence

1. Choose the Python interpreter for the task.
2. Verify or install required Python packages in that interpreter.
3. Verify Google OAuth credentials and scopes when Docs/Drive access is needed.
4. Verify external CLIs only for the workflow that needs them.
5. Run the smallest meaningful validation command before touching important live docs.

Do not install packages into an externally managed system Python. Use the repo, skill, or user virtualenv; create one if needed.

`scripts/setup.py` does not auto-install dependencies. If dependencies are missing, it prints the exact install command for the interpreter you used and exits.

## Python Packages

Core Google Docs/Drive scripts need:

```bash
python -m pip install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib httplib2
```

Image, PDF, and diagram helpers may also need:

```bash
python -m pip install Pillow pypdf PyMuPDF cairosvg
```

`PyMuPDF` is preferred for PDF rendering, but `scripts/render_pdf_contact_sheets.py` can fall back to `pdftoppm` plus Pillow when `PyMuPDF` is unavailable.

## OAuth And API Access

Required Google APIs:

- Google Docs API
- Google Drive API

Current skill scripts require these OAuth scopes:

- `https://www.googleapis.com/auth/documents`
- `https://www.googleapis.com/auth/drive`

Why both are required:

- `documents` is needed for Docs API reads, writes, headings, section edits, tab operations, orientation, and style updates.
- `drive` is needed for Drive import/export, Markdown-to-native-Doc publishing, PDF export, image upload/insertion, file lookup, file rename/update, and refreshing existing docs not necessarily created by this OAuth app.

`drive.file` is not enough for the current reusable workflows because many tasks operate on existing shared docs, export PDFs, list or update Drive files, and upload assets. A narrower-scope variant would require script changes and stricter assumptions about app-created files; do not tell users `drive.file` is supported by this skill unless the scripts have been changed and smoke-tested for that mode.

Use `references/auth-and-setup.md` for OAuth client creation, token storage, refresh, revoke, and troubleshooting.

Readiness check:

```bash
python <skill-root>/scripts/setup.py --check
```

Treat `setup.py --check` as a write-readiness and scope check, not only a token-presence check.

## Capability Matrix

| Workflow | Minimum setup | Validation command |
| --- | --- | --- |
| Read/write existing Google Docs | Python Google packages, OAuth token with Docs/Drive scopes | `python <skill-root>/scripts/setup.py --check` |
| Publish Markdown folder | Read/write setup plus source Markdown folder | `python -m py_compile <skill-root>/scripts/publish_pipeline.py` |
| Update or inspect one doc | Read/write setup | `python <skill-root>/scripts/docs_api.py --help` |
| Insert or resize images | Read/write setup plus `Pillow` | `PYTHONPATH=<skill-root>/scripts python -c "import docs_advanced"` |
| Render Mermaid | Node.js/npm/npx plus Mermaid CLI runtime | `npx --yes @mermaid-js/mermaid-cli@11.4.3 --version` |
| Render HTML diagrams | Chrome/Chromium binary plus `Pillow` | `python <skill-root>/scripts/render_html_assets.py --help` |
| Render Graphviz diagrams | `dot` from Graphviz | `dot -V` |
| SVG-to-PNG workaround | `cairosvg` plus Graphviz if source is DOT/SVG | `python -c "import cairosvg"` |
| PDF text audit | `pypdf` | `python -c "import pypdf"` |
| PDF visual/contact-sheet audit | `Pillow` plus `PyMuPDF` or `pdftoppm` | `python <skill-root>/scripts/render_pdf_contact_sheets.py --help` |
| DOCX fallback import | Pandoc | `pandoc --version` |

## External CLI Notes

- Mermaid rendering usually uses `npx --yes @mermaid-js/mermaid-cli@11.4.3` with a Puppeteer config containing `{"args": ["--no-sandbox"]}`.
- HTML rendering uses the first available Chrome binary from `google-chrome`, `google-chrome-stable`, `chromium`, or `chromium-browser`.
- PDF contact sheets use `PyMuPDF` when installed; otherwise install `poppler-utils` so `pdftoppm` is on `PATH`.
- Graphviz is only needed for DOT assets; do not require it for normal Markdown-only publishing.
- Pandoc is only needed for the DOCX fallback when Markdown import is flaky.

## Minimal Smoke Tests

Run only the smoke tests needed for the current workflow:

```bash
python <skill-root>/scripts/setup.py --check
python <skill-root>/scripts/docs_api.py --help
python <skill-root>/scripts/render_pdf_contact_sheets.py --help
python -m py_compile <skill-root>/scripts/*.py
```

For a real API path test, create a throwaway doc, update it with a tiny Markdown file, read it back, then delete or trash it according to the workspace policy. Use this only when script wiring changed or auth behavior is uncertain.

## First-Time Setup Simulation (safe dry run)

When you need to validate first-time UX without touching existing credentials, run setup with an isolated home:

```bash
TMP_HOME=$(mktemp -d /tmp/gdocs-firsttime-XXXX)
HERMES_HOME="$TMP_HOME" python <skill-root>/scripts/setup.py --check
HERMES_HOME="$TMP_HOME" python <skill-root>/scripts/setup.py --auth-url
```

Expected behavior:
- `--check` reports `NOT_AUTHENTICATED` with guided next steps.
- `--auth-url` fails clearly until `--client-secret` is provided.

Then provide a client-secret file and re-test:

```bash
HERMES_HOME="$TMP_HOME" python <skill-root>/scripts/setup.py --client-secret /path/to/client_secret.json
HERMES_HOME="$TMP_HOME" python <skill-root>/scripts/setup.py --check
HERMES_HOME="$TMP_HOME" python <skill-root>/scripts/setup.py --auth-url
```

This confirms first-time setup messaging and file wiring (`google_client_secret.json`, `google_oauth_pending.json`) without mutating the user's real `~/.hermes` token state.
