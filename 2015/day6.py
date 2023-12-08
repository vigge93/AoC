lights = {(x, y): 0 for x in range(1000) for y in range(1000)}

with open("day6.txt", "r") as f:
    for line in f:
        parts = line.replace("turn ", "").split()
        inst = parts[0]
        x1, y1 = (int(c) for c in parts[1].split(","))
        x2, y2 = (int(c) for c in parts[-1].split(","))
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if inst == "toggle":
                    lights[(x, y)] += 2
                elif inst == "on":
                    lights[(x, y)] += 1
                elif inst == "off":
                    lights[(x, y)] = max(lights[(x, y)] - 1, 0)

print(sum(lights.values()))
