from typing import Dict, List, Tuple
from collections import defaultdict
from deck_of_cards import Card, Player, Deck, Board, deal_cards, deal_flop
from evaluate_poker_hand import evaluate_five_card_hand, evaluate_two_card_hand
import concurrent.futures

def simulate_win_tie_loss(board: Board, players: List[Player], n: int = 10000) -> Dict[str, Tuple[float, float, float]]:
    """Poker calculator to calculate Win Tie Loss of each player based on the board using Monte Carlo Method

    Args:
        board (Board): Board that is 0, 3 , 4, 5 cards
        players (List[Player]): List of players
        n (int): number of simulations to be ran, default is 10,000

    Returns:
        Dict[str, Tuple[float, float, float]]: Return a dicionary with Player.name and Tuple of Win Tie Loss Percentage
    """
    win_tie_loss = {player.name: (0.0, 0.0, 0.0) for player in players}
    deck = Deck()
    for player in players:
            if len(player.hand) == 2:
                deck.remove_cards(player.hand)

    deck.remove_cards(board.board)

    def simulate_single_game():
    # for _ in range(n):
        remaining_cards = deck.copy()
        simulation_board = Board(board.board[:])
        for player in players:
            if len(player.hand) == 0:
                for _ in range(2):
                    player.draw(remaining_cards)
        
        remaining_cards.shuffle()

        # Evaluate hand strength at preflop
        # hand_ranks = evaluate_hand_ranks(simulation_board, players)
        # preflop_results = compare_hand_ranks(hand_ranks)
        # update_win_tie_loss(win_tie_loss, preflop_results)

        # Deal the flop
        if len(simulation_board.board) == 0:
            flop = deal_flop(remaining_cards)
            simulation_board.add_card_list(flop)

        # Evaluate hand strength at flop
        # hand_ranks = evaluate_hand_ranks(simulation_board, players)
        # flop_results = compare_hand_ranks(hand_ranks)
        # update_win_tie_loss(win_tie_loss, flop_results)

        # Deal the turn
        if len(simulation_board.board) == 3:
            turn = deal_cards(1, remaining_cards)
            simulation_board.add_card_list(turn)

        # Evaluate hand strength at turn
        # hand_ranks = evaluate_hand_ranks(simulation_board, players)
        # turn_results = compare_hand_ranks(hand_ranks)
        # update_win_tie_loss(win_tie_loss, turn_results)

        # Deal the river
        if len(simulation_board.board) == 4:
            river = deal_cards(1, remaining_cards)
            simulation_board.add_card_list(river)

        # Evaluate hand strength at river
        hand_ranks = evaluate_hand_ranks(simulation_board, players)
        river_results = compare_hand_ranks(hand_ranks)

        return river_results
        # update_win_tie_loss(win_tie_loss, river_results)

        # print(river_results)
        # print(simulation_board.display())
        # print(win_tie_loss)

    # Number of threads to use
    num_threads = 4

    # Create a ThreadPoolExecutor with the desired number of threads
    executor = concurrent.futures.ThreadPoolExecutor(num_threads)

    # Submit the simulations to the executor
    futures = [executor.submit(simulate_single_game) for _ in range(n)]

    # Wait for all simulations to complete
    concurrent.futures.wait(futures)

    # Process the results
    for future in futures:
        result = future.result()
        update_win_tie_loss(win_tie_loss, result)

    # Calculate percentages
    total_simulations = n
    for player in win_tie_loss:
        win_percentage = round(win_tie_loss[player][0] / total_simulations * 100, 2)
        tie_percentage = round(win_tie_loss[player][1] / total_simulations * 100, 2)
        loss_percentage = round(win_tie_loss[player][2] / total_simulations * 100, 2)
        win_tie_loss[player] = (win_percentage, tie_percentage, loss_percentage)

    print(win_tie_loss)
    return win_tie_loss

