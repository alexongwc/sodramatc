# parse_excel.py


import pandas as pd

INVALID_VALUES = {
    "- NIL -", "-NIL-", "NIL", "NA", "N.A.", "N.A", "", None,
    "NONE", "NOT APPLICABLE", "NAN"
}

def is_valid(text):
    if text is None or pd.isna(text):
        return False
    normalized = str(text).strip().upper().replace(" ", "")
    return normalized not in INVALID_VALUES

def extract_quarter(row):
    for col in row.index:
        if "completion" in col.lower() and "date" in col.lower():
            value = str(row[col]).strip().upper()
            if value in ["Q1", "Q2", "Q3", "Q4"]:
                return value
    return None
