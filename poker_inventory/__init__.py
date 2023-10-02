from flask import Flask
from flask_restful import Api, Resource, abort

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
        try:
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
                        return {"Flush Detected": v}
                return {"No Flush": "No Flush"}
            
            # If a flush is present we call this to check the type of flush
            def check_flush_type(flush_arr):
                print(flush_arr)
                fl_list, fl_values = [], set()
                pointer1, pointer2 = 0, 1
                while pointer2 < len(flush_arr):
                    first_num, second_num = cards[flush_arr[pointer1]], cards[flush_arr[pointer2]]
                    if first_num[0] - 1 == second_num[0]:
                        if first_num[0] not in fl_values:
                            fl_values.add(first_num[0])
                            fl_list.append(first_num[2])
                        if second_num[0] not in fl_values:
                            fl_values.add(second_num[0])
                            fl_list.append(second_num[2])
                    elif first_num[0] == second_num[0]:
                        pass
                    elif len(fl_list) >= 5:
                        break
                    else:
                        fl_list = [second_num[2]]
                        fl_values = set()
                        fl_values.add(second_num[0])
                    pointer1 += 1
                    pointer2 += 1
                fl_values = list(fl_values)
                print(fl_values)
                if fl_values[0] == 10 and len(fl_values) >= 5:
                    return {"Royal Flush": fl_list[:5]}
                if len(fl_values) >= 5:
                    return {"Straight Flush": fl_list[:5]}
                # If no regular Straight/Royal Flush is found  we check for the Wheel Straight Flush (A, 2, 3, 4, 5)
                wheel_list, wheel_set = [], set()
                for card in reversed(flush_arr):
                    curr_card = cards[card]
                    print(curr_card)
                    if curr_card[0] == 14:
                        if card[0] not in wheel_set:
                            wheel_set.add(curr_card[0])
                            wheel_list.append(curr_card[2])
                    elif curr_card[0] == 2:
                        if curr_card[0] not in wheel_set:
                            wheel_set.add(curr_card[0])
                            wheel_list.append(curr_card[2])
                    elif curr_card[0] == 3:
                        if curr_card[0] not in wheel_set:
                            wheel_set.add(curr_card[0])
                            wheel_list.append(curr_card[2])
                    elif curr_card[0] == 4:
                        if curr_card[0] not in wheel_set:
                            wheel_set.add(curr_card[0])
                            wheel_list.append(curr_card[2])
                    elif curr_card[0] == 5:
                        if curr_card[0] not in wheel_set:
                            wheel_set.add(curr_card[0])
                            wheel_list.append(curr_card[2])
                if len(wheel_list) == 5:
                    ace = wheel_list.pop()
                    final_wheel = [str_card for str_card in reversed(wheel_list)]
                    final_wheel.append(ace)
                    return {"Straight Flush": final_wheel}
                # If none of those checks are passed we know to return a regular flush
                return {"Flush": flush_arr[:5]}
                    
            # If a royal flush or straight flush is found we return because those are the 2 best poker hands
            # Otherwise the flush will just be stored in the flush variable in case it's needed later
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
            
            # Check for Four of a Kind
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
                                v += n[:1]
                                return {"Four of a Kind": v}
                return {"No Four of a Kind": "None Found"}
            
            # If Four of a Kind is found we can return that
            quads = quad_check(seven_cards)
            if "Four of a Kind" in quads:
                return quads
            
            # Check for Full House
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
                            if len(n) == 2 and k != c:
                                v += n
                                return {"Full House": v}
                            elif len(n) > 2 and k != c:
                                v += n
                                v.pop()
                                return {"Full House": v}
                return {"No Full House": "None Detected"}
            
            # If a Full House is found return that
            full_house = full_house_check(seven_cards)
            if "Full House" in full_house:
                return full_house
            
            # If a flush is present we know it is a regular flush so we can return it
            if "Flush Detected" in test_flush:
                return flush
            
            # Check for a straight
            def check_straight(cards_arr):
                straight_list, straight_values = [], set()
                pointer1, pointer2 = 0, 1
                while pointer2 < len(cards_arr):
                    first_num, second_num = cards_arr[pointer1], cards_arr[pointer2]
                    if first_num[0] - 1 == second_num[0]:
                        if first_num[0] not in straight_values:
                            straight_values.add(first_num[0])
                            straight_list.append(first_num[2])
                        if second_num[0] not in straight_values:
                            straight_values.add(second_num[0])
                            straight_list.append(second_num[2])
                    elif first_num[0] == second_num[0]:
                        pass
                    elif len(straight_list) >= 5:
                        break
                    else:
                        straight_list = [second_num[2]]
                        straight_values = set()
                        straight_values.add(second_num[0])
                    pointer1 += 1
                    pointer2 += 1
                if len(straight_list) >= 5:
                    return {"Straight": straight_list[:5]}
                # If no regular straight is found check for the Wheel Straight (A, 2, 3, 4, 5)
                wheel_list, wheel_set = [], set()
                for card in reversed(cards_arr):
                    if card[0] == 14:
                        if card[0] not in wheel_set:
                            wheel_set.add(card[0])
                            wheel_list.append(card[2])
                    elif card[0] == 2:
                        if card[0] not in wheel_set:
                            wheel_set.add(card[0])
                            wheel_list.append(card[2])
                    elif card[0] == 3:
                        if card[0] not in wheel_set:
                            wheel_set.add(card[0])
                            wheel_list.append(card[2])
                    elif card[0] == 4:
                        if card[0] not in wheel_set:
                            wheel_set.add(card[0])
                            wheel_list.append(card[2])
                    elif card[0] == 5:
                        if card[0] not in wheel_set:
                            wheel_set.add(card[0])
                            wheel_list.append(card[2])
                if len(wheel_list) == 5:
                    ace = wheel_list.pop()
                    final_wheel = [str_card for str_card in reversed(wheel_list)]
                    final_wheel.append(ace)
                    return {"Straight": final_wheel}
                return {"No Straight": "None Detected"}            

            straight = check_straight(seven_cards)
            if "Straight" in straight:
                return straight
            
            # Check for Three of a Kind
            def trips_check(seven_arr):
                trips_dict, trips_arr = {}, []
                for c in seven_arr:
                    if c[0] not in trips_dict:
                        trips_dict[c[0]] = [c[2]]
                    else:
                        trips_dict[c[0]].append(c[2])
                for k, v in trips_dict.items():
                    if len(v) == 3:
                        trips_arr += v
                        for c, n in trips_dict.items():
                            if c != k and len(trips_arr) < 5:
                                trips_arr += n
                if len(trips_arr) == 5:
                    return {"Three of a Kind": trips_arr}
                return {"No Three of a Kind": "None Found"}

            trips = trips_check(seven_cards)
            if "Three of a Kind" in trips:
                return trips
            
            # Check for two pair
            def check_two_pair(all_cards):
                two_pair_list, two_pair_dict = [], {}
                final_cards, card_set = [], set()
                for card in all_cards:
                    if card[0] not in two_pair_dict:
                        two_pair_dict[card[0]] = [card[2]]
                    else:
                        two_pair_dict[card[0]].append(card[2])
                for value in two_pair_dict.values():
                    if len(value) == 2:
                        two_pair_list.append(value)
                if len(two_pair_list) >= 2:
                    final_cards.append(two_pair_list[0][0])
                    final_cards.append(two_pair_list[0][1])
                    final_cards.append(two_pair_list[1][0])
                    final_cards.append(two_pair_list[1][1])
                    card_set.add(two_pair_list[0][0])
                    card_set.add(two_pair_list[0][1])
                    card_set.add(two_pair_list[1][0])
                    card_set.add(two_pair_list[1][1])
                    for c in all_cards:
                        if c[2] not in card_set:
                            final_cards.append(c[2])
                            break
                    return {"Two Pair": final_cards}
                return {"No Two Pair": "None Detected"}
            
            two_pair = check_two_pair(seven_cards)
            if "Two Pair" in two_pair:
                return two_pair
            
            # Check for a single pair
            def check_pair(check_arr):
                pair_set, pair_list = set(), []
                pair_dict = {}
                for c in check_arr:
                    if c[0] not in pair_dict:
                        pair_dict[c[0]] = [c[2]]
                    else:
                        pair_dict[c[0]].append(c[2])
                for v in pair_dict.values():
                    if len(v) == 2:
                        pair_list.append(v[0])
                        pair_list.append(v[1])
                        pair_set.add(v[0])
                        pair_set.add(v[1])
                if len(pair_list) == 2:
                    for card in check_arr:
                        if card[2] not in pair_set:
                            pair_list.append(card[2])
                        if len(pair_list) == 5:
                            return {"Pair": pair_list}
                return {"No Pair Found": "None Detected"}
            
            pair = check_pair(seven_cards)
            if "Pair" in pair:
                return pair

            # Get the 5 highest cards
            def high_cards(rem_cards):
                final_cards = [card[2] for card in rem_cards]
                return {"High Card": final_cards[:5]}

            # Since we made it to end of the function we know the hand entered is only a high card
            # We return the 5 highest cards as a result
            high = high_cards(seven_cards)
            return high
            
        except:
            abort(400, error="Invalid Input")


