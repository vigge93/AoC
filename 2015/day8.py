import re

res = 0
with open("day8.txt", "r") as f:
    for line in f:
        # line_r = re.sub(r'\\(x[a-f0-9]{2}|\\|")', '_', line.strip()[1:-1])
        line_r = '"' + re.sub(r'("|\\)', r"\\\1", line.strip()) + '"'
        print(line_r)
        res += len(line_r) - len(line.strip())
print(res)
