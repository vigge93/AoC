sea_floor = {}
east = {}
south = {}

with open('day25.txt', 'r') as f:
    for y, line in enumerate(f):
        width = len(line.strip())
        for x, cucumber in enumerate(line.strip()):
            if cucumber == '.':
                continue
            if cucumber == '>':
                east[(y, x)] = cucumber
            elif cucumber == 'v':
                south[(y, x)] = cucumber
            sea_floor[(y, x)] = cucumber
    height = y + 1

steps = 0
moved = True
while moved:
    moved = False
    moveable_east = set()
    for coord, cucumber in east.items():
        if not (coord[0], (coord[1] + 1) % width) in sea_floor:
            moveable_east.add(coord)
    for coord in moveable_east:
        del sea_floor[(coord[0], coord[1])]
        del east[(coord[0], coord[1])]
        sea_floor[(coord[0], (coord[1] + 1) % width)] = '>'
        east[(coord[0], (coord[1] + 1) % width)] = '>'
    moveable_south = set()
    for coord, cucumber in south.items():
        if not ((coord[0] + 1) % height, coord[1]) in sea_floor:
            moveable_south.add(coord)
    for coord in moveable_south:
        del sea_floor[(coord[0], coord[1])]
        del south[(coord[0], coord[1])]
        sea_floor[((coord[0] + 1) % height, coord[1])] = 'v'
        south[((coord[0] + 1) % height, coord[1])] = 'v'
    if moveable_east or moveable_south:
        moved = True
    steps += 1
print(steps)