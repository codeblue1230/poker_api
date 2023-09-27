from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

cards = {
    "2s": (2, "s"),
    "2c": (2, "c", "2c"),
    "2h": (2, "h"),
    "2d": (2, "d"),
    "3s": (3, "s"),
    "3c": (3, "c"),
    "3h": (3, "h"),
    "3d": (3, "d"),
    "4s": (4, "s"),
    "4c": (4, "c"),
    "4h": (4, "h"),
    "4d": (4, "d"),
    "5s": (5, "s"),
    "5c": (5, "c"),
    "5h": (5, "h"),
    "5d": (5, "d"),
    "6s": (6, "s"),
    "6c": (6, "c"),
    "6h": (6, "h"),
    "6d": (6, "d"),
    "7s": (7, "s"),
    "7c": (7, "c"),
    "7h": (7, "h"),
    "7d": (7, "d"),
    "8s": (8, "s"),
    "8c": (8, "c"),
    "8h": (8, "h"),
    "8d": (8, "d"),
    "9s": (9, "s"),
    "9c": (9, "c"),
    "9h": (9, "h"),
    "9d": (9, "d"),
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
        
        # #Check for dupliacte cards entered by User (return Error if any are found)
        def check_dupes():
            check_for_dupes = {}
            for card in table["community"]:
                if card not in check_for_dupes:
                    check_for_dupes[card] = 1
                else:
                    return {"Error": "Invalid Cards"}
            for card in table["player"]:
                if card not in check_for_dupes:
                    check_for_dupes[card] = 1
                else:
                    return {"Error": "Invalid Cards"}
            return {"Valid": "Valid Cards"}

        dupe = check_dupes()
        if "Error" in dupe:
            return dupe
        
        # Add all cards to a list and sort them so we know the 5 highest cards
        seven_cards = [cards[card] for card in table["community"]] # Add community cards
        seven_cards.append(cards[table["player"][0]]) # Add player hole cards
        seven_cards.append(cards[table["player"][1]]) # Add player hole cards
        seven_cards.sort(key=lambda x: x[0], reverse=True) # Sort the cards in order highest to lowest
        flush_dict = {} # Dictionary to count number of card suits
        for item in seven_cards:
            if item[1] not in flush_dict:
                flush_dict[item[1]] = 1
            else:
                flush_dict[item[1]] += 1
        if 5 or 6 or 7 in flush_dict.values():
            return flush_dict

        # Check for a Royal Flush
        def check_royal_flush():
            rf_list, i = [], 0
            while i < len(rf_list):
                if seven_cards[i][0] + 1 == seven_cards[i + 1][0] and seven_cards[i][1] == seven_cards[i + 1][1]:
                    rf_list.append(seven_cards[i][2])
                print(rf_list)
            return rf_list

        royal_flush = check_royal_flush()
        if len(royal_flush) == 5:
            return {"Royal Flush": royal_flush}

        return {"Test": "Failed"}
        
        # FIRST APPROACH IS THE CODE BELOW, GONNA START OVER WITH MORE ORGANIZED
        # CODE BECAUSE I AM NOT HAPPY WITH THE SETUP OF THE CODE BELOW,
        # MY NEW PLAN IS TO WORK MY WAY TOP DOWN FROM THE BEST HAND TO THE WORST HAND
        
        # paired_cards = []
        # all_cards = []
        # pointer1 = 0
        # pointer2 = 1

        # # Check for a straight
        # straight_check = [(card, cards[card]) for card in table["community"]]
        # straight_check.append((table["player1"][0], cards[table["player1"][0]]))
        # straight_check.append((table["player1"][1], cards[table["player1"][1]]))
        # straight_check.sort(key=lambda x: x[1], reverse=True)
        # straight_counter = 1
        # index = 0
        # straight_list = []
        # while index < len(straight_check):
        #     if straight_counter == 5:
        #         break
            
        #     if index == len(straight_check) - 1:
        #         if straight_check[index - 1][1] - 1 == straight_check[index][1]:
        #             straight_counter += 1
        #             straight_list.append(straight_check[index][0])
        #     if index != len(straight_check) - 1:
        #         if straight_check[index - 1][1] - 1 == straight_check[index][1]:
        #             straight_counter += 1
        #             straight_list.append(straight_check[index][0])
        #         else:
        #             straight_counter = 1
        #             straight_list = []
        #             straight_list.append(straight_check[index][0])
        #     print(straight_check[index][1], straight_counter)
        #     index += 1
        # # If straight is found return it
        # if straight_counter == 5:
        #     return {"Straight": straight_list}
        # else: # One final straight check for the wheel straight (A,2,3,4,5)
        #     if straight_check[0][1] == 14 and straight_check[-1][1] == 2:
        #         if straight_check[-2][1] == 3 and straight_check[-3][1] == 4 and straight_check[-4][1] == 5:
        #             wheel = []
        #             wheel.append(straight_check[0][0])
        #             wheel.append(straight_check[-1][0])
        #             wheel.append(straight_check[-2][0])
        #             wheel.append(straight_check[-3][0])
        #             wheel.append(straight_check[-4][0])
        #             return {"Straight": wheel}

        # # Check the board for paired cards
        # while pointer1 < len(table["community"]) - 1:
        #     card1 = table["community"][pointer1]
        #     card2 = table["community"][pointer2]
        #     if cards[card1] == cards[card2]:
        #         paired_cards.append(card1)
        #         paired_cards.append(card2)
        #     pointer2 += 1
        #     if pointer2 == len(table["community"]):
        #         pointer1 += 1
        #         pointer2 = pointer1 + 1
            
        # # Compare user's hole cards to the community cards to search for pairs
        # for card in table["community"]:
        #     if cards[card] == cards[table["player1"][0]]:
        #         paired_cards.append(card)
        #         paired_cards.append(table["player1"][0])
        #     if cards[card] == cards[table["player1"][1]]:
        #         paired_cards.append(card)
        #         paired_cards.append(table["player1"][1])
        #     all_cards.append((card, cards[card]))

        # # Check user's hole cards for pairs
        # if cards[table["player1"][0]] == cards[table["player1"][1]]:
        #     paired_cards.append(table["player1"][0])
        #     paired_cards.append(table["player1"][1])

        # # If no pairs are found return the 5 best cards
        # if len(paired_cards) == 0:
        #     all_cards.append((table["player1"][0], cards[table["player1"][0]]))
        #     all_cards.append((table["player1"][1], cards[table["player1"][1]]))
        #     all_cards.sort(key=lambda x: x[1], reverse=True)
        #     all_cards.pop()
        #     all_cards.pop()
        #     return {
        #         "all_cards": all_cards
        #     }

        # # If the paired_cards list has any values we have to check what the hand is
        # else:
        #     rest_of_cards = []
        #     paired_cards_set = set(paired_cards)
        #     all_cards.append((table["player1"][0], cards[table["player1"][0]]))
        #     all_cards.append((table["player1"][1], cards[table["player1"][1]]))
        #     all_cards = [card for card in all_cards if card[0] not in paired_cards_set]
        #     all_cards.sort(key=lambda x: x[1], reverse=True)
        #     # Check to see if there is a single pair
        #     if len(paired_cards) == 2:
        #         for index, card in enumerate(all_cards):
        #             if index == 0 or index == 1 or index == 2:
        #                 rest_of_cards.append(card[0])
        #         return {
        #             "pair": paired_cards,
        #             "rest of cards": rest_of_cards
        #         }
        #     # Check to see if user has trips
        #     if len(paired_cards_set) == 3:
        #         rest_of_cards.append(all_cards[0][0])
        #         rest_of_cards.append(all_cards[1][0])
        #         return {
        #             "trips": list(paired_cards_set),
        #             "rest of cards": rest_of_cards
        #         }
        #     # Check for quads
        #     if len(paired_cards_set) == 4:
        #         rest_of_cards.append(all_cards[0][0])
        #         return {
        #             "quads": list(paired_cards_set),
        #             "rest of cards": rest_of_cards
        #         }
        #     # Check for Full House
        #     if len(paired_cards_set) == 5: # Check to make sure the 5 best cards make up the full house
        #         return {"Full House": list(paired_cards_set)}
        #     if len(paired_cards_set) == 7: # Get rid of the worst pair and return the proper full house
        #         best_house = [(card, cards[card]) for card in paired_cards_set]
        #         best_house.sort(key=lambda x: x[1], reverse=True)
        #         best_house.pop()
        #         best_house.pop()
        #         full_house = [card[0] for card in best_house]
        #         return {"Full House": full_house}
        #     # Check for two pair
        #     if len(paired_cards) == 4:
        #         rest_of_cards.append(all_cards[0][0])
        #         return {
        #         "paired_cards": paired_cards,
        #         "rest_of_cards": rest_of_cards
        #         }

        # return {"Testing": list(paired_cards_set)}

    
api.add_resource(Poker, "/<string:hole1>_<string:hole2>/<string:flop1>_<string:flop2>_<string:flop3>_<string:turn>_<string:river>")
