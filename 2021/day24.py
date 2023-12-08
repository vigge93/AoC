
register = {'w': 0, 'x': 0, 'y': 0, 'z': 0}

def inp(a):
    register[a] = input_stream[0]
    del input_stream[0]

def add(a, b):
    if isinstance(b, str):
        register[a] += register[b]
    else:
        register[a] += b

def mul(a, b):
    if isinstance(b, str):
        register[a] *= register[b]
    else:
        register[a] *= b

def div(a, b):
    if isinstance(b, str):
        register[a] //= register[b]
    else:
        register[a] //= b

def mod(a, b):
    if isinstance(b, str):
        register[a] %= register[b]
    else:
        register[a] %= b

def eql(a, b):
    if isinstance(b, str):
        register[a] = int(register[a] == register[b])
    else:
        register[a] = int(register[a] == b)

def reset():
    global register
    register = {'w': 0, 'x': 0, 'y': 0, 'z': 0}

input_stream = [2, 6]
instructions = []

with open('day24.txt', 'r') as f:
    for line in f:
        line = line.strip().split()
        instructions.append(line)

for model_number in range(99999999999999, 11111111111110, -1):
    if '0' in str(model_number):
        continue
    reset()
    input_stream = [int(i) for i in str(model_number)]
    for instruction in instructions:
        operator = instruction[0]
        a = instruction[1]
        b = None
        if len(instruction) == 3:
            b = instruction[2]
            try:
                b = int(b)
            except ValueError:
                b = f'"{b}"'
        if b is not None:
            exec(f'{operator}("{a}", {b})')
        else:
            exec(f'{operator}("{a}")')
    if model_number % 128 == 0:
        print(model_number, register['z'])
    if register['z'] == 0:
        print(model_number)
        break