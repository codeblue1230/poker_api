import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(f"{BASE}/Ad_4d/5s_3c_6s_7d_9d")
print(response.json())