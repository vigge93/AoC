coord_table = {}
with open('day5.txt', 'r') as f:
    for line in f:
        coords = line.split(' -> ')
        x1, y1 = [int(x) for x in coords[0].split(',' )]
        x2, y2 = [int(x) for x in coords[1].split(',' )]
        
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            for i in range(y1, y2+1):
                if (x1, i) not in coord_table:
                    coord_table[(x1, i)] = 0
                coord_table[(x1, i)] += 1
        elif y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            for i in range(x1, x2+1):
                if (i, y1) not in coord_table:
                    coord_table[(i, y1)] = 0
                coord_table[(i, y1)] += 1
        elif abs(x2-x1) == abs(y2-y1):
            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            for i in range(0, x2 - x1 + 1):
                newy = y1 + i if y1 < y2 else y1 - i
                if (x1 + i, newy) not in coord_table:
                    coord_table[(x1 + i, newy)] = 0
                coord_table[(x1 + i, newy)] += 1
coord_table = {k: i for k, i in coord_table.items() if i > 1}
print (len(coord_table))