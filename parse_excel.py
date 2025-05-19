# parse_excel.py

import pandas as pd

QUARTERS = ["Q1", "Q2", "Q3", "Q4"]
INVALID_VALUES = {
    "- NIL -", "-NIL-", "NIL", "NA", "N.A.", "N.A", "", None,
    "NONE", "NOT APPLICABLE", "NAN"
}

# Helper: Checks if a value is valid (not empty or placeholder)
def is_valid(text):
    if text is None or pd.isna(text):
        return False
    normalized = str(text).strip().upper().replace(" ", "")
    return normalized not in INVALID_VALUES

# Helper: Finds a column that includes all keywords (case-insensitive)
def find_column(df, keywords: list[str]):
    for col in df.columns:
        name = col.lower()
        if all(k.lower() in name for k in keywords):
            return col
    return None

# Main parser
def parse_excel(file) -> dict:
    df = pd.read_excel(file, engine="openpyxl")
    df.columns = df.columns.str.strip().str.replace(r"\s+", " ", regex=True)

    # Try to identify required columns
    focus_col = find_column(df, ["priority", "focus"])
    updates_col = find_column(df, ["progress", "q1", "q3"])
    completion_col = find_column(df, ["completion", "date"])

    if not all([focus_col, updates_col, completion_col]):
        raise ValueError("Missing required columns: 'Priority Focus Area', 'Progress of Initiatives in Q1-Q3', or 'Completion Date'.")

    result = {q: [] for q in QUARTERS}

    for _, row in df.iterrows():
        quarter = str(row.get(completion_col, "")).strip().upper()
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