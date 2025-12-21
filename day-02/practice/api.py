import requests

api_url = "https://api.sampleapis.com/switch/games" # server URL (API)

response = requests.get(url=api_url)
# print(response.json())

if response.status_code == 200:
    print("ID | Name | Genre | Developer | NA Release")
    print("---|------|-------|-----------|-----------")
    
    data = response.json()[:10] #Take first 10 items
    for game in data:
        name = 'N/A'
        genre = 'N/A'
        dev = 'N/A'
        na_date = 'N/A'
        for key, value in game.items():
            if key == 'name': name = str(value).lstrip('#') #Remove leading '#'
            elif key == 'genre': genre = ', '.join(value)
            elif key == 'developers': dev = value[0] if value else 'N/A'
            elif key == 'releaseDates': na_date = value['Europe']
        
        print(f"{game['id']} | {name} | {genre} | {dev} | {na_date}")
else: 
    print(f"{response.status_code}: {response.reason}")
