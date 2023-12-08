from matplotlib import pyplot as plt

dots = set()
instructions = []
with open('day13.txt', 'r') as f:
    for line in f:
        if ',' in line:
            cord = tuple((int(x) for x in line.strip().split(',')))
            dots.add(cord)
        elif 'fold along' in line:
            inst = line.strip().split()[2]
            inst = inst.split('=')
            instructions.append({'dir': inst[0], 'line': int(inst[1])})
for instruction in instructions:
    dir = instruction['dir']
    line = instruction['line']
    remove_dots = set({})
    add_dots = set({})
    for dot in dots:
        if dir == 'x':
            if dot[0] > line:
                remove_dots.add(dot)
                dot = (2*line - dot[0], dot[1])
                add_dots.add(dot)
        elif dir == 'y':
            if dot[1] > line:
                remove_dots.add(dot)
                dot = (dot[0], 2*line - dot[1])
                add_dots.add(dot)
    dots = dots - remove_dots
    dots |= add_dots
x = []
y = []
for dot in dots:
    x.append(dot[0])
    y.append(dot[1])
plt.scatter(x, y)
ax = plt.gca()
ax.set_ylim(ax.get_ylim()[::-1])
plt.show()
print(len(dots))