# Image Sizing and Inline Object Constraints

## API Limitation: Cannot Resize Existing Images

The Google Docs API does **not** support `updateInlineObjectProperties`.

Verified by inspecting the API discovery document:
- `InsertInlineImageRequest` exists
- `DeletePositionedObjectRequest` exists
- `UpdateInlineObjectPropertiesRequest` does **not** exist

This means once an image is inserted, its display size can only be changed manually in the Google Docs editor.

## Prevention

Compute the correct size at insertion time:

```python
docs_advanced.insert_image(
    doc_id,
    image_path,
    start_index=...,
    width_pts=440,   # portrait max
    height_pts=...,  # computed from aspect ratio
)
```

## Recommended Size Caps

| Orientation | Max Width | Max Height | When to use |
|-------------|-----------|------------|-------------|
| Portrait (default) | 440 pt | ~360 pt | Most inline diagrams |
| Landscape section | 620 pt | ~420 pt | Only when width is the true constraint |

## Detection

Find oversized images by reading `inlineObjects` from the doc structure:

```python
inline_objects = doc.get('inlineObjects', {})
for obj_id, obj in inline_objects.items():
    size = obj.get('inlineObjectProperties', {}).get('embeddedObject', {}).get('size', {})
    w = size.get('width', {}).get('magnitude', 0)
    h = size.get('height', {}).get('magnitude', 0)
    if w > 440:
        print(f'OVERSIZED {obj_id}: {w}x{h}')
```

## Manual Fix (Editor Required)

1. Open the Google Doc
2. Click the image
3. Image options → Size & Rotation
4. Set width to 440pt (height auto-adjusts)

## Empty Paragraph Gaps Around Images

Markdown import and API insertion often leave empty `NORMAL_TEXT` paragraphs between images and captions or between consecutive images.

### Detection

Scan the doc structure for paragraphs with:
- No text content
- No inline objects
- Located between structural elements (images, headings, tables)

### Fix Pattern

Delete from bottom to top so indices do not shift:

```python
for start, end in reversed(empty_ranges):
    batchUpdate(doc_id, {
        'deleteContentRange': {
            'range': {'startIndex': start, 'endIndex': end}
        }
    })
```

## Related

- `references/command-recipes.md` for full image insertion workflow
- `references/preview-validation.md` for diagram sizing matrix
