import unittest
from evaluate_poker_hand import HandRank
from poker_calculator import compare_single_hand_rank, compare_hand_ranks, evaluate_hand_ranks, simulate_win_tie_loss
from deck_of_cards import Player, Card, Board

class TestCompareSingleHandRank(unittest.TestCase):
    def test_compare_same_hand_rank(self):
        hand1 = (HandRank['THREE_OF_A_KIND'], [10, 9, 7])
        hand2 = (HandRank['THREE_OF_A_KIND'], [10, 9, 8])
        self.assertEqual(compare_single_hand_rank(hand1, hand2), -1)

        hand3 = (HandRank['FULL_HOUSE'], [7, 6])
        hand4 = (HandRank['FULL_HOUSE'], [7, 5])
        self.assertEqual(compare_single_hand_rank(hand3, hand4), 1)

        hand5 = (HandRank['FLUSH'], [14, 10, 8, 6, 3])
        hand6 = (HandRank['FLUSH'], [14, 10, 8, 6, 2])
        self.assertEqual(compare_single_hand_rank(hand5, hand6), 1)

        hand7 = (HandRank['PAIR'], [13, 10, 9, 7])
        hand8 = (HandRank['PAIR'], [13, 10, 9, 6])
        self.assertEqual(compare_single_hand_rank(hand7, hand8), 1)

        hand9 = (HandRank['HIGH_CARD'], [12, 10, 8, 6, 4])
        hand10 = (HandRank['HIGH_CARD'], [12, 10, 8, 6, 4])
        self.assertEqual(compare_single_hand_rank(hand9, hand10), 0)

        hand11 = (HandRank['ROYAL_FLUSH'], [])
        hand12 = (HandRank['ROYAL_FLUSH'], [])
        self.assertEqual(compare_single_hand_rank(hand11, hand12), 0)
        
        hand13 = (HandRank['TWO_PAIR'], [8, 3, 13])
        hand14 = (HandRank['TWO_PAIR'], [13, 10, 8])
        self.assertEqual(compare_single_hand_rank(hand13, hand14), -1)

        hand15 = (HandRank['PAIR'], [10, 7, 5, 4])
        hand16 = (HandRank['PAIR'], [8, 6, 5, 4])
        self.assertEqual(compare_single_hand_rank(hand15, hand16), 1)

    def test_compare_different_hand_rank(self):
        hand1 = (HandRank['THREE_OF_A_KIND'], [10, 9, 7])
        hand2 = (HandRank['FULL_HOUSE'], [7, 6])
        self.assertEqual(compare_single_hand_rank(hand1, hand2), -1)

        hand3 = (HandRank['FULL_HOUSE'], [7, 5])
        hand4 = (HandRank['FLUSH'], [14, 10, 8, 6, 3])
        self.assertEqual(compare_single_hand_rank(hand3, hand4), 1)

        hand5 = (HandRank['STRAIGHT'], [9])
        hand6 = (HandRank['HIGH_CARD'], [12, 10, 8, 6, 4])
        self.assertEqual(compare_single_hand_rank(hand5, hand6), 1)

        hand7 = (HandRank['PAIR'], [13, 10, 9, 7])
        hand8 = (HandRank['TWO_PAIR'], [8, 7, 4])
        self.assertEqual(compare_single_hand_rank(hand7, hand8), -1)

        hand9 = (0, [14, 13, 11, 4, 2])
        hand10 = (1, [11, 12, 4, 2])
        self.assertEqual(compare_single_hand_rank(hand9, hand10), -1)

class TestCompareHandRanks(unittest.TestCase):
    def test_compare_hand_ranks(self):
        player1 = Player("Player 1")
        player2 = Player("Player 2")
        player3 = Player("Player 3")

        # Hand ranks and kickers for each player
        players = {
            player1: (HandRank['THREE_OF_A_KIND'], [10, 9, 7]),
            player2: (HandRank['THREE_OF_A_KIND'], [10, 9, 8]),
            player3: (HandRank['FULL_HOUSE'], [7, 6]),
        }

        result = compare_hand_ranks(players)

        expected_result = {
            player1: "Loss",
            player2: "Loss",
            player3: "Win",
        }

        self.assertEqual(result, expected_result)

    def test_compare_hand_ranks123(self):
        player1 = Player("Player 1")
        player2 = Player("Player 2")
        player3 = Player("Player 3")

        # Define the hand ranks and kickers for each player
        players = {
            player1: (2, [10, 9, 8, 7, 6]),
            player2: (2, [10, 9, 8, 7, 5]),
            player3: (1, [14, 13, 12, 11, 10])
        }

        expected_results = {
            player1: "Win",
            player2: "Loss",
            player3: "Loss"
        }

        # Call the compare_hand_ranks function
        results = compare_hand_ranks(players)

        # Compare the actual results with the expected results
        self.assertEqual(results, expected_results)

    def test_compare_two_hands(self):
        player1 = Player("Player 1", [Card("A", "Spade"), Card("K", "Heart")])
        player2 = Player("Player 2", [Card("Q", "Diamond"), Card("J", "Club")])

        players = {
            player1: (0, [14, 13, 11, 4, 2]),
            player2: (1, [11, 12, 4, 2]),
        }

        expected_results = {
            player1: "Loss",
            player2: "Win",
        }
        results = compare_hand_ranks(players)
        self.assertEqual(results, expected_results)

