from copy import deepcopy

key = ['A', 'B', 'C', 'D']
rooms = [['D', 'D', 'D', 'D'], ['A', 'B', 'C', 'C'], ['A', 'A', 'B', 'B'], ['B', 'C', 'A', 'C']]
rooms_key = [['A', 'A', 'A', 'A'], ['B', 'B', 'B', 'B'], ['C', 'C', 'C', 'C'], ['D', 'D', 'D', 'D']]
hallway = ['', '', '', '', '', '' ,'', '', '', '' ,'']
hallway = ['', '', '', '', '', '' ,'', '', '', '' ,'']
energies = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
entries = {'A': 2, 'B':4, 'C': 6, 'D': 8}
spaces = 4


def sort_fish(rooms, hallway, prev_min_energy, d):
    if d <= 3:
        print(rooms, hallway)
    if rooms == rooms_key:
        return 0
    energy = 0
    found = True
    rooms_not_correct = set()
    while found:
        found = False
        for idx, room in enumerate(rooms):
            correct = True
            full = False
            if len(room) == spaces:
                full = True
            for amphipod in room:
                if not amphipod == key[idx]:
                    correct = False
                    break
            if correct and not full:
                for spc, amphipod in enumerate(hallway):
                    if amphipod == key[idx]:
                        empty = True
                        for nspc in range(min(entries[amphipod], spc)+1, max(entries[amphipod], spc)):
                            if hallway[nspc] != '':
                                empty = False
                                break
                        if empty:
                            found = True
                            energy += (abs(entries[amphipod] - spc) + (spaces - len(room)))*energies[amphipod]
                            hallway[spc] = ''
                            room.append(amphipod)
            elif not correct:
                rooms_not_correct.add(idx)
    min_energy = -1
    for idx, room in enumerate(rooms):
        if not (room and idx in rooms_not_correct):
            continue
        amphipod = room[-1]
        for hidx in range(entries[key[idx]] + 1, len(hallway)):
            if hallway[hidx] != '':
                break
            if hidx in entries.values():
                continue
            new_energy = energy
            new_energy += (abs(entries[key[idx]] - hidx) + spaces - len(room) + 1)*energies[amphipod]
            if new_energy >= prev_min_energy and prev_min_energy != -1:
                continue
            new_rooms = deepcopy(rooms)
            new_hallway = deepcopy(hallway)
            new_hallway[hidx] = amphipod
            del new_rooms[idx][-1]
            new_energy += sort_fish(new_rooms, new_hallway, min_energy if min_energy != -1 else prev_min_energy, d+1)
            if new_energy < min_energy or min_energy == -1:
                min_energy = new_energy
        for hidx in range(entries[key[idx]] - 1, -1, -1):
            if hallway[hidx] != '':
                break
            if hidx in entries.values():
                continue
            new_energy = energy
            new_energy += (abs(entries[key[idx]] - hidx) + spaces - len(room) + 1)*energies[amphipod]
            if new_energy >= prev_min_energy and prev_min_energy != -1:
                continue
            new_rooms = deepcopy(rooms)
            new_hallway = deepcopy(hallway)
            new_hallway[hidx] = amphipod
            del new_rooms[idx][-1]
            new_energy += sort_fish(new_rooms, new_hallway, min_energy if min_energy != -1 else prev_min_energy, d+1)
            if new_energy < min_energy or min_energy == -1:
                min_energy = new_energy
    if min_energy == -1 and rooms != rooms_key:
        return 10**7
    elif min_energy == -1:
        return energy
    else:
        return min_energy

# rooms = [['A'], ['B'], ['D'], ['D', 'C']]
# hallway = ['A', 'B', '', '', '', '' ,'', '', '', '' ,'C']        
print(sort_fish(rooms, hallway, -1, 1))