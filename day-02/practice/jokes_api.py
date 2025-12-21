import requests

base_url = "https://v2.jokeapi.dev/joke/"

def get_jokes(cat, flags) -> None:
    if cat not in ['dark', 'pun', 'spooky', 'christmas', 'misc', 'any']:
        print("Invalid Category! Proceeding with a random joke.")
        cat = 'any'
        
    blacklistFlags= ""
    if flags: blacklistFlags = f"?blacklistFlags={flags}"

    api_url = base_url + cat + blacklistFlags
    response = requests.get(url = api_url)
    
    data = response.json()
    if data.get("error"):
        print(f"API Error: {data.get('message', 'Something went wrong!')}")
        return
    
    print(f"\nHere's a {data["category"].lower()} joke for you. Enjoy...! 😆\n")
    joke = data["setup"] + "\n" + data["delivery"] + "\n"
    
    return joke

cat = input("Joke Category (Dark/Pun/Spooky/Christmas/Misc/Random): [Enter for random] ").lower().strip()
if cat == '' or cat == 'random': cat = 'any'

flags = input("Press enter for any jokes or type 'NO' for safe jokes only: ").lower().strip()
if flags == 'no': 
    flags = "nsfw,religious,political,racist,sexist,explicit"
elif flags == '': 
    flags = ""
else:
    print("Invalid input! Defaulting to a random joke.")
    flags = ""

print(get_jokes(cat, flags))