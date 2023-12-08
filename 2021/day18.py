import json
from math import ceil
from copy import deepcopy

def reduce_number(number):
    while True:
        cont = False
        for n1 in range(len(number)):
            if isinstance(number[n1], list):
                for n2 in range(len(number[n1])):
                    if isinstance(number[n1][n2], list):
                        for n3 in range(len(number[n1][n2])):
                            if isinstance(number[n1][n2][n3], list):
                                for n4 in range(len(number[n1][n2][n3])):
                                    if isinstance(number[n1][n2][n3][n4], list):
                                        brk = False
                                        sn1, sn2, sn3, sn4 = n1, n2 + 1, n3 + 1, n4 + 1
                                        for r1 in range(sn1, -1, -1):
                                            if isinstance(number[r1], int):
                                                number[r1] += number[n1][n2][n3][n4][0]
                                                brk = True
                                                break
                                            for r2 in range(sn2 or len(number[r1]), 0, -1):
                                                r2 -= 1
                                                if isinstance(number[r1][r2], int):
                                                    number[r1][r2] += number[n1][n2][n3][n4][0]
                                                    brk = True
                                                    break
                                                for r3 in range(sn3 or len(number[r1][r2]), 0, -1):
                                                    r3 -= 1
                                                    if isinstance(number[r1][r2][r3], int):
                                                        number[r1][r2][r3] += number[n1][n2][n3][n4][0]
                                                        brk = True
                                                        break
                                                    for r4 in range(sn4 or len(number[r1][r2][r3]), 0, -1):
                                                        r4 -= 1
                                                        if r1 == n1 and r2 == n2 and r3 == n3 and r4 == n4:
                                                            continue
                                                        if isinstance(number[r1][r2][r3][r4], int):
                                                            number[r1][r2][r3][r4] += number[n1][n2][n3][n4][0]
                                                            brk = True
                                                            break
                                                        for r5 in range(len(number[r1][r2][r3][r4]) - 1, -1, -1):
                                                            if isinstance(number[r1][r2][r3][r4][r5], int):
                                                                number[r1][r2][r3][r4][r5] += number[n1][n2][n3][n4][0]
                                                                brk = True
                                                                break
                                                        if brk:
                                                            break
                                                    if brk:
                                                        break
                                                    sn4 = None
                                                if brk:
                                                    break
                                                sn3 = None
                                            if brk:
                                                break
                                            sn2 = None
                                        brk = False
                                        sn1, sn2, sn3, sn4 = n1, n2, n3, n4
                                        for r1 in range(sn1, len(number)):
                                            if isinstance(number[r1], int):
                                                number[r1] += number[n1][n2][n3][n4][1]
                                                brk = True
                                                break
                                            for r2 in range(sn2, len(number[r1])):
                                                if isinstance(number[r1][r2], int):
                                                    number[r1][r2] += number[n1][n2][n3][n4][1]
                                                    brk = True
                                                    break
                                                for r3 in range(sn3, len(number[r1][r2])):
                                                    if isinstance(number[r1][r2][r3], int):
                                                        number[r1][r2][r3] += number[n1][n2][n3][n4][1]
                                                        brk = True
                                                        break
                                                    for r4 in range(sn4, len(number[r1][r2][r3])):
                                                        if r1 == n1 and r2 == n2 and r3 == n3 and r4 == n4:
                                                            continue
                                                        if isinstance(number[r1][r2][r3][r4], int):
                                                            number[r1][r2][r3][r4] += number[n1][n2][n3][n4][1]
                                                            brk = True
                                                            break
                                                        for r5 in range(0, len(number[r1][r2][r3][r4])):
                                                            if isinstance(number[r1][r2][r3][r4][r5], int):
                                                                number[r1][r2][r3][r4][r5] += number[n1][n2][n3][n4][1]
                                                                brk = True
                                                                break
                                                        if brk:
                                                            break
                                                    if brk:
                                                        break
                                                    sn4 = 0
                                                if brk:
                                                    break
                                                sn3 = 0
                                            if brk:
                                                break
                                            sn2 = 0
                                        number[n1][n2][n3][n4] = 0
                                        cont = True
                                        break
                            if cont:
                                break
                    if cont:
                        break
            if cont:
                break
        if cont:
            continue
        for n1 in range(len(number)):
            if isinstance(number[n1], int) and number[n1] > 9:
                cont = True
                number[n1] = [number[n1] // 2, ceil(number[n1]/2)]
                break
            if isinstance(number[n1], list):
                for n2 in range(len(number[n1])):
                    if isinstance(number[n1][n2], int) and number[n1][n2] > 9:
                        cont = True
                        number[n1][n2] = [number[n1][n2] // 2, ceil(number[n1][n2]/2)]
                        break
                    if isinstance(number[n1][n2], list):
                        for n3 in range(len(number[n1][n2])):
                            if isinstance(number[n1][n2][n3], int) and number[n1][n2][n3] > 9:
                                cont = True
                                number[n1][n2][n3] = [number[n1][n2][n3] // 2, ceil(number[n1][n2][n3]/2)]
                                break
                            if isinstance(number[n1][n2][n3], list):
                                for n4 in range(len(number[n1][n2][n3])):
                                    if isinstance(number[n1][n2][n3][n4], int) and number[n1][n2][n3][n4] > 9:
                                        cont = True
                                        number[n1][n2][n3][n4] = [number[n1][n2][n3][n4] // 2, ceil(number[n1][n2][n3][n4]/2)]
                                        break
                            if cont:
                                break
                    if cont:
                        break
            if cont:
                break
        if cont:
            continue
        break

def calc_magnitude(number):
    if isinstance(number[0], list):
        number[0] = calc_magnitude(number[0])
    if isinstance(number[1], list):
        number[1] = calc_magnitude(number[1])
    return number[0]*3 + number[1]*2

numbers = []
with open('day18.txt', 'r') as f:
    for line in f:
        numbers.append(json.loads(line))
max_mag = 0
for number in numbers:
    print(number)
    for number2 in numbers:
        if number is number2:
            continue
        number3 = deepcopy(number)
        number2 = deepcopy(number2)
        number3 = [number3, number2]
        reduce_number(number3)
        mag = calc_magnitude(number3)
        if mag > max_mag:
            max_mag = mag
print(max_mag)
