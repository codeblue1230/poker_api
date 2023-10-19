import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(f"{BASE}As/Ks&Js/Qs/10s/9s/5s")
print(response.json())