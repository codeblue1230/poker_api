import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(f"{BASE}/Ad_Kd/5d_Jc_3s_10d_7d")
print(response.json())