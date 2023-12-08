crabs = []
with open('day7.txt', 'r') as f:
    days = f.read().split(',')
    for day in days:
        d = int(day)
        crabs.append(d)
min_fuel = 100000000000000000000
for i in range(min(crabs), max(crabs) + 1):
    fuel = sum([abs(crab - i)*(abs(crab - i) + 1)/2 for crab in crabs])
    if fuel < min_fuel:
        min_fuel = fuel
print(min_fuel)