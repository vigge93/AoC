from functools import cache


# @cache
def get_value(key):
    try:
        return int(key)
    except:
        pass
    func = wires[key]
    while not isinstance(func, int):
        func = func()
    return func


wires = {}
with open("day7.txt", "r") as f:
    for line in f:
        lhs, rhs = line.strip().split("->")
        rhs = rhs.strip()
        if lhs.strip().isnumeric():
            wires[rhs] = int(lhs)
        elif " " not in lhs.strip():
            wires[rhs] = lambda lhs=lhs: get_value(lhs.strip())
        elif "NOT" in lhs:
            lhs = lhs.replace("NOT", "").strip()
            wires[rhs] = lambda lhs=lhs: ~get_value(lhs)
        else:
            lhs_op, op, rhs_op = lhs.split()
            if op == "AND":
                wires[rhs] = lambda lhs_op=lhs_op, rhs_op=rhs_op: get_value(
                    lhs_op
                ) & get_value(rhs_op)
            elif op == "OR":
                wires[rhs] = lambda lhs_op=lhs_op, rhs_op=rhs_op: get_value(
                    lhs_op
                ) | get_value(rhs_op)
            elif op == "LSHIFT":
                wires[rhs] = lambda lhs_op=lhs_op, rhs_op=rhs_op: get_value(
                    lhs_op
                ) << int(rhs_op)
            elif op == "RSHIFT":
                wires[rhs] = lambda lhs_op=lhs_op, rhs_op=rhs_op: get_value(
                    lhs_op
                ) >> int(rhs_op)
    func = wires["a"]
    while not isinstance(func, int):
        func = func()
    print(func)
    wires["b"] = func
    # get_value.cache_clear()
    func = wires["a"]
    while not isinstance(func, int):
        func = func()
    print(func)
