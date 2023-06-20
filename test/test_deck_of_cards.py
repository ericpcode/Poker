import unittest
from io import StringIO

from deck_of_cards import Card, Deck, Player, Board, deal_cards, deal_flop

suits = ['Club', 'Diamond', 'Heart',  'Spade']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K' , 'A']

class TestCard(unittest.TestCase):
    def test_iter(self):
        card = Card('A', 'Spade')
        self.assertEqual(list(card), ['A', 'Spade'])

    def test_card_equality(self):
        card1 = Card('Ace', 'Spades')
        card2 = Card('Ace', 'Spades')
        card3 = Card('Ace', 'Hearts')
        self.assertEqual(card1, card2)
        self.assertNotEqual(card1, card3)

    def test_display(self):
        card = Card('3', 'Diamond')
        expected = '3 of Diamond'
        self.assertEqual(card.display(), expected)

class TestDeck(unittest.TestCase):
    def test_build(self):
        deck1 = Deck()
        expected_cards = [Card(value, suit) for value in ranks for suit in suits]
        # check that the deck has 52 cards
        self.assertEqual(len(deck1.cards), 52)  
        self.assertListEqual(deck1.cards, expected_cards)
        
    def test_shuffle(self):
        deck1 = Deck()
        deck2 = Deck()
        deck2.shuffle()
        # check that both decks have the same number of cards
        self.assertEqual(len(deck1.cards), len(deck2.cards))
        # check that the shuffled deck is not in the same order as the unshuffled deck
        self.assertNotEqual(deck1.cards, deck2.cards)    
    
    def test_draw_card(self):
        deck = Deck()
        num_cards = len(deck.cards)
        drawn_cards = []
        for i in range(num_cards):
            card = deck.draw_card()
            drawn_cards.append(card)
            self.assertNotIn(card, deck.cards)
            self.assertIn(card, drawn_cards)
            # check that all cards were drawn
            self.assertEqual(len(drawn_cards) + len(deck.cards), 52)
        self.assertEqual(len(deck.cards), 0)

    def test_remove_cards(self):
        deck = Deck()
        card1 = Card('A' , 'Club')
        card2 = Card('4' , 'Heart')
        card3 = Card('8' , 'Club')
        card4 = Card('T' , 'Diamond')
        cardList = [card1, card2, card3, card4]
        card5 = Card('J' , 'Spade')
        card6 = Card('J' , 'Spade')
        # check that cards in cardlist are in deck
        for card in cardList:
            self.assertTrue(deck.has_card(card))
        # check that cards in cardlist and deck is 52
        self.assertTrue(deck.has_card(card5))
        self.assertTrue(len(deck.cards), 52)
        # check that removing cards from Card List
        deck.remove_cards(cardList)
        for card in cardList:
            self.assertFalse(deck.has_card(card))
        self.assertTrue(len(deck.cards), 48)
        # check removing card5
        deck.remove_cards([card5])
        self.assertFalse(deck.has_card(card5))
        self.assertTrue(len(deck.cards), 47)

        deck.cards.append(card6)
        self.assertTrue(len(deck.cards), 48)
        deck.remove_cards([card5])
        self.assertTrue(len(deck.cards), 47)
        self.assertFalse(deck.has_card(card5))
        self.assertFalse(deck.has_card(card6))

    def test_has_card(self):
        deck = Deck()
        card1 = Card('A', 'Spade')
        card2 = Card('K', 'Diamond')
        card3 = Card('11', 'Spade')
        self.assertTrue(deck.has_card(card1))
        self.assertTrue(deck.has_card(card2))
        self.assertFalse(deck.has_card(card3))
        card4 = deck.draw_card()
        self.assertFalse(deck.has_card(card4))

    def test_copy(self):
        deck = Deck()
        deck_copy = deck.copy()

        self.assertIsNot(deck, deck_copy)
        self.assertEqual(len(deck.cards), len(deck_copy.cards))
        self.assertEqual(deck.cards, deck_copy.cards)
        self.assertIsNot(deck.cards, deck_copy.cards)

    def test_display(self):
        deck = Deck()
        with StringIO() as buffer:
            for card in deck.cards:
                print(card.display(), file=buffer)
            output = buffer.getvalue().strip()
        expected_output = '\n'.join([f"{value} of {suit}" for value in ranks for suit in suits])
        self.assertEqual(output, expected_output)

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.player = Player("John", money=100)

    def test_draw(self):
        initial_hand_size = len(self.player.hand)
        self.player.draw(self.deck)
        new_hand_size = len(self.player.hand)
        self.assertEqual(new_hand_size, initial_hand_size + 1)
        self.assertEqual(len(self.deck.cards) + new_hand_size, 52)

    def test_iter(self):
        cards = [Card("A", "Spade"), Card("K", "Heart")]
        self.player.hand = cards
        self.assertEqual(list(self.player), cards)

    def test_display_hand(self):
        cards = [Card("A", "Spade"), Card("K", "Heart")]
        self.player.hand = cards
        expected = 'A of Spade, K of Heart'
        self.assertEqual(self.player.display_hand(), expected)  # Just checking that it runs without error

