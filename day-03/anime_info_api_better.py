import requests
from anime_data_extraction_script_better import *
from urllib.parse import urlencode

base_url = "https://kitsu.io/api/edge/anime?"
headers = {
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/vnd.api+json'
}

def build_filters() -> str:
    choices = {"c": "category", "t": "title", "b": "both", "e": "exit"}
    try:
        while True:
            choice = input("Filter by Category or Anime Title or Both(C/T/B). OR for Exit enter(E): ").strip().lower()
            if choice in choices:
                break
            print("Invalid input! Please enter C, T, B or E.")

        filters = {}
        if choice in ("c", "b"):
            category = input("Enter any category (Adventure/Shounen/Romance...etc): ").strip()
            if category: filters["filter[categories]"] = category.lower()
            else: print("[WARNING] Empty category entered. No category filter will be applied.")
        
        if choice in ("t", "b"):
            title = input("Enter any anime title (Attack on Titan/Naruto/Hunter x hunter/One Piece...etc): ").strip()
            if title: filters["filter[text]"] = title
            else: print("[WARNING] Empty anime title entered. No anime title filter will be applied.")
        
        if choice == "e":
            print("Exiting!")
            exit(0)

        if not filters:
            print("No filters applied.")
            return ""
        
        return urlencode(filters)
    
    except (KeyboardInterrupt, EOFError):
        print("\nInput cancelled by user.")
        exit(0)
    
    except Exception as e:
        print(f"[ERROR] Unexpected error building filters: {e}")
        exit(0)

def fetch_anime_info(query: str) -> dict:
    response = requests.get(url = base_url + query, headers = headers)
    data = response.json()
    return data

query = build_filters()
payload = fetch_anime_info(query)

df = to_dataframe(payload)

pretty_print(df)
# save_output(df)
