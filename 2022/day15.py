import time
from dataclasses import dataclass
# import cProfile


day = 15

@dataclass()
class Line():
    __slots__ = ['startX', 'endX', 'sign']
    startX: int
    endX: int
    sign:int

    def remove(self, start_x, end_x):
        if end_x < self.startX or start_x > self.endX:
            return None
        return Line(max(self.startX, start_x), min(self.endX, end_x), -self.sign)

    def signedLength(self):
        return (abs(self.endX - self.startX))*self.sign

    def __radd__(self, other):
        return self.signedLength() + other

def part_1(data):
    y = 2_000_000
    excluded = []
    for sensor, dist in data['sensors'].items():
        sensorX = sensor[0]
        sensorY = sensor[1]
        w = dist - abs(sensorY - y)
        if w < 0:
            continue
        l = sensorX - w
        r = sensorX + w
        new_line = Line(l, r, 1)
        new_excluded = []
        for line in excluded:
            nl = line.remove(l, r)
            if nl:
                new_excluded.append(nl)
        new_excluded.append(new_line)
        excluded += new_excluded
    return sum(excluded)

def covered(x, y, sensors):
    for sensor, dist in sensors.items():
        sX = sensor[0]
        sY = sensor[1]
        if abs(sX - x) + abs(sY - y) <= dist:
            return True
    return False

def part_2(data):
    lminX, lmaxX = 0, 4_000_000
    lminY, lmaxY = 0, 4_000_000
    # r_matrix = [[1/math.sqrt(2), - 1/math.sqrt(2)], [1/math.sqrt(2), 1/math.sqrt(2)]]
    # r_inv_matrix = [[1/math.sqrt(2), - 1/math.sqrt(2)], [1/math.sqrt(2), 1/math.sqrt(2)]]
    for sensor, dist in data['sensors'].items():
        sensorX = sensor[0]
        sensorY = sensor[1]
        minX = max(sensorX - dist, lminX)
        maxX = min(sensorX + dist, lmaxX)
        for x in range(minX, maxX+1):
            h_dist = abs(sensorX - x)
            offset =  dist - h_dist + 1
            y_up = sensorY + offset
            y_down = sensorY - offset
            if y_up <= lmaxY and not covered(x, y_up, data['sensors']):
                return x*4_000_000 + y_up
            if y_down >= lminY and not covered(x, y_down, data['sensors']):
                return x*4_000_000 + y_down
        if minX - 1 >= lminX and not covered(minX - 1, sensorY, data['sensors']):
            return minX*4_000_000 + sensorY
        if maxX + 1 <= lmaxX and not covered(maxX + 1, sensorY, data['sensors']):
            return minX*4_000_000 + sensorY
    return None

def parse_data():
    data = {'sensors': {}, 'beacons': set()}
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            sensor, beacon = line.strip()[10:].split(":")
            beacon = beacon[22:]
            sensorX, sensorY = sensor.split(",")
            beaconX, beaconY = beacon.split(",")
            sensorX = int(sensorX.split("=")[1])
            sensorY = int(sensorY.split("=")[1])
            beaconX = int(beaconX.split("=")[1])
            beaconY = int(beaconY.split("=")[1])
            data['sensors'][(sensorX, sensorY)] = abs(beaconX - sensorX) + abs(beaconY - sensorY)
            data['beacons'].add((beaconX, beaconY))
    return data

if __name__ == '__main__':
    start_time = time.perf_counter_ns()
    data = parse_data()
    p1 = part_1(data)
    p2 = part_2(data)
    # cProfile.run("part_2(data)")
    end_time = time.perf_counter_ns()
    print(f'=== Day {day:02} ===')
    print(f'  · Part 1: {p1}')
    print(f'  · Part 2: {p2}')
    print(f"  · Elapsed: {(end_time - start_time)/10**6:.3f} ms")