# Account binding + heading formatting pitfalls (session note)

Context:
- `gform.py` posts JSON to Apps Script Web App URL from `GFORMS`.
- This flow does not perform per-user OAuth switching during create/list/get.

Key behavior:
1) Account ownership is bound to the Apps Script deployment account (`Execute as: Me`).
2) Creating forms under another account requires redeploying the same script while logged into that target account, then updating `GFORMS`.
3) OAuth tokens used by other tools (Docs/Drive) do not change ownership of forms created through this web-app flow.

Formatting issue observed:
- Passing description text containing literal `\\n` (backslash + n) stores escaped characters visibly in Forms.
- Use real newline characters in payload strings when multiline descriptions are desired.

Verification recipe:
1) `python3 scripts/gform.py list`
2) Open one returned edit URL and confirm active avatar/account in Forms UI
3) `python3 scripts/gform.py get <FORM_ID>` and ensure description does not contain literal `\\n`
