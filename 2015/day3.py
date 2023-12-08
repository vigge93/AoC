presents = {(0, 0)}
cords = [0, 0, 0, 0]
offset = 0

with open("day3.txt", "r") as f:
    data = f.readline()

    for i in data:
        if i == "^":
            cords[offset + 1] -= 1
        elif i == "v":
            cords[offset + 1] += 1
        elif i == ">":
            cords[offset] += 1
        elif i == "<":
            cords[offset] -= 1

        presents.add((cords[offset], cords[offset + 1]))
        offset = abs(offset - 2)

print(len(presents))
