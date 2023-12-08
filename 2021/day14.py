rules = {}

with open('day14.txt', 'r') as f:
    template = f.readline().strip()
    for line in f:
        if not line.isspace():
            rule = line.strip().split('->')
            rules[rule[0].strip()] = rule[1].strip()

pairs = {}
for i in range(len(template) - 1):
    pair = template[i] + template[i+1]
    if not pair in pairs:
        pairs[pair] = 0
    pairs[pair] += 1

for step in range(40):
    pairs_temp = pairs.copy()
    for pair, count in pairs.items():
        new_pairs1 = pair[0] + rules[pair]
        new_pairs2 = rules[pair] + pair[1]
        if not new_pairs1 in pairs_temp:
            pairs_temp[new_pairs1] = 0
        if not new_pairs2 in pairs_temp:
            pairs_temp[new_pairs2] = 0
        pairs_temp[new_pairs1] += count
        pairs_temp[new_pairs2] += count
        pairs_temp[pair] -= count
    pairs = pairs_temp

first = {}
last = {}
counts = {}
for l, count in pairs.items():
    if l[0] not in first:
        first[l[0]] = 0
    first[l[0]] += count
    if l[1] not in last:
        last[l[1]] = 0
    last[l[1]] += count
    if l[0] not in counts:
        counts[l[0]] = 0
    if l[1] not in counts:
        counts[l[1]] = 0
    counts[l[0]] += count
    counts[l[1]] += count
for l, count in counts.items():
    if first[l] != last[l]:
        counts[l] = (count - 1) / 2 + 1
    else:
        counts[l] = count/2

# First > last -> Begins with l
# Last > First -> Ends with l
print(first)
print()
print(last)
print()
print(counts)
counts = list(counts.values())
print(max(counts) - min(counts))