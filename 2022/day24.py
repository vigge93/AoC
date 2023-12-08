import time
from dataclasses import dataclass

day = 24

def get_next_pos(blizz: "Blizzard", wall) -> "Blizzard":
    minX = min(wall, key=lambda x: x[0])[0]
    maxX = max(wall, key=lambda x: x[0])[0]
    minY = min(wall, key=lambda x: x[1])[1]
    maxY = max(wall, key=lambda x: x[1])[1]
    if blizz.dir == 0:
        if blizz.x + 1 == maxX:
            return Blizzard(minX + 1, blizz.y, blizz.dir)
        else:
            return Blizzard(blizz.x + 1, blizz.y, blizz.dir)
    elif blizz.dir == 1:
        if blizz.y + 1 == maxY:
            return Blizzard(blizz.x, minY + 1, blizz.dir)
        else:
            return Blizzard(blizz.x, blizz.y + 1, blizz.dir)
    elif blizz.dir == 2:
        if blizz.x - 1 == minX:
            return Blizzard(maxX - 1, blizz.y, blizz.dir)
        else:
            return Blizzard(blizz.x - 1, blizz.y, blizz.dir)
    elif blizz.dir == 3:
        if blizz.y - 1 == minY:
            return Blizzard(blizz.x, maxY - 1, blizz.dir)
        else:
            return Blizzard(blizz.x, blizz.y - 1, blizz.dir)

@dataclass
class Blizzard:
    x: int
    y: int
    dir: int

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]

    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __repr__(self) -> str:
        return f'<Blizzard x: {self.x}, y: {self.y}, dir: {self.dir}>'

@dataclass
class State:
    player: "tuple[int]"
    blizzards: "list[Blizzard]"
    time: int

    def __eq__(self, other):
        return self.player == other.player and self.time == other.time
    
    def __hash__(self) -> int:
        return hash((self.player, self.time))

    def __repr__(self) -> str:
        return f"<State time: {self.time}, player: {self.player}>"

def part_1(data):
    player = (1, 0)
    start = (1, 0)
    wall = data['wall']
    blizzards = data['blizzard']
    minX = min(wall, key=lambda x: x[0])[0]
    maxX = max(wall, key=lambda x: x[0])[0]
    minY = min(wall, key=lambda x: x[1])[1]
    maxY = max(wall, key=lambda x: x[1])[1]
    goal = (maxX-1, maxY)
    best_time = 0
    states: "list[State]" = []
    states.append(State(player, blizzards, 0))
    visited = {State(player, blizzards, 0)}
    blizzard_states = {}
    while states:
        state = states.pop(0)
        blizzards = state.blizzards
        player = state.player
        t = state.time

        if player == goal:
            best_time = t
            break

        new_blizzards = []
        if t in blizzard_states:
            new_blizzards = blizzard_states[t]
        else:
            for blizz in blizzards:
                new_blizzards.append(get_next_pos(blizz, wall))
            blizzard_states[t] = new_blizzards
        blizzards = new_blizzards
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x*y != 0: # No diagonals
                    continue
                new_player_pos = (player[0] + x, player[1] + y)
                if new_player_pos in blizzards:
                    continue
                if not (minX < new_player_pos[0] < maxX) or not (minY < new_player_pos[1] < maxY):
                    if new_player_pos != goal:
                        continue
                new_state = State(new_player_pos, blizzards, t+1)
                if new_state not in visited:
                    states.append(new_state)
                    visited.add(new_state)
        if player  == start and t < 200:
            states.append(State(player, blizzards, t+1))
    return best_time

def part_2(data):
    player = (1, 0)
    start = (1, 0)
    wall = data['wall']
    blizzards = data['blizzard']
    minX = min(wall, key=lambda x: x[0])[0]
    maxX = max(wall, key=lambda x: x[0])[0]
    minY = min(wall, key=lambda x: x[1])[1]
    maxY = max(wall, key=lambda x: x[1])[1]
    goal = (maxX-1, maxY)
    steps = [(start, goal), (goal, start), (start, goal)]
    step = 0
    best_time = 0
    states: "list[State]" = []
    states.append(State(player, blizzards, 0))
    visited = {State(player, blizzards, 0)}
    blizzard_states = {}
    while states:
        state = states.pop(0)
        blizzards = state.blizzards
        player = state.player
        t = state.time

        if player == goal:
            step += 1
            if step < len(steps):
                start, goal = steps[step]
                states = [State(player, blizzards, t)]
                continue
            else:
                best_time = t
                break

        new_blizzards = []
        if t in blizzard_states:
            new_blizzards = blizzard_states[t]
        else:
            for blizz in blizzards:
                new_blizzards.append(get_next_pos(blizz, wall))
            blizzard_states[t] = new_blizzards
        blizzards = new_blizzards
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x*y != 0: # No diagonals
                    continue
                new_player_pos = (player[0] + x, player[1] + y)
                if new_player_pos in blizzards:
                    continue
                if not (minX < new_player_pos[0] < maxX) or not (minY < new_player_pos[1] < maxY):
                    if new_player_pos != goal:
                        continue
                new_state = State(new_player_pos, blizzards, t+1)
                if new_state not in visited:
                    states.append(new_state)
                    visited.add(new_state)
        if player  == start:
            states.append(State(player, blizzards, t+1))
    return best_time


def parse_data():
    data = {'wall': [], 'blizzard': []}
    with open(f'day{day}.txt', 'r') as f:
        for y, line in enumerate(f):
            for x, cell in enumerate(line.strip()):
                if cell == '#':
                    data['wall'].append((x, y))
                elif cell == '>':
                    data['blizzard'].append(Blizzard(x, y, 0))
                elif cell == 'v':
                    data['blizzard'].append(Blizzard(x, y, 1))
                elif cell == '<':
                    data['blizzard'].append(Blizzard(x, y, 2))
                elif cell == '^':
                    data['blizzard'].append(Blizzard(x, y, 3))
    return data

if __name__ == '__main__':
    start_time = time.perf_counter_ns()
    data = parse_data()
    p1 = part_1(data)
    p2 = part_2(data)
    end_time = time.perf_counter_ns()
    print(f'=== Day {day:02} ===')
    print(f'  · Part 1: {p1}')
    print(f'  · Part 2: {p2}')
    print(f"  · Elapsed: {(end_time - start_time)/10**6:.3f} ms")