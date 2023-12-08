
prev1 = 5000
prev2 = 5000
prev3 = 5000
prev4 = 5000
count = 0
with open('day1.txt', 'r') as f:
    for line in f:
        prev4 = prev3
        prev3 = prev2
        prev2 = prev1
        prev1 = int(line)
        sum1 = prev4 + prev3 + prev2
        sum2 = prev3 + prev2 + prev1
        if sum1 < sum2:
            count += 1
print(count)