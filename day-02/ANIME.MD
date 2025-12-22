***

# Kitsu Anime CLI — Filter, Fetch, Flatten, and Persist

A small, robust Python **CLI tool** that lets you filter anime by **category**, **title**, or **both**, fetches results from the **Kitsu API**, flattens the JSON payload into a clean **pandas DataFrame**, **pretty-prints** selected fields, and **persists** them to **CSV** and **JSON**.

> **Quick demo:**
>
> *   Prompt the user: `C` (Category), `T` (Title), or `B` (Both)
> *   Build Kitsu filters (`filter[categories]`, `filter[text]`)
> *   GET `https://kitsu.io/api/edge/anime?` + query
> *   Transform to a DataFrame with curated fields
> *   Pretty-print and save to `anime_items.csv` and `anime_items.json`

***

## ✨ Key Features

*   **Interactive filtering**: Category (`C`), Title (`T`), or Both (`B`) with input normalization.
*   **Smart validation**: Warns and **skips** empty inputs to keep the query valid.
*   **Clean transformation**: Extracts core attributes and truncates long descriptions (160 chars).
*   **Readable output**: Pretty-prints as JSON with UTF‑8 support.
*   **Durable persistence**:
    *   **CSV**: append-or-create with proper headers.
    *   **JSON**: maintains a **single array**, extends on each run, and pretty saves.

***

## 🧱 Project Structure

    .
    ├── anime_info_api.py              # CLI: build filters, call API, orchestrate flow
    ├── anime_data_extraction.py       # Transform, pretty-print, and save outputs
    └── README.md                      # This document


> ```python
> from anime_data_extraction import *
> ```

***

## 🏛️ Architecture / Workflow Diagram




***

## 📦 Requirements

*   Python **3.8+**
*   Packages: `requests`, `pandas`

```bash
pip install requests pandas
```

***

## 🚀 Getting Started

1.  **Clone or copy** the files into a project directory.
2.  **Ensure imports match filenames** (see note above).
3.  Run the CLI:
    ```bash
    python anime_info_api.py
    ```

***

## 🕹️ Usage

When prompted:

*   Enter `C` for **Category** (e.g., `Adventure`, `Shounen`). Input is lowercased.
*   Enter `T` for **Title** (e.g., `Attack on Titan`). Input is lowercased and spaces become hyphens.
*   Enter `B` for **Both** to combine filters.

**Invalid input** → you’ll be asked to try again.\
**Empty category/title** → a warning is shown and that filter is skipped.

***

## 🔎 API Query Basics

*   **Base URL:** `https://kitsu.io/api/edge/anime?`
*   **Filters used:**
    *   Category → `filter[categories]=<category>`
    *   Title → `filter[text]=<title-with-hyphens>`
*   **Headers:**
    *   `Accept: application/vnd.api+json`
    *   `Content-Type: application/vnd.api+json`

***

## 🧪 Data Transformation

For each item in `payload.data`, the tool extracts:

*   `id`
*   `titles.en` → `title_en`
*   `titles.en_jp` → `title_en_jp`
*   `status`
*   `startDate`, `endDate`
*   `ageRating`
*   `averageRating` → **stringified float** if present, else `None`
*   `popularityRank` → `rank`
*   `description` → **truncated to 160 chars**

Results are combined into a **pandas DataFrame**.

***

## 🖨️ Output & Persistence

*   **Terminal output:** pretty JSON for selected columns (with truncation).
*   **CSV:** `anime_items.csv`
    *   Append if file exists and non-empty; else create with header.
*   **JSON:** `anime_items.json`
    *   Maintain a single array; load existing, extend with new records, and rewrite with indentation.

***

## 📁 Example Session

    Filter by Category or Anime Title or Both? (C/T/B): b
    Enter any category(Adventure/Shounen/Romance...etc): shounen
    Enter any anime title(Attack on Titan, Naruto, Hunter x hunter,...etc): attack on titan

    ============================== Anime Info ==============================
    [
      {
        "id": "7442",
        "title_en": "Attack on Titan",
        "title_en_jp": "Shingeki no Kyojin",
        "status": "finished",
        "startDate": "2013-04-07",
        "endDate": "2023-11-05",
        "ageRating": "R",
        "avgRating": "89.2",
        "rank": 1,
        "description": "Humans are nearly exterminated by giant creatures..."
      },
      ...
    ]
    Saved items to anime_items.csv (created) with 25 new rows.
    Saved selected fields to anime_items.json (array of 25 records).

> Output values depend on live API results; the above is illustrative.

***

## ⚠️ Known Limitations & Next Steps

*   **No pagination** yet (Kitsu supports `page[limit]` / `page[offset]`).
*   **Minimal error handling** for HTTP/network failures.
*   **No CLI flags**; input is purely interactive.

**Roadmap ideas:**

*   Add `argparse` flags (e.g., `--category`, `--title`, `--limit`).
*   Implement pagination & rate-limiting.
*   Persist raw payloads and add unit tests.
*   Export to Excel/Parquet.

***

## 🤝 Acknowledgments

*   Built on the **Kitsu API** (JSON:API compliant).
