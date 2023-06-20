from typing import List, Dict
from itertools import combinations
from functools import lru_cache
import random
from deck_of_cards import suits, Card, ranks
from evaluate_poker_hand import sort_hands_str, ranks_dict

hand_ranks = {
    'AA': 1, 'KK': 2, 'QQ': 3, 'AKs': 4, 'JJ': 5, 'AQs': 6, 'KQs': 7, 'AJs': 8, 'KJs': 9, 'TT': 10,
    'AKo': 11, 'ATs': 12, 'QJs': 13, 'KTs': 14, 'QTs': 15, 'JTs': 16, '99': 17, 'AQo': 18, 'A9s': 19, 'KQo': 20,
    '88': 21, 'K9s': 22, 'T9s': 23, 'A8s': 24, 'Q9s': 25, 'J9s': 26, 'AJo': 27, 'A5s': 28, '77': 29, 'A7s': 30,
    'KJo': 31, 'A4s': 32, 'A3s': 33, 'A6s': 34, 'QJo': 35, '66': 36, 'K8s': 37, 'T8s': 38, 'A2s': 39, '98s': 40,
    'J8s': 41, 'ATo': 42, 'Q8s': 43, 'K7s': 44, 'KTo': 45, '55': 46, 'JTo': 47, '87s': 48, 'QTo': 49, '44': 50,
    '33': 51, '22': 52, 'K6s': 53, '97s': 54, 'K5s': 55, '76s': 56, 'T7s': 57, 'K4s': 58, 'K3s': 59, 'K2s': 60,
    'Q7s': 61, '86s': 62, '65s': 63, 'J7s': 64, '54s': 65, 'Q6s': 66, '75s': 67, '96s': 68, 'Q5s': 69, '64s': 70,
    'Q4s': 71, 'Q3s': 72, 'T9o': 73, 'T6s': 74, 'Q2s': 75, 'A9o': 76, '53s': 77, '85s': 78, 'J6s': 79, 'J9o': 80, 
    'K9o': 81, 'J5s': 82, 'Q9o': 83, '43s': 84, '74s': 85, 'J4s': 86, 'J3s': 87, '95s': 88, 'J2s': 89, '63s': 90,
    'A8o': 91, '52s': 92, 'T5s': 93, '84s': 94, 'T4s': 95, 'T3s': 96, '42s': 97, 'T2s': 98, '98o': 99, 'T8o': 100,
    'A5o': 101, 'A7o': 102, '73s': 103, 'A4o': 104, '32s': 105, '94s': 106, '93s': 107, 'J8o': 108, 'A3o': 109, '62s': 110,
    '92s': 111, 'K8o': 112, 'A6o': 113, '87o': 114, 'Q8o': 115, '83s': 116, 'A2o': 117, '82s': 118, '97o': 119, '72s': 120,
    '76o': 121, 'K7o': 122, '65o': 123, 'T7o': 124, 'K6o': 125, '86o': 126, '54o': 127, 'K5o': 128, 'J7o': 129, '75o': 130,
    'Q7o': 131, 'K4o': 132, 'K3o': 133, 'K2o': 134, '96o': 135, '64o': 136, 'Q6o': 137, '53o': 138, '85o': 139, 'T6o': 140,
    'Q5o': 141, '43o': 142, 'Q4o': 143, 'Q3o': 144, 'Q2o': 145, '74o': 146, 'J6o': 147, '63o': 148, 'J5o': 149, '95o': 150,
    '52o': 151, 'J4o': 152, 'J3o': 153, '42o': 154, 'J2o': 155, '84o': 156, 'T5o': 157, 'T4o': 158, '32o': 159, 'T3o': 160, 
    '73o': 161, 'T2o': 162, '62o': 163, '94o': 164, '93o': 165, '92o': 166, '83o': 167, '82o': 168, '72o': 169
}