def evaluate_hand_ranks(board: Board, players: List[Player]) -> Dict[Player, Tuple[int, List[int]]]:
    """Evaluate hand rank of each player giving them a rank 0-9

    Args:
        board (Board): _description_
        players (List[Player]): List of Players

    Returns:
        Dict[Player, Tuple[int, List[int]]]: _return a Dictionary where each player 
        is assigned to their Hand strength 0-9 and List of kickers
    """
    hand_ranks = {}

    for player in players:
        # Evaluate only player's hole cards
        if board is None or not board.board:
            rank, kickers = evaluate_two_card_hand(player.hand)
        # Evaluate based off the board and hole cards
        else:
            all_cards = player.hand + board.board
            rank, kickers = evaluate_five_card_hand(all_cards)

        hand_ranks[player] = (rank, kickers)

    return hand_ranks

def compare_single_hand_rank(hand1: Tuple[int, List[int]], hand2: Tuple[int, List[int]]) -> int:
    """Compare two hands to see which hand is stronger

    Args:
        hand1 (Tuple[int, List[int]]): Player1 hand strength 0-9, List of kickers
        hand2 (Tuple[int, List[int]]): Player2 hand strength 0-9, List of kickers

    Returns:
        int: 1 - Hand1 stronger
        -1 - Hand2 Stronger
        0 - Tied
    """
    rank1, kickers1 = hand1
    rank2, kickers2 = hand2

    # Compare hand ranks
    if rank1 > rank2:
        return 1
    elif rank1 < rank2:
        return -1

    # Compare kickers if hand ranks are the same
    for kicker1, kicker2 in zip(kickers1, kickers2):
        if kicker1 > kicker2:
            return 1
        elif kicker1 < kicker2:
            return -1
    return 0  # Tie

def compare_hand_ranks(players: Dict[Player, Tuple[int, List[int]]]) -> Dict[Player, str]:
    """Compare hand ranks 0-9 and kickers to see who wins or loses off the given board

    Args:
        players (List[Tuple[Player, List[int]]]): dictionary with Players and 
        their Hand strength 0-9 and List of kickers

    Returns:
        Dict[Player, str]: dictionary with each Player a winner or loser of the board
    """
    results = {player: "Tie" for player in players}

    player_list = list(players.keys())
    num_players = len(player_list)

    for i in range(num_players):
        for j in range(i + 1, num_players):
            hand1 = players[player_list[i]]
            hand2 = players[player_list[j]]

            result = compare_single_hand_rank(hand1, hand2)
            if result > 0:
                if not results[player_list[i]] == "Loss":
                    results[player_list[i]] = "Win"
                results[player_list[j]] = "Loss"
            elif result < 0:
                if not results[player_list[j]] == "Loss":
                    results[player_list[j]] = "Win"
                results[player_list[i]] = "Loss"
    return results

def update_win_tie_loss(win_tie_loss: Dict[str, Tuple[float, float, float]], results: Dict[Player, str]) -> None:
    """Update the win/tie/loss counts for each player based on the simulation results.

    Args:
        win_tie_loss (Dict[str, Tuple[float, float, float]]): Dictionary containing win/tie/loss counts for each player.
        results (Dict[Player, str]): Dictionary containing the simulation results for each player.

    Returns:
        None
    """
    for player, result in results.items():
        if result == "Win":
            win_tie_loss[player.name] = (
                win_tie_loss[player.name][0] + 1,
                win_tie_loss[player.name][1],
                win_tie_loss[player.name][2]
            )
        elif result == "Tie":
            win_tie_loss[player.name] = (
                win_tie_loss[player.name][0],
                win_tie_loss[player.name][1] + 1,
                win_tie_loss[player.name][2]
            )
        else:  # result == "Loss"
            win_tie_loss[player.name] = (
                win_tie_loss[player.name][0],
                win_tie_loss[player.name][1],
                win_tie_loss[player.name][2] + 1
            )