class TestEvaluateHandRanks(unittest.TestCase):
    def test_no_board(self):
        player1 = Player("Player 1", [Card("A", "Spade"), Card("K", "Heart")])
        player2 = Player("Player 2", [Card("Q", "Diamond"), Card("J", "Club")])
        players = [player1, player2]
        board = None

        hand_ranks = evaluate_hand_ranks(board, players)

        self.assertEqual(len(hand_ranks), 2)
        self.assertEqual(hand_ranks[player1], (0, [14, 13])) 
        self.assertEqual(hand_ranks[player2], (0, [12, 11]))  

        player3 = Player("Player 3", [Card("3", "Spade"), Card("Q", "Heart")])
        player4 = Player("Player 4", [Card("3", "Diamond"), Card("9", "Club")])
        player5 = Player("Player 5", [Card("A", "Club"), Card("K", "Diamond")])
        player6 = Player("Player 6", [Card("5", "Heart"), Card("J", "Club")])
        player7 = Player("Player 7", [Card("T", "Spade"), Card("K", "Spade")])
        player8 = Player("Player 8", [Card("K", "Diamond"), Card("8", "Club")])
        player9 = Player("Player 9", [Card("J", "Diamond"), Card("2", "Club")])
        players = [player1, player2, player3, player4, player5, player6, player7, player8, player9]
        board = Board()

        hand_ranks2 = evaluate_hand_ranks(board, players)

        self.assertEqual(len(hand_ranks2), 9)
        self.assertEqual(hand_ranks2[player1], (0, [14, 13])) 
        self.assertEqual(hand_ranks2[player2], (0, [12, 11]))  
        self.assertEqual(hand_ranks2[player3], (0, [12, 3])) 
        self.assertEqual(hand_ranks2[player4], (0, [9, 3])) 
        self.assertEqual(hand_ranks2[player5], (0, [14, 13])) 
        self.assertEqual(hand_ranks2[player6], (0, [11, 5]))  
        self.assertEqual(hand_ranks2[player7], (0, [13, 10])) 
        self.assertEqual(hand_ranks2[player8], (0, [13, 8])) 
        self.assertEqual(hand_ranks2[player9], (0, [11, 2])) 

    def test_with_flop(self):
        player1 = Player("Player 1", [Card("A", "Diamonds"), Card("A", "Clubs")])
        player2 = Player("Player 2", [Card("K", "Spades"), Card("K", "Diamonds")])
        players = [player1, player2]
        board = Board([Card("Q", "Spades"), Card("J", "Diamonds"), Card("T", "Hearts")])

        hand_ranks = evaluate_hand_ranks(board, players)

        self.assertEqual(len(hand_ranks), 2)
        self.assertEqual(hand_ranks[player1], (1, [14, 12, 11, 10])) 
        self.assertEqual(hand_ranks[player2], (1, [13, 12, 11, 10]))

        board2 = Board([Card("J", "Spade"), Card("4", "Club"), Card("2", "Diamond")])
        player3 = Player("Player 3", [Card("A", "Spade"), Card("K", "Heart")])
        player4 = Player("Player 4", [Card("Q", "Diamond"), Card("J", "Club")])
        players2 = [player3, player4]

        hand_ranks2 = evaluate_hand_ranks(board2, players2)

        self.assertEqual(len(hand_ranks2), 2)
        self.assertEqual(hand_ranks2[player3], (0, [14, 13, 11, 4, 2])) 
        self.assertEqual(hand_ranks2[player4], (1, [11, 12, 4, 2]))
        


class TestSimulateWinTieLoss(unittest.TestCase):
    def test_board_size_0(self):
        board = Board([])
        players = [
            Player("Player 1", [Card("A", "Spade"), Card("K", "Heart")]),
            Player("Player 2", [Card("A", "Diamond"), Card("K", "Club")])
        ]
        results = simulate_win_tie_loss(board, players, n=10000)

        # Assert that the win, tie, and loss percentages are within an acceptable range
        self.assertAlmostEqual(results["Player 1"][0], 0.0, delta=0.05)
        self.assertAlmostEqual(results["Player 1"][1], 100.0, delta=0.05)
        self.assertAlmostEqual(results["Player 1"][2], 0.0, delta=0.05)

        self.assertAlmostEqual(results["Player 2"][0], 0.0, delta=0.05)
        self.assertAlmostEqual(results["Player 2"][1], 100.0, delta=0.05)
        self.assertAlmostEqual(results["Player 2"][2], 0.0, delta=0.05)

    def test_flop(self):
        board = Board([Card("J", "Spade"), Card("4", "Club"), Card("2", "Diamond")])
        players = [
            Player("Player 1", [Card("A", "Spade"), Card("K", "Heart")]),
            Player("Player 2", [Card("Q", "Diamond"), Card("J", "Club")])
        ]

        results = simulate_win_tie_loss(board, players, n=10000)

        self.assertAlmostEqual(results["Player 1"][0], 25.0, delta=5.00)
        self.assertAlmostEqual(results["Player 1"][1], 0.0, delta=5.00)
        self.assertAlmostEqual(results["Player 1"][2], 75.0, delta=5.00)

        self.assertAlmostEqual(results["Player 2"][0], 75.0, delta=5.00)
        self.assertAlmostEqual(results["Player 2"][1], 0.0, delta=5.00)
        self.assertAlmostEqual(results["Player 2"][2], 25.0, delta=5.00)