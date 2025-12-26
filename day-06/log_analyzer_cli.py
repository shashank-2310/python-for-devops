import argparse
import json
import sys
from pathlib import Path

default = {
    "levels": ["INFO", "WARNING", "ERROR"],
    "json_filename": "log_summary.json"
}

parser = argparse.ArgumentParser(
    prog = "log_analyzer.py",
    description = "Analyze logs and provide their summary",
    add_help = True
)

parser.add_argument(
    "--file",
    type = str,
    required = True,
    help = "Log file name",
    action = "store",
    metavar = "Log File"
)

parser.add_argument(
    "--out",
    type = str,
    help = "Output JSON file name",
    action = "store",
    metavar = "JSON Filename",
    nargs = "?",
    const = default["json_filename"]
)

parser.add_argument(
    "--level",
    type = str,
    help = "Filter out specific level",
    action = "store",
    metavar = "Levels",
    nargs = "*"

)


class LogAnalyzerError(Exception):
    pass

class LogAnalyzer:
    def __init__(self, args) -> None:
        self.log_file = args.file
        self.base_dir = Path(__file__).parent
        self.log_file_path = self.base_dir / self.log_file

        self.export_json = args.out is not None
        if self.export_json:
            self.json_file = args.out
            
        levels = list(args.level) if args.level else default["levels"]
        self.count = dict.fromkeys(levels, 0)
        self._levels = tuple(self.count.keys())
        
    

    def analyze(self):
        try:
            with self.log_file_path.open(
            "r",
            encoding = "utf-8"
            ) as f:
                for line in f:
                    for key in self._levels:
                        if key in line:
                            self.count[key] += 1
        except FileNotFoundError as e:
            raise LogAnalyzerError(f"File not found: {self.log_file_path}") from e
        except Exception as e:
            raise LogAnalyzerError(f"While analyzing: {e}") from e


    def get_summary(self):
        print("\n===================== Log Levels =====================\n")
        try:
            for key, value in self.count.items():
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
                    self.count,
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
    args = parser.parse_args()
    try:
        analyzer = LogAnalyzer(args)
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
    