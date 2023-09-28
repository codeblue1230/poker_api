from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

cards = {
    "2s": (2, "s", "2s"),
    "2c": (2, "c", "2c"),
    "2h": (2, "h", "2h"),
    "2d": (2, "d", "2d"),
    "3s": (3, "s", "3s"),
    "3c": (3, "c", "3c"),
    "3h": (3, "h", "3h"),
    "3d": (3, "d", "3d"),
    "4s": (4, "s", "4s"),
    "4c": (4, "c", "4c"),
    "4h": (4, "h", "4h"),
    "4d": (4, "d", "4d"),
    "5s": (5, "s", "5s"),
    "5c": (5, "c", "5c"),
    "5h": (5, "h", "5h"),
    "5d": (5, "d", "5d"),
    "6s": (6, "s", "6s"),
    "6c": (6, "c", "6c"),
    "6h": (6, "h", "6h"),
    "6d": (6, "d", "6d"),
    "7s": (7, "s", "7s"),
    "7c": (7, "c", "7c"),
    "7h": (7, "h", "7h"),
    "7d": (7, "d", "7d"),
    "8s": (8, "s", "8s"),
    "8c": (8, "c", "8c"),
    "8h": (8, "h", "8h"),
    "8d": (8, "d", "8d"),
    "9s": (9, "s", "9s"),
    "9c": (9, "c", "9c"),
    "9h": (9, "h", "9h"),
    "9d": (9, "d", "9d"),
    "10s": (10, "s", "10s"),
    "10c": (10, "c", "10c"),
    "10h": (10, "h", "10h"),
    "10d": (10, "d", "10d"),
    "Js": (11, "s", "Js"),
    "Jc": (11, "c", "Jc"),
    "Jh": (11, "h", "Jh"),
    "Jd": (11, "d", "Jd"),
    "Qs": (12, "s", "Qs"),
    "Qc": (12, "c", "Qc"),
    "Qh": (12, "h", "Qh"),
    "Qd": (12, "d", "Qd"),
    "Ks": (13, "s", "Ks"),
    "Kc": (13, "c", "Kc"),
    "Kh": (13, "h", "Kh"),
    "Kd": (13, "d", "Kd"),
    "As": (14, "s", "As"),
    "Ac": (14, "c", "Ac"),
    "Ah": (14, "h", "Ah"),
    "Ad": (14, "d", "Ad")
}

class Poker(Resource):
    def get(self, hole1, hole2, flop1, flop2, flop3, turn, river):
        table = {"community": [flop1, flop2, flop3, turn, river],
                "player": [hole1, hole2]
                }

        # Check for dupliacte cards entered by User (return Error if any are found)
        def check_dupes():
            check_for_dupes = {}
            for card in table["community"]:
                if card not in check_for_dupes:
                    check_for_dupes[card] = 1
                else:
                    return {"Error": "Duplicate Cards"}
            for card in table["player"]:
                if card not in check_for_dupes:
                    check_for_dupes[card] = 1
                else:
                    return {"Error": "Duplicate Cards"}
            return {"Valid": "Valid Cards"}

        dupe = check_dupes()
        if "Error" in dupe:
            return dupe
        
        # Add all cards to a list and sort them so we know the cards are in order from high to low
        # This step is important as this list will be used frequently from here on out
        seven_cards = [cards[card] for card in table["community"]] # Add community cards
        seven_cards.append(cards[table["player"][0]]) # Add player hole card
        seven_cards.append(cards[table["player"][1]]) # Add player hole card
        seven_cards.sort(key=lambda x: x[0], reverse=True) # Sort the cards in order highest to lowest

        # Check to see if any flush is present
        def check_misc_flush(my_cards):
            flush_dict = {} # Dictionary to track each card and it's suit
            for item in my_cards:
                if item[1] not in flush_dict:
                    flush_dict[item[1]] = [item[2]]
                else:
                    flush_dict[item[1]].append(item[2])
            for v in flush_dict.values(): # This loop checks if the dictionary contains a flush
                if len(v) >= 5: # If any value has 5 or more values a flush is present
                    flush_list = v[:5] # Since cards are already sorted we can take the first 5 cards
                    return {"Flush Detected": flush_list}
            return {"No Flush": "No Flush"}
        
        # If a flush is present we call this to check the type of flush
        def check_flush_type(flush_arr):
            sf_tracker = 0
            for i in range(len(flush_arr) - 1): # This loop tells us if we have a straight with out flush
                if cards[flush_arr[i]][0] - 1 == cards[flush_arr[i+1]][0]:
                    sf_tracker += 1
            if sf_tracker == 4 and cards[flush_arr[0]][0] == 14: # Check for royal flush
                return {"Royal Flush": flush_arr} # We know it's royal becuase we assigned 14 to be the value of Ace
            if sf_tracker == 4 and cards[flush_arr[0]][0] != 14: # Check for straight flush
                return {"Straight Flush": flush_arr} # If an Ace is not present we know it is a straight flush and not royal
            if sf_tracker != 4: # If no straight is present we know it is a regular flush
                return {"Flush": flush_arr}
            return {"No Flush": "None Detected"}
                
        # If a royal flush or straight flush is found we return because those are the 2 best poker hands
        # Otherwise the flush will just be stored in the flush variable
        test_flush = check_misc_flush(seven_cards)
        if "Flush Detected" in test_flush:
            flush = check_flush_type(test_flush["Flush Detected"])
            if "Royal Flush" in flush:
                return flush
            elif "Straight Flush" in flush:
                return flush
        """
        Remember that if a straight flush or royal flush are not found we know we have a regular flush,
        We can keep this in mind for later because we will check to make sure we don't have some other
        superior hands (Quads, Full House) before return the flush as the best possible hand
        """
        
        def quad_check(all_cards):
            quad_dict = {}
            for c in all_cards:
                if c[0] not in quad_dict:
                    quad_dict[c[0]] = [c[2]]
                else:
                    quad_dict[c[0]].append(c[2])
            for k, v in quad_dict.items():
                if len(v) == 4:
                    for c, n in quad_dict.items():
                        if c != k:
                            v += n
                            return {"Four of a Kind": v}
            return {"No Four of a Kind": "None Found"}
        
        quads = quad_check(seven_cards)
        if "Four of a Kind" in quads:
            return quads
        
        def full_house_check(card_arr):
            full_dict = {}
            for c in card_arr:
                if c[0] not in full_dict:
                    full_dict[c[0]] = [c[2]]
                else:
                    full_dict[c[0]].append(c[2])
            for k, v in full_dict.items():
                if len(v) == 3:
                    for c, n in full_dict.items():
                        if len(n) == 2:
                            v += n
                            return {"Full House": v}
                        elif len(n) > 2 and k != c:
                            v += n
                            v.pop()
                            return {"Full House": v}
            return {"No Full House": "None Detected"}
        
        full_house = full_house_check(seven_cards)
        if "Full House" in full_house:
            return full_house
        
        if "Flush Detected" in test_flush:
            return flush

        return {"Testing": "Failed"}
    
api.add_resource(Poker, "/<string:hole1>_<string:hole2>/<string:flop1>_<string:flop2>_<string:flop3>_<string:turn>_<string:river>")
