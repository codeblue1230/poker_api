import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(f"{BASE}/Qc_Qs/7s_2c_9s_10h_5h")
print(response.json())