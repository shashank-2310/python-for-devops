# Log Analyzer CLI

Analyze a log file by counting occurrences of log levels and optionally export the summary to JSON.

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

## Errors
- Raises a `LogAnalyzerError` with a clear message if the log file is missing or processing fails.