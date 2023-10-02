import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(f"{BASE}/2h_5s/2c_Jd_7c_5h_8d")
print(response.json())