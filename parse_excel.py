# parse_excel.py

import pandas as pd

QUARTERS = ["Q1", "Q2", "Q3", "Q4"]

def parse_excel(file) -> dict:
    df = pd.read_excel(file, engine="openpyxl")

    # Clean headers
    df.columns = df.columns.str.strip().str.replace(r"\s+", " ", regex=True)

    try:
        focus_col = next(col for col in df.columns if "priority focus area" in col.lower())
        updates_col = next(col for col in df.columns if "workplan initiatives updates" in col.lower())
        completion_col = next(col for col in df.columns if "completion date" in col.lower())
    except StopIteration:
        raise ValueError("Missing expected columns: 'Priority Focus Area', 'Workplan Initiatives Updates', or 'Completion Date'.")

    result = {q: [] for q in QUARTERS}

    for _, row in df.iterrows():
        quarter = str(row.get(completion_col, "")).strip()
        if quarter not in QUARTERS:
            continue

        title = str(row.get(focus_col, "")).strip()
        content = str(row.get(updates_col, "")).strip()

        # Skip if either field is empty or marked as -NIL-
        if not title or not content:
            continue
        if "-NIL-" in title.upper() or "-NIL-" in content.upper():
            continue

        result[quarter].append({
            "section_title": title,
            "content": content
        })

    # Filter out quarters with no valid entries
    return {q: entries for q, entries in result.items() if entries}