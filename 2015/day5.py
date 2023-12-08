res = 0
with open("day5.txt", "r") as f:
    for line in f:
        pairs = [(line[x] + line[x + 1]) for x in range(len(line) - 1)]
        triples = [(line[x] + line[x + 1] + line[x + 2]) for x in range(len(line) - 2)]
        t_found = False
        for t in triples:
            if t[0] == t[2]:
                t_found = True
                break
        if not t_found:
            continue
        for i in range(len(pairs)):
            ridx = pairs[::-1].index(pairs[i])
            idx = len(pairs) - 1 - ridx
            if idx > i + 1:
                res += 1
                break
print(res)
