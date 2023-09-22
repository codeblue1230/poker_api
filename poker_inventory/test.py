import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(f"{BASE}/8c_9s/Jh_9h_Qc_10d_Js")
print(response.json())

# Program effectively detectes all straight, pairs, two pairs, trips, quads, and full houses.  However, 
# I need to fix the quads and two pair snippets because it can mistakenly return a two pair and 
# say quads is the user's hand