import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = "http://127.0.0.1:8000/generate?prompt=hello%20world"
headers = {
    "x-api-key": os.getenv("API_KEY"),
    "content-type": "application/json"
}

response = requests.post(url, headers=headers)

print(response.json())