import time
from dataclasses import dataclass
from collections import defaultdict
from copy import deepcopy

day = 19

@dataclass
class BluePrint():
    id: int
    ore: dict
    clay: dict
    obsidian: dict
    geode: dict

    def canCreateOre(self, ores):
        for ore in self.ore:
            if ores[ore] < self.ore[ore]:
                return False
        return True
    
    def canCreateClay(self, ores):
        for ore in self.clay:
            if ores[ore] < self.clay[ore]:
                return False
        return True
    
    def canCreateObsidian(self, ores):
        for ore in self.obsidian:
            if ores[ore] < self.obsidian[ore]:
                return False
        return True

    def canCreateGeode(self, ores):
        for ore in self.geode:
            if ores[ore] < self.geode[ore]:
                return False
        return True

def getNewStates(bp, new_robots, new_ore_dict, canBuy, robots, ores):
    for new_state in new_robots:
        new_robot_dict = {}
        new_ores = deepcopy(new_ore_dict)
        newCanBuy = deepcopy(canBuy)
        # Update canBuy
        if sum(new_state.values()) == 0:
            if bp.canCreateOre(ores):
                newCanBuy['ore'] = False
            if bp.canCreateClay(ores):
                newCanBuy['clay'] = False
            if bp.canCreateObsidian(ores):
                newCanBuy['obsidian'] = False
        else:
            newCanBuy = {'ore': True, 'clay': True, 'obsidian': True}
        # Update robot count and ore count
        for robot in robots:
            new_robot_dict[robot] = robots[robot] + new_state[robot]
            if new_state[robot]:
                for ore in getattr(bp, robot):
                    new_ores[ore] -= getattr(bp, robot)[ore]
        yield (new_robot_dict, new_ores, newCanBuy)

def getNewRobots(bp: BluePrint, canBuy, maxRobots, robots, ores):
    new_robots = []
    if (bp.canCreateOre(ores) or bp.canCreateClay(ores)
            or bp.canCreateObsidian(ores) or bp.canCreateGeode(ores)):
        if bp.canCreateGeode(ores):
            new_robots.append(defaultdict(lambda: 0, {'geode': 1}))
        else:
            if canBuy['obsidian'] and robots['obsidian'] < maxRobots['obsidian'] and bp.canCreateObsidian(ores):
                new_robots.append(defaultdict(lambda: 0, {'obsidian': 1}))
            if canBuy['clay'] and robots['clay'] < maxRobots['clay'] and bp.canCreateClay(ores):
                new_robots.append(defaultdict(lambda: 0, {'clay': 1}))
            if canBuy['ore'] and robots['ore'] < maxRobots['ore'] and bp.canCreateOre(ores):
                new_robots.append(defaultdict(lambda: 0, {'ore': 1}))
    if not bp.canCreateGeode(ores):
        new_robots.append(defaultdict(lambda: 0))
    return new_robots

def part_1(data: "list[BluePrint]"):
    score = 0
    for bp in data:
        t = 1
        robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
        ores = defaultdict(lambda: 0, {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0})
        canBuy = {'ore': True, 'clay': True, 'obsidian': True}
        maxRobots = {ore: max((bp.ore[ore], bp.clay[ore], bp.obsidian[ore], bp.geode[ore])) for ore in robots}
        candidates = [(t, robots, ores, canBuy)]
        state_scores = defaultdict(dict)
        max_score = defaultdict(lambda: 0)
        while candidates:
            # Get values
            candidates.sort(key=lambda x: (x[0], x[1]['geode'], x[1]['obsidian'], x[1]['clay'], x[1]['ore']), reverse=True)
            c = candidates.pop(0)
            t = c[0]
            robots = c[1]
            ores = c[2]
            canBuy = c[3]
            # Get potential purchases
            new_robots = getNewRobots(bp, canBuy, maxRobots, robots, ores)
    
            # Generate materials
            new_ore_dict = defaultdict(lambda: 0)
            for robot in robots:
                new_ore_dict[robot] = ores[robot] + 1*robots[robot]

            max_score[t] = max(max_score[t], new_ore_dict['geode'])
            if t+1 > 24: continue

            # Generate new states
            for new_robot_dict, new_ores, newCanBuy in getNewStates(bp, new_robots, new_ore_dict, canBuy, robots, ores):
                state_key = tuple(new_robot_dict.values())
                if state_key in state_scores[t]:
                    ok = False
                    for key in state_scores[t][state_key]:
                        if state_scores[t][state_key][key] < new_ores[key]:
                            ok = True
                            break
                    if not ok:
                        continue
                state_scores[t][state_key] = new_ores
                candidates.append((t+1, new_robot_dict, new_ores, newCanBuy))
        score += max_score[24]*bp.id
    return score


def part_2(data: "list[BluePrint]"):
    score = 1
    for bp in data[:3]:
        t = 1
        robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
        ores = defaultdict(lambda: 0, {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0})
        canBuy = {'ore': True, 'clay': True, 'obsidian': True}
        maxRobots = {ore: max((bp.ore[ore], bp.clay[ore], bp.obsidian[ore], bp.geode[ore])) for ore in robots}
        candidates = [(t, robots, ores, canBuy)]
        state_scores = defaultdict(dict)
        max_score = defaultdict(lambda: 0)
        while candidates:
            # Get values
            candidates.sort(key=lambda x: (x[0], x[1]['geode'], x[1]['obsidian'], x[1]['clay'], x[1]['ore']), reverse=True)
            c = candidates.pop(0)
            t = c[0]
            robots = c[1]
            ores = c[2]
            canBuy = c[3]

            # Get potential purchases
            new_robots = getNewRobots(bp, canBuy, maxRobots, robots, ores)
    
            # Generate materials
            new_ore_dict = defaultdict(lambda: 0)
            for robot in robots:
                new_ore_dict[robot] = ores[robot] + 1*robots[robot]

            max_score[t] = max(max_score[t], new_ore_dict['geode'])

            if t+1 > 32: continue

            # Generate new states
            for new_robot_dict, new_ores, newCanBuy in getNewStates(bp, new_robots, new_ore_dict, canBuy, robots, ores):
                # Check state
                state_key = tuple(new_robot_dict.values())
                if state_key in state_scores[t]:
                    ok = False
                    for key in state_scores[t][state_key]:
                        if state_scores[t][state_key][key] < new_ores[key]:
                            ok = True
                            break
                    if not ok:
                        continue
                state_scores[t][state_key] = new_ores
                candidates.append((t+1, new_robot_dict, new_ores, newCanBuy))
        score *= max_score[32]
    return score

def parse_data():
    data = []
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            id, info = line.strip().split(':')
            id = int(id)
            robots = info.strip().split('.')
            res = defaultdict(None)
            for robot in robots:
                resources_res = defaultdict(lambda: 0)
                type, resources = robot.strip().split(maxsplit=1)
                resources = resources.split(',')
                for resource in resources:
                    amount, t = resource.strip().split()
                    resources_res[t] = int(amount)
                res[type] = resources_res
            data.append(BluePrint(id, res['ore'], res['clay'], res['obsidian'], res['geode']))


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