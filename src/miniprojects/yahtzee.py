"""
Planner for Yahtzee game
Simplifications:  only allow discard and roll, only score against upper level

@author: Dmitry Marcautsan
"""

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def gen_all_permutations(outcomes, length):
    """
    Iterative function that enumerates the set of all permutations of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            round_outcomes = list(outcomes)
            for item in partial_sequence:
                round_outcomes.remove(item)
            for item in round_outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    aggregator = {}
    for card in hand:
        card_key = str(card)
        if card_key in aggregator:
            aggregator[card_key] = aggregator[card_key] + card
        else:
            aggregator[card_key] = card
    return max([agg_score for _, agg_score in aggregator.items()])


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    permutations = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)
    return sum([score(list(held_dice)+ list(perm)) for perm in permutations]) / float(len(permutations))


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    combinations = set([()])
    for num_dice in range(1, len(hand) + 1):
        step_combinations = set([tuple(sorted(perm)) for perm in gen_all_permutations(hand, num_dice)])
        combinations = combinations.union(step_combinations)
    return combinations


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    value_and_hold = [(expected_value(hold, num_die_sides, len(hand) - len(hold)), hold) for hold in all_holds]
    return sorted(value_and_hold, key=lambda entry: entry[0])[-1]


