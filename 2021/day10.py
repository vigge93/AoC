from statistics import median

pairs = [('(', ')'), ('[', ']'), ('{', '}'), ('<', '>')]
score_table = {')': 3, ']': 57, '}': 1197, '>': 25137}
acmp_table = {'(': 1, '[': 2, '{': 3, '<': 4}
scores = []
with open('day10.txt', 'r') as f:
    for line in f:
        score = 0
        for i in range(len(line) - 2, -1, -1):
            for pair in pairs:
                if line[i] == pair[0] and line[i+1] == pair[1]:
                    line = line[:i] + line[i+2:]
                    break
        found = False
        for char in line:
            for pair in pairs:
                if char == pair[1]:
                    # score += score_table[char]
                    found = True
                    break
            if found:
                break
        if not found:
            for char in line[::-1]:
                if char == '\n':
                    continue
                score *= 5
                score += acmp_table[char]
            scores.append(score)
print(median(scores))