def generate_two_card_hands() -> List[str]:
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    suits = ['s', 'o']
    two_card_hands = []

    for i in range(len(ranks)):
        for j in range(len(ranks)):
            if ranks.index(ranks[i]) == ranks.index(ranks[j]):
                hand = ranks[i] + ranks[j]
            elif ranks.index(ranks[i]) < ranks.index(ranks[j]):
                hand = ranks[i] + ranks[j] + suits[0]
            elif ranks.index(ranks[i]) > ranks.index(ranks[j]):
                hand = ranks[j] + ranks[i] + suits[1]
            two_card_hands.append(hand)
    return two_card_hands

def convert_two_hand_string_to_list(hand_string: str) -> List[Card]:
    """Convert two card Hand into List of two Cards with random suits

    Args:
        hand_string (str): string of hand ex: "AA", "AKo", or "AKs"

    Returns:
        List[Card]: List of two Cards with random suits
    """
    
    ranks = [hand_string[0], hand_string[1]]
    hand_type = hand_string[2:]

    if hand_type == "s":
        suit1 = suit2 = random.choice(suits)
    else: # If Pair or off suit, assign two different random suits
        suit1, suit2 = random.sample(suits, 2)

    rank1, rank2 = ranks[0], ranks[1]
    card1 = Card(rank1,suit1)
    card2 = Card(rank2,suit2)
    hand_list = [card1, card2]
    return hand_list

def all_two_card_hand_list() -> List[List[Card]]:
    list_str = generate_two_card_hands()
    all_cards = []
    for hand_str in list_str:
        all_cards.append(convert_two_hand_string_to_list(hand_str))
    return all_cards

def calculate_ev(hand: str, opponent_hands: List[str]) -> float:
    # Simulate poker scenarios and calculate the expected value of the hand against opponent hands
    # Return the calculated expected value as a float
    return None

def rank_hands_by_ev(hand_rankings: Dict[str, float]) -> List[str]:
    # Rank the hands in descending order based on their expected value
    sorted_hands = sorted(hand_rankings, key=hand_rankings.get, reverse=True)
    return sorted_hands

def ev_based_hand_ranking() -> List[str]:
    hands = generate_two_card_hands()
    opponent_hands = list(combinations(hands, 2))  # Generate all possible combinations of opponent hands

    hand_rankings = {}  # Dictionary to store hand rankings based on expected value

    for hand in hands:
        ev_sum = 0.0
        for opponent_hand in opponent_hands:
            ev_sum += calculate_ev(hand, opponent_hand)
        average_ev = ev_sum / len(opponent_hands)
        hand_rankings[hand] = average_ev

    ranked_hands = rank_hands_by_ev(hand_rankings)
    return ranked_hands

def hand_strength(hand_string: str) -> int:
    return hand_ranks.get(hand_string, 170)

def convert_hand_to_str(hand: List[Card]) -> str:
    index1 = ranks.index(hand[0].value)
    index2 = ranks.index(hand[1].value)
    hand_str = ""
    if index1 < index2:
        hand_str = str(hand[1].value) + str(hand[0].value)
    else:
        hand_str = str(hand[0].value) + str(hand[1].value)
    if hand[0].suit == hand[1].suit:
        hand_str += "s"
    elif index1 != index2:
        hand_str += "o"
    return hand_str

def display_hand(hand: List[Card]) -> None:
    cards = [card.display() for card in hand]
    print(", ".join(cards))

def calculate_top_hands(all_hands: List[List[Card]], percentage: int) -> List[List[Card]]:
    num_hands = len(all_hands)
    num_hands_to_play = int(num_hands * percentage/100)

    sorted_hands = sorted(all_hands, key=lambda hand: hand_strength(convert_hand_to_str(hand)), reverse=False)
    top_hands = sorted_hands[:num_hands_to_play]
    
    for hand in top_hands:
        display_hand(hand)
    return top_hands

def calculate_top_range_str(percentage: int) -> List[str]:
    all_hand_str = generate_two_card_hands()
    num_hands = 1326
    count = 0
    num_hands_to_play = int(num_hands * percentage/100)

    sorted_hands = sorted(all_hand_str, key=lambda hand: hand_strength(hand), reverse=False)
    top_hands = []
    
    for hand in sorted_hands:
        top_hands.append(hand)
        if count >= num_hands_to_play:
            break
        elif len(hand) == 2: # If pair, 6 combinations
            count+=6
        elif hand[2] == "s": # If suited, 4 combinations
            count+=4
        elif hand[2] == "o": # If offsuit, 12 combinations
            count+=12
    return top_hands

