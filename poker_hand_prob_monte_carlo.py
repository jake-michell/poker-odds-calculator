import itertools
from texasholdem import Card, Deck
from texasholdem.evaluator import evaluate, rank_to_string
import random
from math import comb

# Generate a standard deck of 52 cards
def generate_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
    return [(rank, suit) for rank in ranks for suit in suits]

deck = Deck()

# Classify a poker hand
def classify_hand(hand):
    # Helper to count ranks
    ranks = [card[0] for card in hand]
    suits = [card[1] for card in hand]
    rank_counts = {rank: ranks.count(rank) for rank in ranks}
    
    # Check for specific hand types
    is_flush = len(set(suits)) == 1
    sorted_ranks = sorted([ranks.index(rank) for rank in ranks])  # Assume ranks are ordered
    is_straight = all(sorted_ranks[i] + 1 == sorted_ranks[i+1] for i in range(len(sorted_ranks) - 1))
    
    if is_flush and is_straight and ranks == ['10', 'Jack', 'Queen', 'King', 'Ace']:
        return "Royal Flush"
    elif is_flush and is_straight:
        return "Straight Flush"
    elif 4 in rank_counts.values():
        return "Four of a Kind"
    elif 3 in rank_counts.values() and 2 in rank_counts.values():
        return "Full House"
    elif is_flush:
        return "Flush"
    elif is_straight:
        return "Straight"
    elif 3 in rank_counts.values():
        return "Three of a Kind"
    elif list(rank_counts.values()).count(2) == 2:
        return "Two Pair"
    elif 2 in rank_counts.values():
        return "One Pair"
    else:
        return "High Card"



def calculate_hand_probabilities():
    total_combinations = comb(52, 5)
    
    # Probabilities
    probabilities = {
        "High Card": 1302540/ total_combinations,  # Calculated last
        "One Pair": 1098240/ total_combinations,
        "Two Pair": 123552 / total_combinations,
        "Three of a Kind": 54912/ total_combinations,
        "Straight": 10200 / total_combinations,
        "Flush": 5108 / total_combinations,
        "Full House": 3744 / total_combinations,
        "Four of a Kind": 624 / total_combinations,
        "Straight Flush": 36 / total_combinations,
        "Royal Flush": 4 / total_combinations,
    }
    
    # High Card is calculated as the remaining hands
    
    
    
    return probabilities


def monte_carlo_simulation(trials=1000000):
    deck = generate_deck()
    hand_counts = {
        "High card": 0, "Pair": 0, "Two Pair": 0, "Three of a Kind": 0,
        "Straight": 0, "Flush": 0, "Full House": 0, "Four of a Kind": 0,
        "Straight Flush": 0, "Royal Flush": 0,
    }

    for _ in range(trials):
        hand = random.sample(deck, 5)
        hand_rank = evaluate(hand)
        if hand_rank == 1:
            hand_type = "Royal Flush"
        else: hand_type = rank_to_string(hand_rank)
        hand_counts[hand_type] += 1

    return {hand: count / trials for hand, count in hand_counts.items()}

# Compare theoretical and empirical probabilities
def compare_results():
    theoretical = calculate_hand_probabilities()
    empirical = monte_carlo_simulation()
    print("Theoretical Probabilities:")
    for hand, prob in theoretical.items():
        print(f"{hand}: {prob:.6f}")
    print("\nEmpirical Probabilities:")
    for hand, prob in empirical.items():
        print(f"{hand}: {prob:.6f}")

compare_results()