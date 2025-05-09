# parse_excel.py

import pandas as pd

QUARTERS = ["Q1", "Q2", "Q3", "Q4"]
INVALID_VALUES = {
    "- NIL -", "-NIL-", "NIL", "NA", "N.A.", "N.A", "", None,
    "NONE", "NOT APPLICABLE", "NAN"
}

def is_valid(text):
    if text is None or pd.isna(text):
        return False
    normalized = str(text).strip().upper().replace(" ", "")
    return normalized not in INVALID_VALUES

def parse_excel(file) -> dict:
    df = pd.read_excel(file, engine="openpyxl")
    df.columns = df.columns.str.strip().str.replace(r"\s+", " ", regex=True)

    try:
        focus_col = next(col for col in df.columns if "priority focus area" in col.lower())
        updates_col = next(col for col in df.columns if "workplan initiatives updates" in col.lower())
        completion_col = next(col for col in df.columns if "completion date" in col.lower())
    except StopIteration:
        raise ValueError("Missing required columns: 'Priority Focus Area', 'Workplan Initiatives Updates', or 'Completion Date'.")

    result = {q: [] for q in QUARTERS}

    for _, row in df.iterrows():
        quarter = str(row.get(completion_col, "")).strip()
        if quarter not in QUARTERS:
            continue

        title = row.get(focus_col, "")
        content = row.get(updates_col, "")

        if not (is_valid(title) and is_valid(content)):
            continue

        result[quarter].append({
            "section_title": str(title).strip(),
            "content": str(content).strip()
        })

    return {q: entries for q, entries in result.items() if entries}