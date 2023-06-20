import unittest

from evaluate_poker_hand import evaluate_five_card_hand, evaluate_hand, HandRank, evaluate_two_card_hand, sort_hands_str
from deck_of_cards import Card, Deck, Board, Player

ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K' , 'A']

class TestEvaluateFiveCardHand(unittest.TestCase):
    def test_royal_flush(self):
        hand1 = [Card('A', 'Spade'), Card('K', 'Spade'), Card('Q', 'Spade'), Card('J', 'Spade'), Card('T', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand1), (HandRank['ROYAL_FLUSH'],[]))

        hand2 = [Card('J', 'Heart'), Card('K', 'Heart'), Card('T', 'Heart'), Card('A', 'Heart'), Card('Q', 'Heart')]
        self.assertEqual(evaluate_five_card_hand(hand2), (HandRank['ROYAL_FLUSH'],[]))

        hand3 = [Card('J', 'Heart'), Card('K', 'Spade'), Card('T', 'Heart'), Card('A', 'Heart'), Card('Q', 'Heart')]
        self.assertNotEqual(evaluate_five_card_hand(hand3), (HandRank['ROYAL_FLUSH'],[]))

    def test_straight_flush(self):
        hand1 = [Card('K', 'Spade'), Card('Q', 'Spade'), Card('J', 'Spade'), Card('T', 'Spade'), Card('9', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand1), (HandRank['STRAIGHT_FLUSH'],[13]))

        hand2 = [Card('Q', 'Spade'), Card('K', 'Spade'), Card('9', 'Spade'), Card('T', 'Spade') , Card('J', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand2), (HandRank['STRAIGHT_FLUSH'],[13]))

        hand3 = [Card('Q', 'Spade'), Card('K', 'Spade'), Card('9', 'Heart'), Card('T', 'Spade') , Card('J', 'Spade')]
        self.assertNotEqual(evaluate_five_card_hand(hand3), (HandRank['STRAIGHT_FLUSH'],[13]))

        hand4 = [Card('3', 'Diamond'), Card('5', 'Diamond'), Card('2', 'Diamond'), Card('6', 'Diamond') , Card('4', 'Diamond')]
        self.assertEqual(evaluate_five_card_hand(hand4), (HandRank['STRAIGHT_FLUSH'],[6]))
        # Bottom Straight
        hand5 = [Card('3', 'Diamond'), Card('5', 'Diamond'), Card('2', 'Diamond'), Card('A', 'Diamond') , Card('4', 'Diamond')]
        self.assertEqual(evaluate_five_card_hand(hand5), (HandRank['STRAIGHT_FLUSH'],[5]))

    def test_four_kind(self):
        hand1 = [Card('K', 'Spade'), Card('K', 'Heart'), Card('K', 'Diamond'), Card('K', 'Club'), Card('9', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand1), (HandRank['FOUR_OF_A_KIND'],[13,9]))

        hand2 = [Card('K', 'Spade'), Card('K', 'Heart'), Card('9', 'Spade'), Card('K', 'Diamond'), Card('K', 'Club')]
        self.assertEqual(evaluate_five_card_hand(hand2), (HandRank['FOUR_OF_A_KIND'],[13,9]))

        hand3 = [Card('9', 'Spade'), Card('9', 'Heart'), Card('9', 'Diamond'), Card('9', 'Club'), Card('K', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand3), (HandRank['FOUR_OF_A_KIND'],[9,13]))

        hand4 = [Card('3', 'Spade'), Card('3', 'Heart'), Card('3', 'Diamond'), Card('3', 'Club'), Card('A', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand4), (HandRank['FOUR_OF_A_KIND'],[3,14]))

        hand5 = [Card('A', 'Spade'), Card('A', 'Heart'), Card('A', 'Diamond'), Card('A', 'Club'), Card('J', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand5), (HandRank['FOUR_OF_A_KIND'],[14,11]))

    def test_full_house(self):
        hand1 = [Card('K', 'Spade'), Card('K', 'Heart'), Card('K', 'Diamond'), Card('9', 'Club'), Card('9', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand1), (HandRank['FULL_HOUSE'],[13,9]))

        hand2 = [Card('K', 'Spade'), Card('K', 'Heart'), Card('9', 'Diamond'), Card('9', 'Club'), Card('9', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand2), (HandRank['FULL_HOUSE'],[9,13]))

        hand3 = [Card('A', 'Spade'), Card('A', 'Heart'), Card('A', 'Diamond'), Card('4', 'Club'), Card('4', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand3), (HandRank['FULL_HOUSE'],[14,4]))

        hand4 = [Card('A', 'Spade'), Card('A', 'Heart'), Card('7', 'Diamond'), Card('7', 'Club'), Card('7', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand4), (HandRank['FULL_HOUSE'],[7,14]))

    def test_flush(self):
        hand1 = [Card('A', 'Club'), Card('K', 'Club'), Card('9', 'Club'), Card('7', 'Club'), Card('6', 'Club')]
        self.assertEqual(evaluate_five_card_hand(hand1), (HandRank['FLUSH'],[14,13,9,7,6]))

        hand2 = [Card('J', 'Club'), Card('7', 'Club'), Card('6', 'Club'), Card('3', 'Club'), Card('9', 'Club')]
        self.assertEqual(evaluate_five_card_hand(hand2), (HandRank['FLUSH'],[11,9,7,6,3]))

        hand3 = [Card('2', 'Club'), Card('5', 'Club'), Card('8', 'Club'), Card('7', 'Club'), Card('6', 'Club')]
        self.assertEqual(evaluate_five_card_hand(hand3), (HandRank['FLUSH'],[8,7,6,5,2]))

    def test_straight(self):
        # Bottom Straight
        hand1 = [Card('3', 'Spade'), Card('2', 'Heart'), Card('A', 'Diamond'), Card('5', 'Club'), Card('4', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand1), (HandRank['STRAIGHT'],[5]))
        # Top Straight
        hand2 = [Card('K', 'Spade'), Card('J', 'Heart'), Card('A', 'Diamond'), Card('T', 'Club'), Card('Q', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand2), (HandRank['STRAIGHT'], [14]))

        hand3 = [Card('3', 'Spade'), Card('7', 'Heart'), Card('6', 'Diamond'), Card('5', 'Club'), Card('4', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand3), (HandRank['STRAIGHT'],[7]))
        # Straight can't wrap from the top to bottom
        hand4 = [Card('K', 'Spade'), Card('Q', 'Heart'), Card('A', 'Diamond'), Card('2', 'Club'), Card('3', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand4), (HandRank['HIGH_CARD'],[14,13,12,3,2]))

    def test_three_kind(self):
        hand1 = [Card('4', 'Spade'), Card('4', 'Heart'), Card('4', 'Diamond'), Card('T', 'Club'), Card('J', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand1), (HandRank['THREE_OF_A_KIND'],[4,11,10]))

        hand2 = [Card('A', 'Spade'), Card('A', 'Heart'), Card('A', 'Diamond'), Card('K', 'Club'), Card('3', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand2), (HandRank['THREE_OF_A_KIND'],[14,13,3]))

        hand3 = [Card('3', 'Spade'), Card('3', 'Heart'), Card('3', 'Diamond'), Card('A', 'Club'), Card('5', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand3), (HandRank['THREE_OF_A_KIND'],[3,14,5]))

    def test_two_pair(self):
        hand1 = [Card('4', 'Spade'), Card('4', 'Heart'), Card('3', 'Diamond'), Card('3', 'Club'), Card('J', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand1), (HandRank['TWO_PAIR'],[4,3,11]))

        hand2 = [Card('6', 'Spade'), Card('3', 'Heart'), Card('A', 'Diamond'), Card('6', 'Club'), Card('A', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand2), (HandRank['TWO_PAIR'],[14,6,3]))

        hand3 = [Card('2', 'Spade'), Card('A', 'Heart'), Card('K', 'Diamond'), Card('2', 'Club'), Card('K', 'Spade')]
        self.assertEqual(evaluate_five_card_hand(hand3), (HandRank['TWO_PAIR'],[13,2,14]))

    def test_pair(self):
        hand1 = [Card('4', 'Spade'), Card('3', 'Heart'), Card('2', 'Diamond'), Card('A', 'Club'), Card('4', 'Heart')]
        self.assertEqual(evaluate_five_card_hand(hand1), (HandRank['PAIR'],[4,14,3,2]))

        hand2 = [Card('K', 'Spade'), Card('A', 'Heart'), Card('2', 'Diamond'), Card('A', 'Club'), Card('J', 'Heart')]
        self.assertEqual(evaluate_five_card_hand(hand2), (HandRank['PAIR'],[14,13,11,2]))

    def test_high_card(self):
        hand1 = [Card('4', 'Spade'), Card('3', 'Heart'), Card('2', 'Diamond'), Card('A', 'Club'), Card('6', 'Heart')]
        self.assertEqual(evaluate_five_card_hand(hand1), (HandRank['HIGH_CARD'],[14,6,4,3,2]))
        # J Q K A 2
        hand2 = [Card('J', 'Spade'), Card('K', 'Heart'), Card('Q', 'Diamond'), Card('A', 'Club'), Card('2', 'Heart')]
        self.assertEqual(evaluate_five_card_hand(hand2), (HandRank['HIGH_CARD'],[14,13,12,11,2]))
        # Q K A 2 3
        hand3 = [Card('3', 'Spade'), Card('K', 'Heart'), Card('Q', 'Diamond'), Card('A', 'Club'), Card('2', 'Heart')]
        self.assertEqual(evaluate_five_card_hand(hand3), (HandRank['HIGH_CARD'],[14,13,12,3,2]))
        # K A 2 3 4
        hand4 = [Card('3', 'Spade'), Card('K', 'Heart'), Card('4', 'Diamond'), Card('A', 'Club'), Card('2', 'Heart')]
        self.assertEqual(evaluate_five_card_hand(hand4), (HandRank['HIGH_CARD'],[14,13,4,3,2]))

