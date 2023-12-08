import itertools
import time
import numpy as np
        
scanners = []

rotations = ((
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
    ),
    (
        (1, 0, 0),
        (0, 0, -1),
        (0, 1, 0)
    ),
    (
        (1, 0, 0),
        (0, -1, 0),
        (0, 0, -1)
    ),
    (
        (1, 0, 0),
        (0, 0, 1),
        (0, -1, 0)
    ),
    (
        (0, -1, 0),
        (1, 0, 0),
        (0, 0, 1)
    ),
    (
        (0, 0, 1),
        (1, 0, 0),
        (0, 1, 0)
    ),
    (
        (0, 1, 0),
        (1, 0 ,0),
        (0, 0, -1)
    ),
    (
        (0, 0, -1),
        (1, 0, 0),
        (0, -1, 0)
    ),
    (
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, 1)
    ),
    (
        (-1, 0, 0),
        (0, 0, -1),
        (0, -1, 0)
    ),
    (
        (-1, 0, 0),
        (0, 1, 0),
        (0, 0, -1)
    ),
    (
        (-1, 0, 0),
        (0, 0, 1),
        (0, 1, 0)
    ),
    (
        (0, 1, 0),
        (-1, 0, 0),
        (0, 0, 1)
    ),
    (
        (0, 0, 1),
        (-1, 0, 0),
        (0, -1, 0)
    ),
    (
        (0, -1, 0),
        (-1, 0, 0),
        (0, 0, -1)
    ),
    (
        (0, 0, -1),
        (-1, 0, 0),
        (0, 1, 0)
    ),
    (
        (0, 0, -1),
        (0, 1, 0),
        (1, 0, 0)
    ),
    (
        (0, 1, 0),
        (0, 0, 1),
        (1, 0, 0)
    ),
    (
        (0, 0, 1),
        (0, -1, 0),
        (1, 0, 0)
    ),
    (
        (0, -1, 0),
        (0, 0, -1),
        (1, 0, 0)
    ),
    (
        (0, 0, -1),
        (0, -1, 0),
        (-1, 0, 0)
    ),
    (
        (0, -1, 0),
        (0, 0, 1),
        (-1, 0, 0)
    ),
    (
        (0, 0, 1),
        (0, 1, 0),
        (-1, 0, 0)
    ),
    (
        (0, 1, 0),
        (0, 0, -1),
        (-1, 0, 0)
    )
)

def get_candidates(beacon, base_scanner):
    new_candidates = set()
    for rotation in rotations:
        v = np.matmul(rotation, beacon)
        for beacon2 in base_scanner:
            u = np.array(beacon2)
            c = (tuple(u-v), rotation
            
            )
            new_candidates.add(c)
    return new_candidates

t1 = time.perf_counter()
with open('day19.txt', 'r') as f:
    scanner = set()
    i = 0
    for line in f:
        if line.isspace():
            continue
        if '---' in line:
            scanners.append(scanner)
            scanner = set()
            i = 0
            continue
        new_beacon = tuple([int(x) for x in line.strip().split(',')])
        scanner.add(new_beacon)
        i += 1
    scanners.append(scanner)
print(f'Loading data: {time.perf_counter() - t1}')

base_scanner = scanners[0]
active_set = base_scanner.copy()
coords = []
del scanners[0]
while scanners:
    mapped_scanners = []
    new_active_set = set()
    for i, scanner in enumerate(scanners):
        print(i)
        true_candidate = None
        beacon_candidates = []
        for beacon in scanner:
            beacon_candidates.append(get_candidates(beacon, active_set))
        for combs in itertools.combinations(beacon_candidates, 2):
            candidates = combs[0].intersection(combs[1])
            for candidate in candidates:
                correlated = 0
                for beacon in scanner:
                    v = np.matmul(candidate[1], beacon)
                    if any(tuple(beacon2 - v) == candidate[0] for beacon2 in active_set):
                        correlated += 1
                        if correlated >= 12:
                            break

                if correlated >= 12:
                    true_candidate = candidate
                    break
            if true_candidate:
                for beacon in scanner:
                    v = np.matmul(true_candidate[1], beacon)
                    v = tuple(np.array(true_candidate[0]) + v)
                    base_scanner.add(v)
                    new_active_set.add(v)
                    # active_set.add(v)
                mapped_scanners.append(scanner)
                break
        if true_candidate:
            coords.append(true_candidate[0])
    for scanner in mapped_scanners:
        scanners.remove(scanner)
    active_set = new_active_set

max_dist = 0
for comb in itertools.combinations(coords, 2):
    dist = abs(comb[0][0] - comb[1][0]) + abs(comb[0][1] - comb[1][1]) + abs(comb[0][2] - comb[1][2])
    if dist > max_dist:
        max_dist = dist
print(len(base_scanner))
print(max_dist)
print(f'Time: {(time.perf_counter() - t1)//1}s')