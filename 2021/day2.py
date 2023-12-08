depth = 0
dist = 0
aim = 0
with open('day2.txt', 'r') as f:
    for line in f:
        line = line.split()
        command = line[0]
        amount = int(line[1])
        if command == 'forward':
            dist += amount
            depth += aim*amount
        elif command == 'down':
            aim += amount
        elif command == 'up':
            aim -= amount
        else:
            print('Error')
print(depth*dist)