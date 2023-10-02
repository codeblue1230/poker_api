from poker_inventory import Poker, api

my_app=api.add_resource(Poker, "/<string:hole1>_<string:hole2>/<string:flop1>_<string:flop2>_<string:flop3>_<string:turn>_<string:river>")