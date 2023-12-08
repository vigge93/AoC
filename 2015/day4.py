import hashlib

key = "ckczppom"
num = 0

res = ""

while not res.startswith("000000"):
    num += 1
    res = hashlib.md5(f"{key}{num}".encode()).hexdigest()

print(res, num)
