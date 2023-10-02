from poker_inventory import Poker, api
import requests

BASE = "https://best-hold-em-hand.onrender.com"

my_app=api.add_resource(Poker, "/<string:hole1>_<string:hole2>/<string:flop1>_<string:flop2>_<string:flop3>_<string:turn>_<string:river>")

response = requests.get(f"{BASE}/2h_5s/2c_Jd_7c_5h_8d")