import time

day = 4

def part_1(data):
    data = data['cards']
    s = 0
    for winning, given in data.values():
        overlap = winning & given
        if overlap:
            s += 2**(len(overlap)-1)
    return s

def part_2(data):
    cards = data['cards']
    for card in cards:
        winning, given = cards[card]
        cards[card] = len(winning & given)
    owned = data['owned_cards']
    for card in sorted(owned.keys()):
        overlap = cards[card]
        for i in range(card + 1, card + overlap + 1):
            if i in cards:
                owned[i] += owned[card]
    return sum(owned.values())

def parse_data():
    data = {
        'cards': {},
        'owned_cards': {}
    }
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            line = line.strip()
            card_num, cards = line.split(':')
            card_num = int(card_num.split(' ')[-1].strip())
            winning, given = cards.split('|')
            winning_nums = []
            given_nums = []
            for winning_num in winning.split():
                if not winning_num.strip():
                    continue
                winning_nums.append(int(winning_num.strip()))
            for given_num in given.split():
                if not given_num.strip():
                    continue
                given_nums.append(int(given_num.strip()))
            data['cards'][card_num] = (set(winning_nums), set(given_nums))
            data['owned_cards'][card_num] = 1
    return data

if __name__ == '__main__':
    start_time = time.perf_counter_ns()
    data = parse_data()
    data_time = time.perf_counter_ns()
    p1 = part_1(data)
    p1_time = time.perf_counter_ns()
    p2 = part_2(data)
    end_time = time.perf_counter_ns()
    print(f'''=== Day {day:02} ===\n'''
    f'''  · Loading data\n'''
    f'''  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n'''
    f'''  · Part 1: {p1}\n'''
    f'''  · Elapsed: {(p1_time - data_time)/10**6:.3f} ms\n\n'''
    f'''  · Part 2: {p2}\n'''
    f'''  · Elapsed: {(end_time - p1_time)/10**6:.3f} ms\n\n'''
    f'''  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms''')