gamma = 0
epsilon = 0
report = []
with open('day3.txt', 'r') as f:
    for line in f:
        nums = [int(x) for x in line.strip()]
        report.append(nums)
report2 = report[:]

for i in range(12):
    count = 0
    for num in report:
        if num[i] == 1:
            count +=1
        else:
            count -= 1
    count2 = 0
    for num in report2:
        if num[i] == 1:
            count2 +=1
        else:
            count2 -= 1
    if len(report) > 1:
        for j in range(len(report) - 1, -1, -1):
            if count < 0:
                if report[j][i] == 1:
                    del(report[j])
            elif report[j][i] == 0:
                del(report[j])
    if len(report2) > 1:
        for j in range(len(report2) - 1, -1, -1):
            if count2 >= 0:
                if report2[j][i] == 1:
                    del(report2[j])
            elif report2[j][i] == 0:
                del(report2[j])

mult = 1
for i in range(len(report[0]) - 1, -1, -1):
    if report[0][i] > 0:
        gamma += mult
    if report2[0][i] > 0:
        epsilon += mult
    mult *= 2
print(gamma*epsilon)