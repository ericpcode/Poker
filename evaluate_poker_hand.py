from typing import List, Tuple
from collections import Counter
from deck_of_cards import Card, Deck, Board, Player

ranks_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

HandRank = {
    'HIGH_CARD' : 0,
    'PAIR' : 1,
    'TWO_PAIR' : 2,
    'THREE_OF_A_KIND' : 3,
    'STRAIGHT' : 4,
    'FLUSH' : 5,
    'FULL_HOUSE' : 6,
    'FOUR_OF_A_KIND' : 7,
    'STRAIGHT_FLUSH' : 8,
    'ROYAL_FLUSH' : 9}


def evaluate_hand(board: List[Card], hand: List[Card]) -> Tuple[int, List[int]]:
    """Evaluate a two card hand and a board of size 3, 4, 5

    Args:
        board (List[Card]): List of Cards size: 3, 4, 5
        hand (List[Card]): Two card hand

    Returns:
        Tuple[int, List[int]]: A tuple containing the rank and kickers of the best 5 card hand/board combination
    """
    all_cards = board + hand
    best_rank = HandRank['HIGH_CARD']
    best_kickers = []

    # Evaluate each five-card combination
    for i in range(len(all_cards)-4):
        for j in range(i+1, len(all_cards)-3):
            for k in range(j+1, len(all_cards)-2):
                for l in range(k+1, len(all_cards)-1):
                    for m in range(l+1, len(all_cards)):
                        five_cards = [all_cards[i], all_cards[j], all_cards[k], all_cards[l], all_cards[m]]
                        rank, kickers = evaluate_five_card_hand(five_cards)
                        if rank > best_rank:
                            best_rank = rank
                            best_kickers = kickers
                        elif rank == best_rank and kickers > best_kickers:
                            best_kickers = kickers

    return (best_rank, best_kickers)

def sort_cards(cards: List[Card]):
    return sorted([ranks_dict[card.value] for card in cards], reverse=True)

def sort_hands_str(hand_list: List[str], order:bool= True) -> List[str]:
    sorted_hands = sorted(hand_list, key=lambda hand: (ranks_dict[hand[0]], ranks_dict[hand[1]]), reverse=order)
    return sorted_hands

def evaluate_two_card_hand(cards: List[Card]) -> Tuple[int, List[int]]:
    """Evaluate the rank and kickers of a two-card hand.

    Args:
        cards (List[Card]): List of two cards representing the hand.

    Returns:
        Tuple[int, List[int]]: A tuple containing the rank and kickers of the hand.
    """
    if cards[0].value == cards[1].value:  # Pair
        rank = 1
        kicker = ranks_dict[cards[0].value]
        return rank, [kicker]
    
    else:
        sorted_kickers = sort_cards(cards)
        rank = 0
        return rank, sorted_kickers

def evaluate_five_card_hand(cards: List[Card]) -> Tuple[int, List[int]]:
    """_summary_

    Args:
        cards (List[Card]): _description_

    Returns:
        Tuple[int, List[int]]: _description_
    """
    values = sort_cards(cards)
    suits = [card.suit for card in cards]

    is_flush = len(set(suits)) == 1
    is_top_straight = values == [14, 13, 12, 11, 10]
    is_straight = (values == list(range(values[0], values[0]-5, -1)) 
                   or values == [14, 5, 4, 3, 2]) # Bottom Straight: A, 2, 3, 4, 5 in order as: A, 5, 4, 3, 2
                   

    # Check for straight flush and royal flush
    if is_flush and is_straight:
        if values[0] == ranks_dict['A']:
            if values[4] == ranks_dict['T']:
                return (HandRank['ROYAL_FLUSH'], [])
            # Bottom Straight Flush: A, 2, 3, 4, 5 returning 5 as the highest
            return (HandRank['STRAIGHT_FLUSH'], [values[1]])
        # Straight Flush with the highest card returned
        return (HandRank['STRAIGHT_FLUSH'], [values[0]])

    # Check for four of a kind
    if values[0] == values[3]:
        return (HandRank['FOUR_OF_A_KIND'], [values[0], values[4]])
    if values[1] == values[4]:
        return (HandRank['FOUR_OF_A_KIND'], [values[1], values[0]])

    # Check for full house
    if values[0] == values[1] and values[2] == values[4]:
        return (HandRank['FULL_HOUSE'], [values[2], values[0]])
    if values[0] == values[2] and values[3] == values[4]:
        return (HandRank['FULL_HOUSE'], [values[0], values[3]])

    # Check for flush
    if is_flush:
        return (HandRank['FLUSH'], values)

    # Check for straight
    if is_straight or is_top_straight:
        if values[0] == ranks_dict['A'] and values[1] == ranks_dict['5']:
            # Bottom Straight, return 5 as the highest
            return (HandRank['STRAIGHT'], [values[1]])
        else:
            return (HandRank['STRAIGHT'], [values[0]])

    # Check for three of a kind
    for value, count in Counter(values).items():
        if count == 3:
            kickers = sorted([v for v in values if v != value], reverse=True)
            return (HandRank['THREE_OF_A_KIND'], [value] + kickers)

    # Check for two pair
    pairs = sorted([value for value, count in Counter(values).items() if count == 2], reverse=True)
    if len(pairs) == 2:
        other = [value for value in values if value not in pairs]
        return (HandRank['TWO_PAIR'], pairs + [other[0]])

    # Check for pair
    if len(pairs) == 1:
        kickers = sorted([value for value in values if value not in pairs], reverse=True)
        return (HandRank['PAIR'], pairs + kickers)

    # High card
    return (HandRank['HIGH_CARD'], values)

class TexasHoldem:
    """_summary_
    """
    def __init__(self, players: List[Player], deck: Deck, board: Board = Board):
        self.players = players
        self.deck = deck
        self.board = board

    # Deal each player 2 cards from deck
    def deal_players(self):
        cardsDealt = 0
        while cardsDealt < 2:
            for player in self.players:
                player.draw(self.deck)
            cardsDealt += 1

    def flop(self):
        for i in range(3):
            card = self.deck.draw_card()
            self.board.change_card_pos(i, card)

    def turn(self):
        card = self.deck.draw_card()
        self.board.change_card_pos(3, card)

    def river(self):
        card = self.deck.draw_card()
        self.board.change_card_pos(4, card)

    #def bet