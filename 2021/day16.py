from functools import reduce

hex_to_bin = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',}

def parse_packet(transmission):
    version = int(transmission[:3], 2)
    type_id = int(transmission[3:6], 2)
    transmission = transmission[6:]
    res = 0
    if type_id == 4:
        num = ''
        while int(transmission[:5], 2) >= 0b10000:
            num += transmission[1:5]
            transmission = transmission[5:]
        num += transmission[1:5]
        transmission = transmission[5:]
        res = int(num, 2)
    else:
        numbers = []
        mode = int(transmission[0], 2)
        transmission = transmission[1:]
        if mode == 0:
            total_length = int(transmission[:15], 2)
            transmission = transmission[15:]
            sub_transmission = transmission[:total_length]
            transmission = transmission[total_length:]
            while len(sub_transmission) > 0:
                sub_transmission, result = parse_packet(sub_transmission)
                numbers.append(result)
        elif mode == 1:
            num_packages = int(transmission[:11], 2)
            transmission = transmission[11:]
            for _ in range(num_packages):
                transmission, result = parse_packet(transmission)
                numbers.append(result)
        if type_id == 0:
            res = sum(numbers)
        elif type_id == 1:
            res = reduce(lambda x, y: x*y, numbers)
        elif type_id == 2:
            res = min(numbers)
        elif type_id == 3:
            res = max(numbers)
        elif type_id == 5:
            res = 1 if numbers[0] > numbers[1] else 0
        elif type_id == 6:
            res = 1 if numbers[0] < numbers[1] else 0
        elif type_id == 7:
            res = 1 if numbers[0] == numbers[1] else 0

    return transmission, res
    

with open('day16.txt', 'r') as f:
    data = f.read()

transmission = ''
for l in data:
    transmission += hex_to_bin[l]
transmission, res = parse_packet(transmission)

print(res)