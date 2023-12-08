numbers = {
    0: {'a', 'b', 'c', 'e', 'f', 'g'},
    1: {'c', 'f'},
    2: {'a', 'c', 'd', 'e', 'g'},
    3: {'a', 'c', 'd', 'f', 'g'},
    4: {'b', 'd', 'c', 'f'},
    5: {'a', 'b', 'd', 'f', 'g'},
    6: {'a', 'b', 'd', 'e', 'f', 'g'},
    7: {'a', 'c', 'f'},
    8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
    9: {'a', 'b', 'c', 'd', 'f', 'g'}
}


count = 0
with open('day8.txt', 'r') as f:
    for line in f:
        decode = {'a': set(), 'b': set(), 'c': set(), 'd': set(), 'e': set(), 'f': set(), 'g': set()}
        decode2 = {0: set(), 1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}
        data = line.split('|')
        input_signals = data[0].split()
        outputs = data[1].split()
        for signals in input_signals:
            num = -1
            if len(signals) == 2:
                num = 1
            elif len(signals) == 3:
                num = 7
            elif len(signals) == 4:
                num = 4
            elif len(signals) == 7:
                num = 8
            else:
                continue
            decode2[num] = set(signals)
        decode['a'] = decode2[7] - decode2[1]
        decode['d'] = decode2[4]
        decode['g'] = decode2[8]
        decode['b'] = decode2[8]
        for signals in input_signals:
            if len(signals) == 5:
                decode['d'] = decode['d'].intersection(set(signals))
                decode['g'] = decode['g'].intersection(set(signals))
            elif len(signals) == 6:
                decode['b'] = decode['b'].intersection(set(signals))
        decode['g'] = decode['g'] - decode['a'] - decode['d']
        decode['b'] = decode['b'] - decode2[7] - decode['g']
        decode['c'] = decode2[8]
        for signals in input_signals:
            if len(signals) == 5 and not decode['b'].intersection(set(signals)):
                decode['c'] = decode['c'].intersection(set(signals))
        decode['c'] = decode['c'] - decode['a'] - decode['d'] - decode['g']
        decode['f'] = decode2[1] - decode['c']
        decode['e'] = decode2[8] - decode2[7] - decode2[4] - decode['g']
        n = 0
        p = 0
        for signals in outputs[::-1]:
            new = set()
            for l in signals:
                for k, num in decode.items():
                    if l in num:
                        new.add(k)
            for k, num in numbers.items():
                if num <= new and new <= num:
                    n += k * 10**p
                    break
            p += 1
        count += n

print(count)
