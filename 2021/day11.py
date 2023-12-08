from dataclasses import dataclass

octipi = []
flashes = 0

@dataclass
class Octipi:
    energy: int = 0
    flashed: bool = False

def flash_octipi(octipus, x, y):
    global flashes
    flashes += 1
    octipus.flashed = True
    octipus.energy = 0
    if x > 0:
        if not octipi[y][x-1].flashed:
            octipi[y][x-1].energy += 1
            if octipi[y][x-1].energy > 9:
                flash_octipi(octipi[y][x-1], x-1, y)
        if y > 0:
            if not octipi[y-1][x-1].flashed:
                octipi[y-1][x-1].energy += 1
                if octipi[y-1][x-1].energy > 9:
                    flash_octipi(octipi[y-1][x-1], x-1, y-1)
        if y < 9:
            if not octipi[y+1][x-1].flashed:
                octipi[y+1][x-1].energy += 1
                if octipi[y+1][x-1].energy > 9:
                    flash_octipi(octipi[y+1][x-1], x-1, y+1)
    if x < 9:
        if not octipi[y][x+1].flashed:
            octipi[y][x+1].energy += 1
            if octipi[y][x+1].energy > 9:
                flash_octipi(octipi[y][x+1], x+1, y)
        if y > 0:
            if not octipi[y-1][x+1].flashed:
                octipi[y-1][x+1].energy += 1
                if octipi[y-1][x+1].energy > 9:
                    flash_octipi(octipi[y-1][x+1], x+1, y-1)
        if y < 9:
            if not octipi[y+1][x+1].flashed:
                octipi[y+1][x+1].energy += 1
                if octipi[y+1][x+1].energy > 9:
                    flash_octipi(octipi[y+1][x+1], x+1, y+1)
    if y > 0:
        if not octipi[y-1][x].flashed:
            octipi[y-1][x].energy += 1
            if octipi[y-1][x].energy > 9:
                flash_octipi(octipi[y-1][x], x, y-1)
    if y < 9:
        if not octipi[y+1][x].flashed:
            octipi[y+1][x].energy += 1
            if octipi[y+1][x].energy > 9:
                flash_octipi(octipi[y+1][x], x, y+1)

with open('day11.txt', 'r') as f:
    for line in f:
        row = []
        for chr in line:
            if chr == '\n':
                continue
            row.append(Octipi(energy=int(chr)))
        octipi.append(row)

all_flashed = False
i = 0
while not all_flashed:
    i += 1
    for row in octipi:
        for oct in row:
            oct.energy += 1
            oct.flashed = False
    for y, row in enumerate(octipi):
        for x, oct in enumerate(row):
            if oct.energy > 9 and not oct.flashed:
                flash_octipi(oct, x, y)
    all_flashed = True
    for row in octipi:
        for oct in row:
            if not oct.flashed:
                all_flashed = False
                break
    if all_flashed:
        print(i)
        break
print(flashes)