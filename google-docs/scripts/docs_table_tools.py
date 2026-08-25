#!/usr/bin/env python3
"""Small Google Docs table helpers.

Use this for operations that are safer when tables are selected by exact
header cells instead of loose substring matching.
"""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import docs_api  # noqa: E402


def paragraph_text(paragraph):
    return "".join(
        element.get("textRun", {}).get("content", "")
        for element in paragraph.get("elements", [])
    )


def iter_paragraph_elements(elements):
    for element in elements:
        if "paragraph" in element:
            yield element
        table = element.get("table")
        if table:
            for row in table.get("tableRows", []):
                for cell in row.get("tableCells", []):
                    yield from iter_paragraph_elements(cell.get("content", []))


def cell_text(cell):
    parts = []
    for element in iter_paragraph_elements(cell.get("content", [])):
        text = paragraph_text(element["paragraph"]).strip()
        if text:
            parts.append(text)
    return " ".join(parts)


def load_doc(doc_id):
    docs = docs_api.build_service("docs", "v1")
    return docs.documents().get(documentId=doc_id).execute(num_retries=5)


def iter_tables(doc):
    for element in doc.get("body", {}).get("content", []):
        table = element.get("table")
        if table:
            yield element.get("startIndex"), table


def table_header(table):
    rows = table.get("tableRows", [])
    if not rows:
        return []
    return [cell_text(cell) for cell in rows[0].get("tableCells", [])]


def find_table_by_header(doc, expected_header):
    matches = []
    for start_index, table in iter_tables(doc):
        header = table_header(table)
        if header[: len(expected_header)] == expected_header:
            matches.append((start_index, table))

    if not matches:
        observed = [table_header(table) for _start, table in iter_tables(doc)]
        raise RuntimeError(
            "No table matched exact header {}. Observed headers: {}".format(
                expected_header,
                observed,
            )
        )
    if len(matches) > 1:
        starts = [start for start, _table in matches]
        raise RuntimeError(
            "Header {} matched multiple tables at start indexes {}".format(
                expected_header,
                starts,
            )
        )
    return matches[0]


def find_row_index(table, anchor_text):
    for index, row in enumerate(table.get("tableRows", [])):
        cells = row.get("tableCells", [])
        if cells and cell_text(cells[0]) == anchor_text:
            return index

    visible = [
        cell_text(row.get("tableCells", [])[0])
        for row in table.get("tableRows", [])
        if row.get("tableCells")
    ]
    raise RuntimeError(
        "Anchor row {!r} not found. Visible first-column values: {}".format(
            anchor_text,
            visible,
        )
    )


def row_exists(table, first_cell_text):
    return any(
        row.get("tableCells") and cell_text(row["tableCells"][0]) == first_cell_text
        for row in table.get("tableRows", [])
    )


def inspect_tables(doc_id, max_rows):
    doc = load_doc(doc_id)
    result = []
    for number, (start_index, table) in enumerate(iter_tables(doc), start=1):
        rows = table.get("tableRows", [])
        sample_rows = []
        for row in rows[:max_rows]:
            sample_rows.append([cell_text(cell) for cell in row.get("tableCells", [])])
        result.append(
            {
                "number": number,
                "startIndex": start_index,
                "header": table_header(table),
                "rowCount": len(rows),
                "sampleRows": sample_rows,
            }
        )
    print(json.dumps(result, indent=2, ensure_ascii=False))


def insert_rows(doc_id, header, anchor, rows, insert_below, dry_run):
    docs = docs_api.build_service("docs", "v1")
    doc = load_doc(doc_id)
    table_start, table = find_table_by_header(doc, header)
    anchor_index = find_row_index(table, anchor)

    print(
        json.dumps(
            {
                "docId": doc_id,
                "tableStartIndex": table_start,
                "header": table_header(table),
                "anchor": anchor,
                "anchorRowIndex": anchor_index,
                "insertBelow": insert_below,
                "rows": rows,
                "dryRun": dry_run,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    if dry_run:
        return

    ordered_rows = list(rows)
    if insert_below:
        ordered_rows = list(reversed(ordered_rows))

    for row in ordered_rows:
        doc = load_doc(doc_id)
        table_start, table = find_table_by_header(doc, header)
        if row_exists(table, str(row[0])):
            print("skip existing row: {}".format(row[0]))
            continue
        anchor_index = find_row_index(table, anchor)
        target_index = anchor_index + 1 if insert_below else anchor_index
        docs.documents().batchUpdate(
            documentId=doc_id,
            body={
                "requests": [
                    {
                        "insertTableRow": {
                            "tableCellLocation": {
                                "tableStartLocation": {"index": table_start},
                                "rowIndex": anchor_index,
                                "columnIndex": 0,
                            },
                            "insertBelow": insert_below,
                        }
                    }
                ]
            },
        ).execute(num_retries=5)

        doc = load_doc(doc_id)
        _table_start, table = find_table_by_header(doc, header)
        new_cells = table["tableRows"][target_index].get("tableCells", [])
        requests = []
        for value, cell in reversed(list(zip(row, new_cells))):
            start = cell["content"][0]["startIndex"]
            requests.append(
                {"insertText": {"location": {"index": start}, "text": str(value)}}
            )
        docs.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": requests},
        ).execute(num_retries=5)
        print("inserted row: {}".format(row[0]))


def load_rows_arg(args):
    if args.rows_json:
        return json.loads(args.rows_json)
    if args.rows_file:
        return json.loads(Path(args.rows_file).read_text())
    raise SystemExit("Provide --rows-json or --rows-file")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect = subparsers.add_parser("inspect", help="Print tables, headers, and sample rows")
    inspect.add_argument("doc_id")
    inspect.add_argument("--max-rows", type=int, default=5)

    insert = subparsers.add_parser("insert-rows", help="Insert rows by strict header and anchor")
    insert.add_argument("doc_id")
    insert.add_argument("--header-json", required=True, help='Example: ["Time (UTC+7)", "Event"]')
    insert.add_argument("--anchor", required=True, help="Exact first-cell text of anchor row")
    insert.add_argument("--rows-json", help='Example: [["2026-01-01", "Event"]]')
    insert.add_argument("--rows-file", help="JSON file containing an array of rows")
    insert.add_argument("--above", action="store_true", help="Insert above anchor instead of below")
    insert.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()
    if args.command == "inspect":
        inspect_tables(args.doc_id, args.max_rows)
    elif args.command == "insert-rows":
        insert_rows(
            args.doc_id,
            json.loads(args.header_json),
            args.anchor,
            load_rows_arg(args),
            insert_below=not args.above,
            dry_run=args.dry_run,
        )


if __name__ == "__main__":
    main()