class Home(Resource):
    def get(self):
        base = "https://poker1230.pythonanywhere.com/"
        return {
            "URL Format": f"{base}<holecard1>/<holecard2>&<communitycard1>/<communitycard2>/<communitycard3>/<communitycard4>/<communitycard5>",
            "Example": f"{base}5h/5c&10s/Jd/2c/5s/9d",
            "Use lowercase letters to represent each suit": {
                "s": "\u2660",
                "c": "\u2663",
                "d": "\u2666",
                "h": "\u2665"
            },
            "All 52 Cards": {
                "Ace": ["As", "Ac", "Ad", "Ah"],
                "King": ["Ks", "Kc", "Kd", "Kh"],
                "Queen": ["Qs", "Qc", "Qd", "Qh"],
                "Jack": ["Js", "Jc", "Jd", "Jh"],
                "10": ["10s", "10c", "10d", "10h"],
                "9": ["9s", "9c", "9d", "9h"],
                "8": ["8s", "8c", "8d", "8h"],
                "7": ["7s", "7c", "7d", "7h"],
                "6": ["6s", "6c", "6d", "6h"],
                "5": ["5s", "5c", "5d", "5h"],
                "4": ["4s", "4c", "4d", "4h"],
                "3": ["3s", "3c", "3d", "3h"],
                "2": ["2s", "2c", "2d", "2h"],
            }
        }
    

api.add_resource(Home, "/")
api.add_resource(Poker, "/<string:hole1>/<string:hole2>&<string:flop1>/<string:flop2>/<string:flop3>/<string:turn>/<string:river>")
