res = 0

with open("day2.txt", "r") as f:
    for line in f:
        dims = [int(x) for x in line.split("x")]
        res += (
            2 * dims[0]
            + 2 * dims[1]
            + 2 * dims[2]
            - 2 * max(dims)
            + dims[0] * dims[1] * dims[2]
        )
        # res += dims[0]*dims[1]*dims[2]/max(dims)
print(res)