def group_hands(hand_list:List[str]) -> List[str]:
    pairs = []
    suited_hands = []
    off_suit_hands = []
    hand_list = sort_hands_str(hand_list, False)

    for hand in hand_list:
        if len(hand) == 2:  # Pair
            pairs.append(hand)
        elif hand[-1] == 's':  # Suited hand
            suited_hands.append(hand)
        else:  # Off-suit hand
            off_suit_hands.append(hand)

    # Sort the groups
    pairs = group_pairs(pairs)
    suited_hands = group_non_pairs(suited_hands)
    off_suit_hands = group_non_pairs(off_suit_hands)

    grouped_hands = pairs + suited_hands + off_suit_hands
    return grouped_hands

def group_pairs(pair_list: List[str]) -> List[str]:
    groups = []
    group = []
    if not pair_list:
        return []
    for pair in pair_list:
        if not group or ranks_dict[pair[0]] - ranks_dict[group[-1][0]] == 1:
            group.append(pair)
        else:
            groups.append(group)
            group = [pair]
    
    groups.append(group)  # Add the last group
    
    result = []
    for group in groups:
        if len(group) == 1:
            result.append(f"{group[0]}")
        elif "AA" in group:
            result.append(f"{group[0]}+")
        else:
            result.append(f"{group[0]}-{group[-1]}")
    
    return result[::-1]

def group_non_pairs(non_pairs_list):
    result = []
    if not non_pairs_list:
        return []
    group_start = non_pairs_list[0]
    prev_hand = non_pairs_list[0]

    for hand in non_pairs_list[1:]:
        # Check if Same group, ex: 97o, 98o
        if hand[0] == prev_hand[0] and ranks_dict[hand[1]] - ranks_dict[prev_hand[1]] == 1:
            prev_hand = hand
        else:
            # Check if group is alone
            if group_start == prev_hand:
                result.append(group_start)
            elif ranks_dict[prev_hand[0]] - ranks_dict[prev_hand[1]] == 1:
                result.append(group_start + "+")
            else:
                result.append(group_start + "-" + prev_hand)
            group_start = hand
            prev_hand = hand
    #TODO: FIX THE PLUS
    if group_start == prev_hand:
        result.append(group_start)
    elif ranks_dict[prev_hand[0]] - ranks_dict[prev_hand[1]] == 1:
        result.append(group_start + "+")
    else:
        result.append(group_start + "-" + prev_hand)
    return result[::-1]

def ungroup_hands(hand_list: List[str]) -> List[str]:
    result = []
    for hand in hand_list:
        if len(hand) == 3:
            if hand[2] == "+": # If pairs through AA, ex: 99+
                hand_index = list(ranks_dict.keys()).index(hand[0])
                for rank in list(ranks_dict.keys())[hand_index:]:
                    result.append(rank + rank)
            else: # Lone suited/off Hand
                result.append(hand)
        elif len(hand) == 2: # Lone pair, ex: 99
            result.append(hand)
        elif hand[3] == "+": # if suited/off through, ex: KTs+
            hand_index_1 = list(ranks_dict.keys()).index(hand[0])
            hand_index_2 = list(ranks_dict.keys()).index(hand[1])
            for rank in list(ranks_dict.keys())[hand_index_2:hand_index_1]:
                result.append(hand[0] + rank + hand[2])
        elif hand[3] == "-": # ex: J8s-JTs
            hand_index_1 = list(ranks_dict.keys()).index(hand[0])
            hand_index_2 = list(ranks_dict.keys()).index(hand[1])
            hand_index_3 = list(ranks_dict.keys()).index(hand[5])
            for rank in list(ranks_dict.keys())[hand_index_2:hand_index_3+1]:
                result.append(hand[0] + rank + hand[2])
    return result
