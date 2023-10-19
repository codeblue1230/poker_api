import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(f"{BASE}Ac/4c&2c/7c/3c/5c/6c")
print(response.json())