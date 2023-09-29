import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(f"{BASE}/5h_Jd/Kd_Jc_9s_Ac_2h")
print(response.json())