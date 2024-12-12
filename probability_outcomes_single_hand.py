from texasholdem import Card, Deck
from texasholdem.evaluator import evaluate, rank_to_string
import itertools
from collections import Counter

# Define all possible hand ranks in poker
hand_ranks = [
    "High card", "Pair", "Two Pair", "Three of a Kind", "Straight",
    "Flush", "Full House", "Four of a Kind", "Straight Flush"
]

# Create a deck
my_deck = Deck()

# Define specific hole cards (Ace of Spades and Ace of Diamonds)
my_hand = [Card("Ks"), Card("Kd")]

# Remove these cards from the deck to ensure they're not in the remaining cards
my_deck.cards = [card for card in my_deck.cards if card not in my_hand]

# Extract the remaining cards from the deck
remaining_cards = my_deck.cards
print(remaining_cards)
# Generate all combinations of 5 community cards
community_combinations = itertools.combinations(remaining_cards, 5)
print(community_combinations)
# Create a counter to store the frequency of each outcome
outcome_counter = Counter()

# Evaluate all combinations
total_combinations = 0
list_hand_scores = []
for community_cards in community_combinations:
    # Evaluate the hand
    hand_score = evaluate(cards=my_hand, board=list(community_cards))
    outcome = rank_to_string(hand_score)
    # Update the counter
    list_hand_scores.append(hand_score)
    outcome_counter[outcome] += 1
    total_combinations += 1

# Display results
print(f"Total combinations evaluated: {total_combinations}")
print("Outcome counts:")
for rank in hand_ranks:
    count = outcome_counter.get(rank, 0)
    print(f"{rank}: {count}")

# Optional: Save results to a file
with open("outcome_counts.txt", "w") as file:
    file.write(f"Total combinations evaluated: {total_combinations}\n")
    file.write("Outcome counts:\n")
    for rank in hand_ranks:
        count = outcome_counter.get(rank, 0)
        file.write(f"{rank}: {count}\n")
print(list_hand_scores)
