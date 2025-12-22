import requests
from anime_data_extraction_script import *

base_url = "https://kitsu.io/api/edge/anime?"
headers = {
    'Content-Type': 'application/vnd.api+json',
    'Accept': 'application/vnd.api+json'
}

def build_filters() -> str:
    catFilter = animeFilter = False
    category = animeTitle = "" 

    filter_by = input("Filter by Category or Anime Title or Both? (C/T/B): ").lower().strip()
    if filter_by == 'c':
        catFilter = True
        category = input("Enter any category(Adventure/Shounen/Romance...etc): ").lower().strip() 
        if not category:
            print("[WARN] Empty category entered. No category filter will be applied.")
            catFilter = False
        
    elif filter_by == 't':
        animeFilter = True
        animeTitle = input("Enter any anime title(Attack on Titan, Naruto, Hunter x hunter,...etc): ").lower().strip().replace(" ","-")
        if not animeTitle:
            print("[WARN] Empty anime title entered. No anime title filter will be applied.")
            animeTitle = False
        
    elif filter_by == 'b':
        catFilter = True
        animeFilter = True
        category = input("Enter any category(Adventure/Shounen/Romance...etc): ").lower().strip()
        animeTitle = input("Enter any anime title(Attack on Titan, Naruto, Hunter x hunter,...etc): ").lower().strip().replace(" ","-")
        
        if not category:
            print("[WARN] Empty category entered. No category filter will be applied.")
            catFilter = False
        if not animeTitle:
            print("[WARN] Empty anime title entered. No anime title filter will be applied.")
            animeTitle = False
            
    else: print("Invalid input! Please try again.")
    
    filter = []
    if catFilter:
        filter.append(f"filter[categories]={category}")
        
    if animeFilter:
        filter.append(f"filter[text]={animeTitle}")
        
    if not filter:
        print("Something went wrong with filtering anime...!")    
    
    return "&".join(filter)
    
def fetch_anime_info(query: str) -> dict:
    response = requests.get(url = base_url + query, headers = headers)
    data = response.json()
    return data

query = build_filters()
payload = fetch_anime_info(query)

df = to_dataframe(payload)

pretty_print(df)
save_output(df)
