import sys
import json
from pathlib import Path

LOG_FILE = "app.log"
JSON_FILE = "log_summary.json"
base_dir = Path(__file__).parent


def count_log_levels(LOG_FILE) -> None:
    log_file_path = base_dir / LOG_FILE

    keys = ["INFO", "WARN", "ERROR"]
    cnt = dict.fromkeys(keys, 0)
    
    try:
        with log_file_path.open(
        "r",
        encoding = "utf-8"
        ) as f:
            for line in f:
                for key in keys:
                    if key in line:
                        cnt[key] += 1
    except FileNotFoundError:
        print("[ERROR] File not found!")
        sys.exit(1)
    except Exception as e:
        print(f"[counting log levels] Unexpected error occurred: {e}")
        sys.exit(1)

    print("\n===================== Log Levels =====================\n")
    for key, value in cnt.items():
        print(f"{key}: {value}")
        
    export_log_statistics(cnt) 


def export_log_statistics(cnt: dict) -> None:
    json_file_path = base_dir / JSON_FILE
    
    try:
        with json_file_path.open(
        "w",
        encoding = "utf-8"
        ) as f:
            json.dump(cnt, f, ensure_ascii = False, indent = 4)
        print(f"\nExported data to {json_file_path}")
    except (OSError, TypeError) as e:
        print(f"[exporting logs] failed to write JSON: {e}")
        sys.exit(1)  


if __name__ == "__main__":
    try:
        count_log_levels(LOG_FILE)
    except Exception as e:
        print(f"[main] Unexpected error occurred: {e}")
        sys.exit(1)