class TestBoard(unittest.TestCase):
    def test_change_card_pos_1(self):
        card1 = Card('A' , 'Club')
        card2 = Card('4' , 'Heart')
        card3 = Card('8' , 'Club')
        card4 = Card('10' , 'Diamond')
        card5 = Card('J' , 'Spade')
        newCard = Card('2', 'Diamond')
        board1 = Board([card1, card2, card3, card4, card5])
        board2 = Board([newCard, card2, card3, card4, card5])
        board1.change_card_pos(1, newCard)
        self.assertEqual(board1.board,board2.board)

    def test_change_card_pos_2(self):
        card1 = Card('A' , 'Club')
        card2 = Card('4' , 'Heart')
        card3 = Card('8' , 'Club')
        card4 = Card('10' , 'Diamond')
        card5 = Card('J' , 'Spade')
        newCard = Card('2', 'Diamond')
        board1 = Board([card1, card2, card3, card4, card5])
        board2 = Board([card1, newCard, card3, card4, card5])
        board1.change_card_pos(2, newCard)
        self.assertEqual(board1.board,board2.board)

    def test_change_card_pos_3(self):
        card1 = Card('A' , 'Club')
        card2 = Card('4' , 'Heart')
        card3 = Card('8' , 'Club')
        card4 = Card('10' , 'Diamond')
        card5 = Card('J' , 'Spade')
        newCard = Card('2', 'Diamond')
        board1 = Board([card1, card2, card3, card4, card5])
        board2 = Board([card1, card2, newCard, card4, card5])
        board1.change_card_pos(3, newCard)
        self.assertEqual(board1.board,board2.board)

    def test_change_card_pos_4(self):
        card1 = Card('A' , 'Club')
        card2 = Card('4' , 'Heart')
        card3 = Card('8' , 'Club')
        card4 = Card('10' , 'Diamond')
        card5 = Card('J' , 'Spade')
        newCard = Card('2', 'Diamond')
        board1 = Board([card1, card2, card3, card4, card5])
        board2 = Board([card1, card2, card3, newCard, card5])
        board1.change_card_pos(4, newCard)
        self.assertEqual(board1.board,board2.board)
    
    def test_change_card_pos_5(self):
        card1 = Card('A' , 'Club')
        card2 = Card('4' , 'Heart')
        card3 = Card('8' , 'Club')
        card4 = Card('10' , 'Diamond')
        card5 = Card('J' , 'Spade')
        newCard = Card('2', 'Diamond')
        board1 = Board([card1, card2, card3, card4, card5])
        board2 = Board([card1, card2, card3, card4, newCard])
        board1.change_card_pos(5, newCard)
        self.assertEqual(board1.board,board2.board)

    def test_add_card_list(self):
        board = Board()
        cards = [Card('A', 'Spade'), Card('K', 'Heart'), Card('Q', 'Diamond')]
        board.add_card_list(cards)

        self.assertEqual(len(board.board), 3)
        self.assertEqual(board.board, cards)

    def test_display(self):
        card1 = Card('A' , 'Club')
        card2 = Card('4' , 'Heart')
        card3 = Card('8' , 'Club')
        card4 = Card('10' , 'Diamond')
        card5 = Card('J' , 'Spade')
        cardList= [card1, card2, card3, card4, card5]
        board1 = Board(cardList)
        expected = 'A of Club, 4 of Heart, 8 of Club, 10 of Diamond, J of Spade'
        self.assertEqual(board1.display(), expected)

class TestDeal(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_deal_flop(self):
        flop = deal_flop(self.deck)
        self.assertEqual(len(flop), 3)
        self.assertEqual(len(self.deck.cards), 49)

    def test_deal_cards(self):
        cards = deal_cards(2, self.deck)
        self.assertEqual(len(cards), 2)
        self.assertEqual(len(self.deck.cards), 50)