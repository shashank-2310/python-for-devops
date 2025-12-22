import json
import pandas as pd
from pathlib import Path

"""
    Convert a Kitsu API payload (dict) into a flat pandas DataFrame
    containing selected fields for easy consumption (CSV/JSON/printing).

    Only the chosen fields are extracted to keep output concise.
"""


def to_dataframe(payload: dict) -> pd.DataFrame:
    rows = []
    #Iterate through the list of items in the API response
    for item in payload.get("data", []):
        id = item.get("id")
        
        #Nested attributes
        attrs = item.get("attributes", {}) or {}
        titles = attrs.get("titles", {}) or {}
        
        status = attrs.get("status", "") or ""
        startDate = attrs.get("startDate", "") or ""
        endDate = attrs.get("endDate", "") or ""
        ageRating = attrs.get("ageRating", "") or ""
        avgRating = str(float(attrs["averageRating"])) if attrs.get("averageRating") else None
        rank = attrs.get("popularityRank", "") or ""
        desc = attrs.get("description", "") or ""
        
        #Local truncation helper to keep text readable in terminal/JSON
        def truncate(text: str, maxlen: int = 160) -> str:
            if isinstance(text, str) and len(text) > maxlen:
                return text[: maxlen - 1] + "..."
            return text
        
        row = {
            "id": id,
            "title_en": titles.get("en"),
            "title_en_jp": titles.get("en_jp"),
            "status": status,
            "startDate":startDate,
            "endDate": endDate,
            "ageRating": ageRating,
            "avgRating": avgRating,
            "rank": rank,
            "description": truncate(desc) if desc else None
        }
        rows.append(row)
        
    return pd.DataFrame(rows)

def pretty_print(df: pd.DataFrame) -> None:
    if df.empty:
        print("No data to show")
        return
    
    #Fields to display
    cols_to_show = [
        "id",
        "title_en",
        "title_en_jp",
        "status",
        "startDate",
        "endDate",
        "ageRating",
        "avgRating",
        "rank",
        "description"
    ]
    
    #Keep only columns that exist
    cols = [c for c in cols_to_show if c in df.columns]
    cpy_df = df[cols].copy()
    
    #Truncate long strings in the display like description
    def truncate(x, n=160):
        return (x[: n - 1] + "…") if isinstance(x, str) and len(x) > n else x #Only truncate strings > 160 char
    
    #Iterate through each column and replace with truncated version
    for c in cpy_df.columns:
        cpy_df[c] = cpy_df[c].map(lambda v: truncate(v))
    
    #Convert to list of dicts (records)
    records = cpy_df.to_dict(orient="records")
    print("\n============================== Anime Info ==============================\n")
    print(json.dumps(records, ensure_ascii=False, indent=2))

    
CSV_FILE = "anime_items.csv"
JSON_FILE = "anime_raw.json"

def save_output(df: pd.DataFrame) -> None:
    base_dir: Path = Path(__file__).parent
    csv_path: Path = base_dir / "anime_items.csv"
    json_path: Path = base_dir / "anime_items.json"

    #CSV file: append if exists, else create with header
    csv_exists = csv_path.exists() and csv_path.stat().st_size > 0
    df.to_csv(
        csv_path,
        mode="a" if csv_exists else "w",
        header=not csv_exists,
        index=False,
        encoding="utf-8",
    )
    print(f"Saved items to {csv_path} ({'appended' if csv_exists else 'created'}) with {len(df)} new rows.")

    #JSON file: convert df to a list of dicts or records & pretty dump
    records = df.to_dict(orient="records")

    # Append to JSON array across runs:
    data = []
    if json_path.exists():
        try:
            with json_path.open("r", encoding="utf-8") as f: #r = read mode
                existing = json.load(f)
                if isinstance(existing, list): #checking if the variable existing is a list
                    data = existing  #reuse the existing list
                elif existing:  #if it is a dict or non-empty
                    data = [existing]  #wrap it in a list
        except Exception:
            data = []
    data.extend(records) #extend => add all elements from records into data 1 by 1

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved selected fields to {json_path} (array of {len(data)} records).")