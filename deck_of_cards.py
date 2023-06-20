# Deck of Cards

import random
from typing import List

suits = ['Club', 'Diamond', 'Heart',  'Spade']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __iter__(self):
        return iter((self.value, self.suit))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self.value == other.value and self.suit == other.suit
    
    def __hash__(self):
        return hash((self.value, self.suit))
    
    def display(self) -> str:
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.build()

    # Build a 52 unique card deck
    def build(self):
        for value in ranks:
            for suit in suits:
                self.cards.append(Card(value,suit))
    
    # Shuffle the deck using Fisher-Yates/Knuth shuffle algorithm
    def shuffle(self):
        n = len(self.cards)
        for i in range(n - 1, 0, -1):
            j = random.randrange(i + 1)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    # Return the top Card of the deck and remove it from the deck
    def draw_card(self) -> Card:
        return self.cards.pop()
    
    # Remove List of cards from deck
    def remove_cards(self, removal:List[Card]):
        self.cards = [card for card in self.cards if card not in removal]
    
    # Check if a card with the given value and suit exists in the deck
    def has_card(self, card: Card) -> bool:
        for c in self.cards:
            if c.value == card.value and c.suit == card.suit:
                return True
        return False
    
    def copy(self) -> 'Deck':
        """Create a copy of the deck object."""
        new_deck = Deck()
        new_deck.cards = self.cards.copy()
        return new_deck

    def display(self):
        for c in self.cards:
            c.display()

class Player:
    def __init__(self, name, hand:List[Card]=[], money=0):
        self.name = name
        self.hand = hand
        self.money = money

    # Add a Card from the deck to the Player's hand
    def draw(self, deck:Deck):
        self.hand.append(deck.draw_card())
        return self

    def __iter__(self):
        return iter(self.hand)

    def display_hand(self) -> str:
        hand_string = ""
        for card in self.hand:
            hand_string += card.display() + ", "
        return hand_string.rstrip(", ")

class Board:
    def __init__(self, board: List[Card]=[]):
        self.board = board
        
    # Change 1 card on board based on position number 1-5
    def change_card_pos(self, pos, newCard):
        try:
            self.board[pos - 1] = newCard
        except IndexError:
            self.board.append(newCard)

    def add_card_list(self, cardList:List[Card]):
        if cardList:
            for c in cardList:
                self.board.append(c)

    def display(self):
        card_strings = [card.display() for card in self.board]
        return ', '.join(card_strings)
    
def deal_flop(deck: Deck) -> List[Card]:
    flop = deal_cards(3, deck)
    return flop

def deal_cards(num_cards: int, deck: Deck) -> List[Card]:
    cards = []
    for _ in range(num_cards):
        card = deck.draw_card()
        cards.append(card)
    return cards

def convert_card_list_str(cards: List[Card], full_suit = False):
    result = []
    for card in cards:
        if full_suit:
            result.append(card.value + card.suit)
        else:
            result.append(card.value + card.suit[0])
    return result

