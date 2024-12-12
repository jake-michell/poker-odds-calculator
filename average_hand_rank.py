from texasholdem import Card, Deck
from texasholdem.evaluator import evaluate, rank_to_string
import numpy as np
import itertools
from collections import Counter
import csv
from tqdm import tqdm  # For the progress bar

def generate_hole_cards():
    ranks = "AKQJT98765432"
    suited = [(f"{r1}s", f"{r2}s") for r1 in ranks for r2 in ranks if r1 > r2]  # Suited hands s (spaids) s(spaids)
    offsuit = [(f"{r1}s", f"{r2}d") for r1 in ranks for r2 in ranks if r1 > r2]  # Off-suited hands, s (spades) d (diamonds)
    pairs = [(f"{r}s", f"{r}d") for r in ranks]  # Pairs
    return pairs + suited + offsuit

# Generate all distinct hole cards
distinct_hands = generate_hole_cards()

output_file = "poker_hand_scores.csv"
fieldnames = ["Hand", "Suited", "Mean", "Standard Deviation", "Median", "IQR"]

# Open CSV for writing
with open(output_file, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Simulate for each hand with progress bar
    for hole_cards in tqdm(distinct_hands, desc="Evaluating Hands", unit="hand"):
        # Determine if suited or not
        suited = hole_cards[0][-1] == hole_cards[1][-1]
        is_suited = "Suited" if suited else "Off-suited"
        hand_name = f"{hole_cards[0][0]}{hole_cards[1][0]}"

        # Create deck and remove hole cards
        my_deck = Deck()
        my_hand = [Card(hole_cards[0]), Card(hole_cards[1])]
        my_deck.cards = [card for card in my_deck.cards if card not in my_hand]

        # Generate all combinations of 5 community cards
        remaining_cards = my_deck.cards
        community_combinations = itertools.combinations(remaining_cards, 5)
        # list of all the hand scores
        list_hand_score = []
        # Evaluate all combinations
        total_combinations = 0
        for community_cards in community_combinations:
            hand_score = evaluate(cards=my_hand, board=list(community_cards))
            list_hand_score.append(hand_score)
            total_combinations += 1

        # Calculate average hand rank for all hands
        mean = np.mean(list_hand_score)
        std_dev = np.std(list_hand_score, ddof=1)
        median = np.median(list_hand_score)
        q1 = np.percentile(list_hand_score, 25)
        q3 = np.percentile(list_hand_score, 75)
        iqr = q3 - q1
        
        # Write results to CSV
        row = {
            "Hand": hand_name,
            "Suited": is_suited,
            "Mean": mean,
            "Standard Deviation": std_dev,
            "Median": median,
            "IQR": iqr
        }
        writer.writerow(row)

print(f"Simulation completed. Results saved to {output_file}.")
