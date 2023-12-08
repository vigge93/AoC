fishes = {i: 0 for i in range(10)}
with open('day6.txt', 'r') as f:
    days = f.read().split(',')
    for day in days:
        d = int(day)
        fishes[d] += 1

for i in range(256):
    fishes[7] += fishes[0]
    fishes[9] += fishes[0]
    fishes[0] = fishes[1]
    fishes[1] = fishes[2]
    fishes[2] = fishes[3]
    fishes[3] = fishes[4]
    fishes[4] = fishes[5]
    fishes[5] = fishes[6]
    fishes[6] = fishes[7]
    fishes[7] = fishes[8]
    fishes[8] = fishes[9]
    fishes[9] = 0
sum = 0
for fish in fishes:
    sum += fishes[fish]
print(sum)