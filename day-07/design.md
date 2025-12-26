# Log Analyzer CLI – Design

## Problem
Count occurrences of log levels in a log file and optionally export the summary to JSON.

## Inputs
- `--file <log_file>` (required): Path/name of the log file.
- `--level [LEVEL ...]` (optional): Levels to count; defaults to `INFO WARNING ERROR` if omitted.
- `--out [JSON_FILE]` (optional): Enable JSON export. If no filename is provided, uses `log_summary.json`.

## Outputs
- Console: Prints counts per selected level.
- File (optional): Writes counts as JSON in the script directory when `--out` is provided.

## Main Steps
1. Parse CLI arguments with `argparse`.
2. Build the level list (default: INFO, WARNING, ERROR).
3. Resolve the log file path relative to the script directory.
4. Read the log file line by line and increment counters for matching levels.
5. Print the summary to stdout.
6. If `--out` is set, write the counts to the JSON file.

## Errors / Edge Cases
- Missing log file → raise `LogAnalyzerError` with a clear message.
- JSON export failures (e.g., permission issues) → `LogAnalyzerError`.
- Assumes UTF-8 text log and substring matching for levels.

## Features
- Counts log levels (INFO, WARNING, ERROR by default)
- Optional level filtering via `--level`
- Optional JSON export via `--out` (default filename: `log_summary.json`)

## Usage
```bash
python log_analyzer_cli.py --file <log_file> [--level LEVEL ...] [--out [JSON_FILE]]
```

Examples:
- Basic summary (no JSON):
  ```bash
  python log_analyzer_cli.py --file app.log
  ```
- Summary filtered to specific levels:
  ```bash
  python log_analyzer_cli.py --file app.log --level ERROR WARNING
  ```
- Export summary to default JSON:
  ```bash
  python log_analyzer_cli.py --file app.log --out
  ```
- Export summary to custom JSON:
  ```bash
  python log_analyzer_cli.py --file app.log --out summary.json
  ```

## Arguments
- `--file` (required): Log file name to analyze.
- `--level` (optional, zero or more): Levels to count; defaults to `INFO WARNING ERROR` if omitted.
- `--out` (optional): Enable JSON export. Provide an optional filename; if omitted, uses `log_summary.json`.

## Behavior
- Prints a table of level counts to stdout.
- When `--out` is used, writes counts to JSON in the same directory as the script.

## Notes
- Default JSON filename: `log_summary.json` (when `--out` is used without a name).
- Levels are matched by substring; ensure log lines contain the level tokens (e.g., `INFO`, `ERROR`, `WARNING`).