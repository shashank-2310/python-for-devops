from urllib import response
import requests
from dotenv import load_dotenv
import os

load_dotenv()

#Function to get API key & API URL from .env
def get_api():
    api_key = os.getenv("STOCK_MARKET_API_KEY") 
    if not api_key:
        print("API Key not found in .env file")
        exit(1)

    api_url = os.getenv("STOCK_MARKET_URL")
    if not api_url:
        print("API URL not found in .env file")
        exit(1)
    return api_key, api_url

#Function to get data from API
def get_stock_market_data(symbol):
    api_key, api_url = get_api()
    
    query = f"query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url = api_url + query)
    
    data = response.json()
    for key, value in data.items():
        print(key, value)

symbol = input("Enter the Symbol you want for the Stock Market API eg. (AMZN, GOGL, IBM, etc): ").upper()
get_stock_market_data(symbol)