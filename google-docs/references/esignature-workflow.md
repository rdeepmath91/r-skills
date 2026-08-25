# Google Docs eSignature workflow

Use when a user asks how to request or complete signatures from Google Docs/Drive, especially inside an organization-managed Google Workspace account.

## Availability

Google Docs/Drive eSignature is available only for eligible plans. Google currently lists availability for:

- Workspace Individual
- Business Standard and Business Plus
- Enterprise Starter, Standard, and Plus
- Enterprise Essentials and Enterprise Essentials Plus
- Education Plus users

For organization-managed Google Workspace accounts, the administrator must enable the feature. If the user does not see `Tools -> eSignature` in Google Docs or `Menu -> eSignature` on a PDF in Drive, first suspect plan/admin availability rather than user error.

## Request signatures from a Google Doc

1. Open the source Google Doc.
2. Open `Tools -> eSignature`.
3. In the side panel, use `Manage signers` to add signer labels. Google supports up to 10 signers per request.
4. For each signer, insert required fields such as Signature, Initials, Name, Date signed, or text fields.
5. Confirm every field is assigned to the correct signer.
6. Click `Request signature`.
7. Enter actual signer email addresses, add an optional message, enable automatic reminders if desired, select audit-trail locale if shown, then click `Request signature`.

Google generates a locked PDF copy for the signing request and emails signers. The original Google Doc remains editable and is not automatically shared with signers as part of the request.

## Request signatures from a PDF in Drive

1. Open the PDF in Google Drive viewing mode.
2. Open `Menu -> eSignature`.
3. Add signers and fields in the side panel.
4. Save changes if using the PDF as a reusable template, or click `Request signature` to send.

## After sending

- Track status from the generated PDF: open it in Drive, then `Menu -> eSignature` or `View details`.
- The request PDF is locked while the request is active. To change content or fields, cancel the request, edit the source Google Doc/PDF, and send a new request.
- When all signers complete, Google creates the final signed PDF in the requester's Drive folder and includes an audit trail page.
- Signers receive email links and get their own copy of the final signed PDF in My Drive.

## Signing flow for recipients

1. Open the request email.
2. Follow the link and click `Start signing`.
3. Complete assigned fields.
4. Create a signature by typing or drawing, then click `Adopt and sign`.
5. Click `Mark Complete` after all required fields are filled.

Recipients may reject instead; the requester receives an email notification.

## Compliance caveat

Phrase carefully: Google Docs eSignature is an electronic signature workflow with an audit trail. Do not imply it is the same as certificate-based/PKI digital signing or that it satisfies a particular legal/compliance standard unless the user provides their jurisdiction/policy requirements or official org guidance.