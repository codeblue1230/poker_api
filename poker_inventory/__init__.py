from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

cards = {
    "2s": 2,
    "2c": 2,
    "2h": 2,
    "2d": 2,
    "3s": 3,
    "3c": 3,
    "3h": 3,
    "3d": 3,
    "4s": 4,
    "4c": 4,
    "4h": 4,
    "4d": 4,
    "5s": 5,
    "5c": 5,
    "5h": 5,
    "5d": 5,
    "6s": 6,
    "6c": 6,
    "6h": 6,
    "6d": 6,
    "7s": 7,
    "7c": 7,
    "7h": 7,
    "7d": 7,
    "8s": 8,
    "8c": 8,
    "8h": 8,
    "8d": 8,
    "9s": 9,
    "9c": 9,
    "9h": 9,
    "9d": 9,
    "10s": 10,
    "10c": 10,
    "10h": 10,
    "10d": 10,
    "Js": 11,
    "Jc": 11,
    "Jh": 11,
    "Jd": 11,
    "Qs": 12,
    "Qc": 12,
    "Qh": 12,
    "Qd": 12,
    "Ks": 13,
    "Kc": 13,
    "Kh": 13,
    "Kd": 13,
    "As": 14,
    "Ac": 14,
    "Ah": 14,
    "Ad": 14,
}

class Poker(Resource):
    def get(self, hole1, hole2, flop1, flop2, flop3, turn, river):
        table = {"community": [flop1, flop2, flop3, turn, river],
                "player1": [hole1, hole2]
                }
        
        #Check for dupliacte cards entered by User (return an Error if found)
        check_for_dupes = {}
        for card in table["community"]:
            if card not in check_for_dupes:
                check_for_dupes[card] = 1
            else:
                return {"Error": "Invalid Cards"}
        for card in table["player1"]:
            if card not in check_for_dupes:
                check_for_dupes[card] = 1
            else:
                return {"Error": "Invalid Cards"}
            
        
        paired_cards = []
        all_cards = []
        pointer1 = 0
        pointer2 = 1

        # Check the board for paired cards
        while pointer1 < len(table["community"]) - 1:
            card1 = table["community"][pointer1]
            card2 = table["community"][pointer2]
            if cards[card1] == cards[card2]:
                paired_cards.append(card1)
                paired_cards.append(card2)
            pointer2 += 1
            if pointer2 == len(table["community"]):
                pointer1 += 1
                pointer2 = pointer1 + 1
            
        # Compare user's hole cards to the community cards to search for pairs
        for card in table["community"]:
            if cards[card] == cards[table["player1"][0]]:
                paired_cards.append(card)
                paired_cards.append(table["player1"][0])
            if cards[card] == cards[table["player1"][1]]:
                paired_cards.append(card)
                paired_cards.append(table["player1"][1])
            all_cards.append((card, cards[card]))

        # Check user's hole cards for pairs
        if cards[table["player1"][0]] == cards[table["player1"][1]]:
            paired_cards.append(table["player1"][0])
            paired_cards.append(table["player1"][1])

        # If no pairs are found return the 5 best cards
        if len(paired_cards) == 0:
            all_cards.append((table["player1"][0], cards[table["player1"][0]]))
            all_cards.append((table["player1"][1], cards[table["player1"][1]]))
            all_cards.sort(key=lambda x: x[1], reverse=True)
            all_cards.pop()
            all_cards.pop()
            response = {
                "all_cards": all_cards
            }

        # If a pair is detected we return the list of pairs with the next 3 best cards
        else:
            rest_of_cards = []
            paired_cards_set = set(paired_cards)
            all_cards.append((table["player1"][0], cards[table["player1"][0]]))
            all_cards.append((table["player1"][1], cards[table["player1"][1]]))
            all_cards = [card for card in all_cards if card[0] not in paired_cards_set]
            all_cards.sort(key=lambda x: x[1], reverse=True)
            for index, card in enumerate(all_cards):
                if index == 0 or index == 1 or index == 2:
                    rest_of_cards.append(card[0])
            response = {
            "paired_cards": paired_cards,
            "rest_of_cards": rest_of_cards
            }

        return response

    
api.add_resource(Poker, "/<string:hole1>_<string:hole2>/<string:flop1>_<string:flop2>_<string:flop3>_<string:turn>_<string:river>")
