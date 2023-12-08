iterations = 50
image = []

with open('day20.txt' , 'r') as f:
    algorithm = f.readline()
    f.readline()
    for line in f:
        row = [0 for _ in range(iterations + 1)]
        for pixel in line.strip():
            if pixel == '#':
                row.append(1)
            else:
                row.append(0)
        row += [0 for _ in range(iterations + 1)]
        image.append(row)
    for _ in range(iterations + 1):
        image.append([0 for _ in range(len(image[0]))])
        image.insert(0, [0 for _ in range(len(image[0]))])

def convert(x):
    if x == '#':
        return 1
    else:
        return 0

for i in range(iterations):
    new_image = []
    for i, row in enumerate(image):
        new_row = []
        for j, col in enumerate(row):
            if i == 0 or j == 0 or i >= len(image) - 1 or j >= len(row) - 1:
                if col == 0:
                    new_row.append(convert(algorithm[0]))
                else:
                    new_row.append(convert(algorithm[-1]))
                continue
            index = ''
            for y in range(i-1, i+2):
                for x in range(j-1, j+2):
                    index += str(image[y][x])
            index = int(index, 2)
            new_row.append(convert(algorithm[index]))
        new_image.append(new_row)
    image = new_image
count = 0
for row in image:
    count += sum(row)
print(count)