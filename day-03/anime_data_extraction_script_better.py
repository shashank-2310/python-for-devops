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
    try:
        items = payload.get("data", []) or []
    except Exception as e:
        print(f"to_dataframe: invalid payload provided: {e}")
        return pd.DataFrame(rows)

    #Iterate through the list of items in the API response
    for item in items:
        try:
            id = item.get("id")

            #Nested attributes
            attrs = item.get("attributes", {}) or {}
            titles = attrs.get("titles", {}) or {}

            status = attrs.get("status", "") or ""
            startDate = attrs.get("startDate", "") or ""
            endDate = attrs.get("endDate", "") or ""
            ageRating = attrs.get("ageRating", "") or ""
            avgRating = None
            try:
                ar = attrs.get("averageRating")
                if ar is not None and ar != "": avgRating = str(float(ar))
            except (ValueError, TypeError):
                avgRating = None
            rank = attrs.get("popularityRank", "") or ""
            desc = attrs.get("description", "") or ""

            #Local truncation helper to keep text readable in terminal/JSON
            def truncate(text: str, maxlen: int = 160) -> str:
                if isinstance(text, str) and len(text) > maxlen:
                    return text[: maxlen - 1] + "..."
                return text

            row = {
                "id": id,
                "title_en_jp": titles.get("en_jp"),
                "status": status,
                "startDate": startDate,
                "endDate": endDate,
                "ageRating": ageRating,
                "avgRating": avgRating,
                "rank": rank,
                "description": truncate(desc) if desc else None
            }
            rows.append(row)
        except Exception as item_err:
            #skip malformed items but continue processing others
            print(f"to_dataframe: skipped item due to error: {item_err}")
            continue
    try:
        return pd.DataFrame(rows)
    except Exception as e:
        print(f"to_dataframe: failed to create DataFrame: {e}")
        return pd.DataFrame([])


def pretty_print(df: pd.DataFrame) -> None:
    try:
        if df.empty:
            print("No data to show")
            return

        #Fields to display
        cols_to_show = [
            "id",
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
            return (x[: n - 1] + "…") if isinstance(x, str) and len(x) > n else x  #Only truncate strings > 160 char

        #Iterate through each column and replace with truncated version
        for c in cpy_df.columns:
            # use map with error protection
            cpy_df[c] = cpy_df[c].map(lambda v: truncate(v) if v is not None else v)

        #Convert to list of dicts (records)
        records = cpy_df.to_dict(orient="records")
        print("\n============================== Anime Info ==============================\n")
        print(json.dumps(records, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"pretty_print: error while printing data: {e}")


CSV_FILE = "anime_items.csv"
JSON_FILE = "anime_raw.json"

def save_output(df: pd.DataFrame) -> None:
    try:
        base_dir: Path = Path(__file__).parent
    except Exception:
        base_dir = Path.cwd()

    csv_path: Path = base_dir / CSV_FILE
    json_path: Path = base_dir / JSON_FILE

    #CSV file: append if exists, else create with header
    try:
        csv_exists = csv_path.exists() and csv_path.stat().st_size > 0
        df.to_csv(
            csv_path,
            mode="a" if csv_exists else "w",
            header=not csv_exists,
            index=False,
            encoding="utf-8",
        )
        print(f"Saved items to {csv_path} ({'appended' if csv_exists else 'created'}) with {len(df)} new rows.")
    except Exception as e:
        print(f"save_output: failed to write CSV {csv_path}: {e}")

    #JSON file: convert df to a list of dicts or records & pretty dump
    try:
        records = df.to_dict(orient="records")
    except Exception as e:
        print(f"save_output: failed to convert DataFrame to records: {e}")
        records = []

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
            # if file corrupted or unreadable, start fresh
            data = []

    try:
        data.extend(records)
    except Exception as e:
        print(f"save_output: failed to extend JSON data: {e}")

    try:
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved selected fields to {json_path} (array of {len(data)} records).")
    except Exception as e:
        print(f"save_output: failed to write JSON {json_path}: {e}")