import sys
import json
from pathlib import Path

class LogAnalyzerError(Exception):
    pass

class LogAnalyzer:
    def __init__(self, log_file: str, export_json: bool) -> None:
        self.log_file = log_file
        self.cnt = {
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "UNKNOWN": 0
        }
        self.base_dir = Path(__file__).parent
        self.log_file_path = self.base_dir / self.log_file
        self.export_json = export_json
        if export_json:
            self.json_file = "log_summary.json"
    

    def analyze(self):
        try:
            with self.log_file_path.open(
            "r",
            encoding = "utf-8"
            ) as f:
                for line in f:
                    if "INFO" in line:
                        self.cnt["INFO"] += 1
                    elif ("WARNING" in line) or ("WARN" in line):
                        self.cnt["WARNING"] += 1
                    elif "ERROR" in line:
                        self.cnt["ERROR"] += 1
                    else:
                        self.cnt["UNKNOWN"] += 1
        except FileNotFoundError as e:
            raise LogAnalyzerError(f"File not found: {self.log_file_path}") from e
        except Exception as e:
            raise LogAnalyzerError(f"While analyzing: {e}") from e


    def get_summary(self):
        print("\n===================== Log Levels =====================\n")
        try:
            for key, value in self.cnt.items():
                print(f"{key}: {value}")
        except Exception as e:
            raise LogAnalyzerError(f"Printing summary error: {e}") from e
        if self.export_json:
            self.export_to_json()


    def export_to_json(self):
        try:
            json_file_path = self.base_dir / self.json_file
            with json_file_path.open(
                "w",
                encoding = "utf-8"
            ) as f:
                json.dump(
                    self.cnt,
                    f,
                    ensure_ascii = False,
                    indent = 4
                )
                print(f"\nExported data to {json_file_path}")
        except (OSError, TypeError) as e:
            raise LogAnalyzerError(f"Failed to write JSON: {e}") from e
        except Exception as e:
            raise LogAnalyzerError(f"Exporting summary error: {e}") from e


def main():
    try:
        choice = input("Output as JSON(Y/N): ").lower().strip()
        if choice == "y":
            json_flag = True
        elif choice == "n":
            json_flag = False
        else:
            raise TypeError("Please enter 'Y' or 'N'")
    except KeyboardInterrupt:
        print("Input interrupted by user... Exiting!")
        sys.exit(1)
    except TypeError as e:
        print(f"Invalid choice! {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[Input] Unexpected error occurred: {e}")
        sys.exit(1)
 
    try:
        analyzer = LogAnalyzer("app.log", json_flag)
        analyzer.analyze()
        analyzer.get_summary()
    except LogAnalyzerError as e:
        print(f"[LogAnalyzer] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[Main] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
    