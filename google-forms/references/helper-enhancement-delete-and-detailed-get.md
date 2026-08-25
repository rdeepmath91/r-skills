# Google Forms helper enhancement: delete questions and detailed get

Use this when the current Apps Script web-app helper is too limited for in-place form cleanup.

## Why this matters
The deployed helper may support `get`, `list`, `addQuestions`, and `responses`, but not deletion or option-level inspection. Google Forms itself can delete items, and Apps Script can delete items with `form.deleteItem(index)`; the limitation is the deployed helper contract, not Google Forms.

Avoid saying “I can’t delete questions” as a general claim. Say: “the current deployed helper does not expose a delete action.”

## Minimal Apps Script additions
Add actions to `doPost`:

```js
case 'deleteQuestion':
  return deleteQuestion(payload);
case 'getDetailed':
  return getDetailed(payload);
```

Add delete support with guardrails:

```js
function deleteQuestion(p) {
  var formId = requireFormId(p, 'deleteQuestion');
  var form = FormApp.openById(formId);
  var index = Number(p.index);
  if (isNaN(index)) return respond({ error: 'Missing numeric index' });

  var items = form.getItems();
  if (index < 0 || index >= items.length) {
    return respond({ error: 'No item at index ' + index, questionCount: items.length });
  }

  var item = items[index];
  var title = item.getTitle();
  var type = String(item.getType());
  form.deleteItem(index);

  return respond({
    status: 'deleted',
    formId: formId,
    index: index,
    title: title,
    type: type,
    questionCount: form.getItems().length
  });
}
```

Add detailed inspection for choices / native Other state where supported:

```js
function getDetailed(p) {
  var formId = requireFormId(p, 'getDetailed');
  var form = FormApp.openById(formId);
  var items = form.getItems().map(function(it, i) {
    var out = { index: i, type: String(it.getType()), title: it.getTitle() };
    try {
      if (it.getType() === FormApp.ItemType.MULTIPLE_CHOICE) {
        var mc = it.asMultipleChoiceItem();
        out.required = mc.isRequired();
        out.choices = mc.getChoices().map(function(c) {
          return { value: c.getValue(), isOther: typeof c.isOther === 'function' ? c.isOther() : false };
        });
      } else if (it.getType() === FormApp.ItemType.CHECKBOX) {
        var cb = it.asCheckboxItem();
        out.required = cb.isRequired();
        out.choices = cb.getChoices().map(function(c) {
          return { value: c.getValue(), isOther: typeof c.isOther === 'function' ? c.isOther() : false };
        });
      } else if (it.getType() === FormApp.ItemType.TEXT) {
        out.required = it.asTextItem().isRequired();
      } else if (it.getType() === FormApp.ItemType.PARAGRAPH_TEXT) {
        out.required = it.asParagraphTextItem().isRequired();
      }
    } catch (err) {
      out.detailError = String(err);
    }
    return out;
  });

  return respond({
    title: getFormTitle(form, formId),
    description: form.getDescription(),
    responderUri: form.getPublishedUrl(),
    editUri: form.getEditUrl(),
    questionCount: items.length,
    questions: items
  });
}
```

## Python helper additions
Add functions:

```python
def cmd_delete_question(form_id: str, index: int):
    return post_and_follow({'action': 'deleteQuestion', 'formId': form_id, 'index': index})

def cmd_get_detailed(form_id: str):
    return post_and_follow({'action': 'getDetailed', 'formId': form_id})
```

Then wire CLI commands:

```python
elif cmd == 'delete-question':
    print(cmd_delete_question(sys.argv[2], int(sys.argv[3])))
elif cmd == 'get-detailed':
    print(cmd_get_detailed(sys.argv[2]))
```

## Verification after deletion
Run:

```bash
python3 scripts/gform.py get FORM_ID
python3 scripts/gform.py responses FORM_ID
```

Confirm:
1. `questionCount` decreased as expected.
2. The deleted title is absent.
3. The `responderUri` is unchanged.
4. Response count is checked before/after if preserving responses matters.

## Edit URL pattern
If Drive metadata is unavailable or times out, the Google Forms edit URL can be derived from the form ID:

```text
https://docs.google.com/forms/d/FORM_ID/edit
```

Validate the form itself through `gform.py get FORM_ID` and, when possible, Drive metadata `webViewLink`.