class TestEvaluateTwoCardHand(unittest.TestCase):
    def test_high_card(self):
        hand1 = [Card("2", "Heart"), Card("6", "Diamond")]
        self.assertEqual(evaluate_two_card_hand(hand1), (0, [6, 2]))

        hand2 = [Card("A", "Club"), Card("K", "Spade")]
        self.assertEqual(evaluate_two_card_hand(hand2), (0, [14, 13]))

        hand3 = [Card("J", "Spade"), Card("9", "Spade")]
        self.assertEqual(evaluate_two_card_hand(hand3), (0, [11, 9]))

        hand4 = [Card("6", "Club"), Card("A", "Spade")]
        self.assertEqual(evaluate_two_card_hand(hand4), (0, [14, 6]))

    def test_pair(self):
        hand1 = [Card("9", "Diamond"), Card("9", "Heart")]
        self.assertEqual(evaluate_two_card_hand(hand1), (1, [9]))

        hand2 = [Card("A", "Club"), Card("A", "Spade")]
        self.assertEqual(evaluate_two_card_hand(hand2), (1, [14]))

        hand3 = [Card("Q", "Heart"), Card("Q", "Diamond")]
        self.assertEqual(evaluate_two_card_hand(hand3), (1, [12]))

class TestEvaluateHand(unittest.TestCase):
    def test_full_board_best(self):
        board1 = [Card('A', 'Spade'), Card('K', 'Spade'), Card('Q', 'Spade'), Card('J', 'Spade'), Card('T', 'Spade')]
        hand1 = [Card('A', 'Heart'), Card('A', 'Diamond')]
        self.assertEqual(evaluate_hand(board1, hand1), (HandRank['ROYAL_FLUSH'],[]))

        board2 = [Card('A', 'Spade'), Card('K', 'Spade'), Card('Q', 'Spade'), Card('J', 'Spade'), Card('T', 'Spade')]
        hand2 = [Card('A', 'Heart'), Card('A', 'Diamond')]
        self.assertEqual(evaluate_hand(board2, hand2)[0], 9)
        # 3 pair, board is best
        board3 = [Card('K', 'Spade'), Card('K', 'Heart'), Card('J', 'Spade'), Card('J', 'Diamond'), Card('T', 'Club')]
        hand3 = [Card('3', 'Heart'), Card('3', 'Diamond')]
        self.assertEqual(evaluate_hand(board3, hand3), (HandRank['TWO_PAIR'],[13,11,10]))

    def test_full_board_one_card_hand(self):
        board1 = [Card('A', 'Diamond'), Card('K', 'Spade'), Card('Q', 'Spade'), Card('J', 'Spade'), Card('T', 'Spade')]
        hand1 = [Card('A', 'Heart'), Card('A', 'Spade')]
        self.assertEqual(evaluate_hand(board1, hand1), (HandRank['ROYAL_FLUSH'],[]))

        board2 = [Card('K', 'Spade'), Card('K', 'Heart'), Card('3', 'Diamond'), Card('9', 'Club'), Card('9', 'Spade')]
        hand2 = [Card('K', 'Club'), Card('3', 'Spade')]
        self.assertEqual(evaluate_hand(board2, hand2), (HandRank['FULL_HOUSE'],[13,9]))

        board3 = [Card('4', 'Spade'), Card('9', 'Heart'), Card('8', 'Diamond'), Card('A', 'Club'), Card('6', 'Heart')]
        hand3 = [Card('K', 'Club'), Card('3', 'Spade')]
        self.assertEqual(evaluate_hand(board3, hand3), (HandRank['HIGH_CARD'],[14,13,9,8,6]))

    def test_flop_two_card_hand(self):
        board1 = Board([Card("J", "Spade"), Card("4", "Club"), Card("2", "Diamond")])
        player1 = Player("Player 1", [Card("A", "Spade"), Card("K", "Heart")])
        player2 = Player("Player 2", [Card("Q", "Diamond"), Card("J", "Club")])
        self.assertEqual(evaluate_hand(board1.board, player1.hand), (HandRank['HIGH_CARD'],[14,13,11,4,2]))
        self.assertEqual(evaluate_hand(board1.board, player2.hand), (HandRank['PAIR'],[11,12,4,2]))

    def test_board_two_card_hand(self):
        # Royal Flush 
        board1 = [Card('A', 'Diamond'), Card('9', 'Heart'), Card('Q', 'Spade'), Card('J', 'Spade'), Card('T', 'Spade')]
        hand1 = [Card('K', 'Spade'), Card('A', 'Spade')]
        self.assertEqual(evaluate_hand(board1, hand1), (HandRank['ROYAL_FLUSH'],[]))
        # Straight Flush
        board2 = [Card('3', 'Heart'), Card('5', 'Club'), Card('2', 'Diamond'), Card('6', 'Diamond') , Card('4', 'Diamond')]
        hand2 = [Card('3', 'Diamond'), Card('5', 'Diamond')]
        self.assertEqual(evaluate_hand(board2, hand2), (HandRank['STRAIGHT_FLUSH'],[6]))
        # Bottom Straight Flush
        board3 = [Card('2', 'Club'), Card('7', 'Diamond'), Card('2', 'Diamond'), Card('A', 'Diamond') , Card('4', 'Diamond')]
        hand3 = [Card('3', 'Diamond'), Card('5', 'Diamond')]
        self.assertEqual(evaluate_hand(board3, hand3), (HandRank['STRAIGHT_FLUSH'],[5]))
        # Four of a Kind 
        board4 = [Card('7', 'Spade'), Card('5', 'Heart'), Card('3', 'Diamond'), Card('3', 'Club'), Card('A', 'Spade')]
        hand4 = [Card('3', 'Diamond'), Card('3', 'Club')]
        self.assertEqual(evaluate_hand(board4, hand4), (HandRank['FOUR_OF_A_KIND'],[3,14]))
        # Four of a Kind with A
        board5 = [Card('6', 'Spade'), Card('T', 'Club'), Card('A', 'Diamond'), Card('A', 'Club'), Card('J', 'Spade')]
        hand5 = [Card('A', 'Diamond'), Card('A', 'Club')]
        self.assertEqual(evaluate_hand(board5, hand5), (HandRank['FOUR_OF_A_KIND'],[14,11]))
        # Full House A 3 of a kind
        board6 = [Card('A', 'Spade'), Card('3', 'Heart'), Card('7', 'Diamond'), Card('4', 'Club'), Card('4', 'Spade')]
        hand6 = [Card('A', 'Diamond'), Card('A', 'Club')]
        self.assertEqual(evaluate_hand(board6, hand6), (HandRank['FULL_HOUSE'],[14,4]))
        # Full House A pair
        board7 = [Card('9', 'Spade'), Card('8', 'Heart'), Card('7', 'Diamond'), Card('7', 'Club'), Card('7', 'Spade')]
        hand7 = [Card('A', 'Diamond'), Card('A', 'Club')]
        self.assertEqual(evaluate_hand(board7, hand7), (HandRank['FULL_HOUSE'],[7,14]))
        # Flush
        board8 = [Card('9', 'Heart'), Card('7', 'Club'), Card('8', 'Diamond'), Card('3', 'Club'), Card('9', 'Club')]
        hand8 = [Card('6', 'Club'), Card('J', 'Club')]
        self.assertEqual(evaluate_hand(board8, hand8), (HandRank['FLUSH'],[11,9,7,6,3]))
        # Bottom Straight
        board9 = [Card('3', 'Spade'), Card('2', 'Heart'), Card('9', 'Diamond'), Card('T', 'Club'), Card('4', 'Spade')]
        hand9 = [Card('A', 'Club'), Card('5', 'Club')]
        self.assertEqual(evaluate_hand(board9, hand9), (HandRank['STRAIGHT'],[5]))
        # Top Straight
        board10 = [Card('K', 'Spade'), Card('J', 'Heart'), Card('6', 'Diamond'), Card('7', 'Club'), Card('Q', 'Spade')]
        hand10 = [Card('A', 'Club'), Card('T', 'Club')]
        self.assertEqual(evaluate_hand(board10, hand10), (HandRank['STRAIGHT'], [14]))
        # Regular Straight
        board11 = [Card('9', 'Spade'), Card('7', 'Heart'), Card('6', 'Diamond'), Card('T', 'Club'), Card('4', 'Spade')]
        hand11 = [Card('3', 'Club'), Card('5', 'Club')]
        self.assertEqual(evaluate_hand(board11, hand11), (HandRank['STRAIGHT'],[7]))
        # 3 of a kind
        board12 = [Card('9', 'Spade'), Card('T', 'Heart'), Card('4', 'Diamond'), Card('J', 'Club'), Card('5', 'Spade')]
        hand12 = [Card('4', 'Heart'), Card('4', 'Club')]
        self.assertEqual(evaluate_hand(board12, hand12), (HandRank['THREE_OF_A_KIND'],[4,11,10]))
        # Two pair
        board13 = [Card('7', 'Spade'), Card('3', 'Heart'), Card('4', 'Diamond'), Card('6', 'Club'), Card('A', 'Spade')]
        hand13 = [Card('4', 'Heart'), Card('A', 'Club')]
        self.assertEqual(evaluate_hand(board13, hand13), (HandRank['TWO_PAIR'],[14,4,7]))
        # Pair
        board14 = [Card('2', 'Spade'), Card('3', 'Heart'), Card('6', 'Diamond'), Card('7', 'Club'), Card('4', 'Diamond')]
        hand14 = [Card('4', 'Heart'), Card('A', 'Club')]
        self.assertEqual(evaluate_hand(board14, hand14), (HandRank['PAIR'],[4,14,7,6]))
        # High Card
        board15 = [Card('4', 'Spade'), Card('3', 'Heart'), Card('2', 'Diamond'), Card('9', 'Club'), Card('7', 'Heart')]
        hand15 = [Card('T', 'Heart'), Card('A', 'Club')]
        self.assertEqual(evaluate_hand(board15, hand15), (HandRank['HIGH_CARD'],[14,10,9,7,4]))

class TestSortHandsStr(unittest.TestCase):
    def test_ascending(self):
        hand_list = ['AA', 'Q9s', 'AKo', 'K9o', '77', 'J9o', '62s', 'Q2o', 'T9o', '88']
        sorted_hands = sort_hands_str(hand_list, False)
        expected = ['62s', '77', '88', 'T9o', 'J9o', 'Q2o', 'Q9s', 'K9o', 'AKo', 'AA']
        self.assertEqual(sorted_hands, expected)
