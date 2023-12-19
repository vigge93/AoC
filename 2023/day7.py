import time
from enum import IntEnum
from functools import reduce

day = 7


class Hands(IntEnum):
    HIGH_CARD = (1,)
    ONE_PAIR = (2,)
    TWO_PAIR = (3,)
    THREE_KIND = (4,)
    FULL_HOUSE = (5,)
    FOUR_KIND = (6,)
    FIVE_KIND = 7


card_num_map = {"A": 14, "K": 13, "Q": 12, "T": 10, "J": 1}


def part_1(data):
    transformed = []
    for hand, bid in data:
        converted_hand = []
        for card in hand:
            if card.isnumeric():
                converted_hand.append(int(card))
            else:
                converted_hand.append(card_num_map[card])
        unq_cards = set(converted_hand)
        hand_counts = {}
        for card in unq_cards:
            hand_counts[card] = converted_hand.count(card)
        if any(map(lambda card: card == 5, hand_counts.values())):
            transformed.append((Hands.FIVE_KIND, converted_hand, bid))
        elif any(map(lambda card: card == 4, hand_counts.values())):
            transformed.append((Hands.FOUR_KIND, converted_hand, bid))
        elif any(map(lambda card: card == 3, hand_counts.values())):
            if any(map(lambda card: card == 2, hand_counts.values())):
                transformed.append((Hands.FULL_HOUSE, converted_hand, bid))
            else:
                transformed.append((Hands.THREE_KIND, converted_hand, bid))
        elif any(map(lambda card: card == 2, hand_counts.values())):
            if sum(map(lambda card: card == 2, hand_counts.values())) == 2:
                transformed.append((Hands.TWO_PAIR, converted_hand, bid))
            else:
                transformed.append((Hands.ONE_PAIR, converted_hand, bid))
        else:
            transformed.append((Hands.HIGH_CARD, converted_hand, bid))
    transformed.sort()
    return reduce(
        lambda prev, next: prev + (next[0] + 1) * next[1][2], enumerate(transformed), 0
    )


def part_2(data):
    transformed = []
    for hand, bid in data:
        converted_hand = []
        for card in hand:
            if card.isnumeric():
                converted_hand.append(int(card))
            else:
                converted_hand.append(card_num_map[card])
        unq_cards = set(converted_hand)
        hand_counts = {}
        jokers = 0
        for card in unq_cards:
            hand_counts[card] = converted_hand.count(card)
        if 1 in hand_counts and len(unq_cards) > 1:
            jokers = hand_counts[1]
            del hand_counts[1]
        hand_values = list(hand_counts.values())
        if any(map(lambda card: card + jokers == 5, hand_values)):
            transformed.append((Hands.FIVE_KIND, converted_hand, bid))
        elif any(map(lambda card: card + jokers == 4, hand_values)):
            transformed.append((Hands.FOUR_KIND, converted_hand, bid))
        elif any(
            mapped_hand := list(map(lambda card: card + jokers == 3, hand_values))
        ):
            hand_values[mapped_hand.index(True)] += jokers
            if any(map(lambda card: card == 2, hand_values)):
                transformed.append((Hands.FULL_HOUSE, converted_hand, bid))
            else:
                transformed.append((Hands.THREE_KIND, converted_hand, bid))
        elif any(
            mapped_hand := list(map(lambda card: card + jokers == 2, hand_values))
        ):
            hand_values[mapped_hand.index(True)] += jokers
            if sum(map(lambda card: card == 2, hand_values)) == 2:
                transformed.append((Hands.TWO_PAIR, converted_hand, bid))
            else:
                transformed.append((Hands.ONE_PAIR, converted_hand, bid))
        else:
            transformed.append((Hands.HIGH_CARD, converted_hand, bid))
    transformed.sort()
    return reduce(
        lambda prev, next: prev + (next[0] + 1) * next[1][2], enumerate(transformed), 0
    )


def parse_data():
    data = []
    with open(f"day{day}.txt", "r") as f:
        for line in f:
            hand, bid = line.strip().split()
            data.append((hand, int(bid)))
    return data


if __name__ == "__main__":
    start_time = time.perf_counter_ns()
    data = parse_data()
    data_time = time.perf_counter_ns()
    p1 = part_1(data)
    p1_time = time.perf_counter_ns()
    p2 = part_2(data)
    end_time = time.perf_counter_ns()
    print(
        f"""=== Day {day:02} ===\n"""
        f"""  · Loading data\n"""
        f"""  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n"""
        f"""  · Part 1: {p1}\n"""
        f"""  · Elapsed: {(p1_time - data_time)/10**6:.3f} ms\n\n"""
        f"""  · Part 2: {p2}\n"""
        f"""  · Elapsed: {(end_time - p1_time)/10**6:.3f} ms\n\n"""
        f"""  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms"""
    )
