from deck_of_cards import Board, Player, Card
from poker_calculator import simulate_win_tie_loss

import cProfile
import pstats
import time

def main():
    with cProfile.Profile() as profile:
        board = Board([Card("J", "Spade"), Card("4", "Club"), Card("2", "Diamond")])
        players = [
            Player("Player 1", [Card("A", "Spade"), Card("K", "Heart")]),
            Player("Player 2", [Card("Q", "Diamond"), Card("J", "Club")])
        ]

        simulate_win_tie_loss(board, players, n=10000)

    time.sleep(1)  # Delay after running the code

    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.TIME)
    results.print_stats()


if __name__ == "__main__":
    main()


