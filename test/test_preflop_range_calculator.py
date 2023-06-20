import unittest
from deck_of_cards import Card
from preflop_range_calculator import convert_two_hand_string_to_list, all_two_card_hand_list, hand_strength, hand_ranks, group_pairs, group_non_pairs, group_hands, ungroup_hands

class TestConvertTwoHandStringToList(unittest.TestCase):
    def test_pair(self):
        hand_string = "AA"
        hand_list = convert_two_hand_string_to_list(hand_string)
        self.assertEqual(len(hand_list), 2)
        self.assertIsInstance(hand_list[0], Card)
        self.assertIsInstance(hand_list[1], Card)
        self.assertEqual(hand_list[0].value, hand_list[1].value)
        self.assertEqual(hand_list[0].value, 'A')
        self.assertNotEqual(hand_list[0].suit, hand_list[1].suit)

    def test_suited_hand(self):
        hand_string = "AKs"
        hand_list = convert_two_hand_string_to_list(hand_string)
        self.assertEqual(len(hand_list), 2)
        self.assertIsInstance(hand_list[0], Card)
        self.assertIsInstance(hand_list[1], Card)
        self.assertNotEqual(hand_list[0].value, hand_list[1].value)
        self.assertEqual(hand_list[0].value, 'A')
        self.assertEqual(hand_list[1].value, 'K')
        self.assertEqual(hand_list[0].suit, hand_list[1].suit)

    def test_offsuit_hand(self):
        hand_string = "AKo"
        hand_list = convert_two_hand_string_to_list(hand_string)
        self.assertEqual(len(hand_list), 2)
        self.assertIsInstance(hand_list[0], Card)
        self.assertIsInstance(hand_list[1], Card)
        self.assertNotEqual(hand_list[0].value, hand_list[1].value)
        self.assertEqual(hand_list[0].value, 'A')
        self.assertEqual(hand_list[1].value, 'K')
        self.assertNotEqual(hand_list[0].suit, hand_list[1].suit)

class TestTwoCardHandList(unittest.TestCase):
    def test_all_two_card_hand_list(self):
        # Get the list of all two-card hands
        hand_list = all_two_card_hand_list()

        # Check the length of the hand list
        self.assertEqual(len(hand_list), 169)

        # Check if each element in the hand list is a list of two cards
        for hand in hand_list:
            self.assertIsInstance(hand, list)
            self.assertEqual(len(hand), 2)
            self.assertIsInstance(hand[0], Card)
            self.assertIsInstance(hand[1], Card)

class HandStrengthTest(unittest.TestCase):
    def test_hand_strength_known_hand(self):
        self.assertEqual(hand_strength('AA'), 1)
        self.assertEqual(hand_strength('AKs'), 4)
        self.assertEqual(hand_strength('22'), 52)

    def test_hand_strength_unknown_hand(self):
        self.assertEqual(hand_strength('XY'), 170)
        self.assertEqual(hand_strength('KQo'), 20)
        self.assertEqual(hand_strength('J9s'), 26)

    def test_hand_ranks_unique_values(self):
        values = list(hand_ranks.values())
        self.assertEqual(len(values), 169)
        self.assertEqual(len(set(values)), 169)

    def test_hand_ranks_key_value_relationship(self):
        sorted_ranks = sorted(hand_ranks.items(), key=lambda x: x[1])
        for i, (key, value) in enumerate(sorted_ranks):
            expected_value = i + 1
            self.assertEqual(value, expected_value)

class TestGroupPairs(unittest.TestCase):
    def test_pair(self):
        pair_list = ["22","33","44","77", "QQ","KK","AA"]
        grouped_pairs = group_pairs(pair_list)
        expected = ['QQ+', '77', '22-44']
        self.assertEqual(grouped_pairs,expected)

class TestGroupNonPairs(unittest.TestCase):
    def test_offsuit(self):
        non_pairs_list = ['95o', 'T3o', 'T4o', 'T7o', 'T8o', 'Q2o', 'Q3o', 'Q4o', 'Q7o', 'Q9o', 'QTo', 'QJo']
        grouped_non_pairs = group_non_pairs(non_pairs_list)
        expected = ['Q9o+', 'Q7o', 'Q2o-Q4o', 'T7o-T8o', 'T3o-T4o', '95o']
        self.assertEqual(grouped_non_pairs,expected)

    def test_suited(self):
        non_pairs_list = ['85s', '86s', '87s','98s', 'T7s', 'T8s', 'T9s']
        list1 = group_non_pairs(non_pairs_list)
        expected = ['T7s+', '98s', '85s+']
        self.assertEqual(list1,expected)

        non_pairs_list2 = ['85s', '86s', '87s']
        list2 = group_non_pairs(non_pairs_list2)
        expected2 = ['85s+']
        self.assertEqual(list2,expected2)

class TestGroupHands(unittest.TestCase):
    def test_various(self):
        hand_list = ["T5s","Q6s","Q7s","J7s","97o","87s","T4s","95s","86s","77","83s","74s","85s","94s","87o","84o","AKs","KK","KQs","QQ","JJ","AA","TT","99"]
        list1 = group_hands(hand_list)
        expected = ['99+', '77', 'AKs', 'KQs', 'Q6s-Q7s', 'J7s', 'T4s-T5s', '94s-95s', '85s+', '83s', '74s', '97o', '87o', '84o']
        self.assertEqual(list1,expected)

class TestUnGroupHands(unittest.TestCase):
    def test_various(self):
        hand_list = ['88+', 'A9s+', 'KTs-KQs', 'QTs-QJs', 'JTs', 'AQo+', 'KQo']
        list1 = ungroup_hands(hand_list)
        expected = ['88', '99', 'TT', 'JJ', 'QQ', 'KK', 'AA', 'A9s', 'ATs', 'AJs', 'AQs', 'AKs', 'KTs', 'KJs', 'KQs', 'QTs', 'QJs', 'JTs', 'AQo', 'AKo', 'KQo']
        self.assertEqual(list1, expected)