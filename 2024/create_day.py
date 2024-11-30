import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error, must provide day")
        exit(0)
    day = sys.argv[1]
    with open("dayT.py", "r") as code:
        codeText = code.read()
        codeText = codeText.replace("dayT", day)
        with open(f"day{day}.py", "x") as new_code:
            new_code.write(codeText)
        with open(f"day{day}.txt", "x") as f:
            pass
        with open(f"day{day}.xexample-1.txt", "x") as f:
            pass
        with open(f"day{day}.xexample-2.txt", "x") as f:
            pass
