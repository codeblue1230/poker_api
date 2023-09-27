import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(f"{BASE}/Ac_10c/Jc_Kh_Qc_Kc_10s")
print(response.json())