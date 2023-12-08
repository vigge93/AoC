boards = []
with open('day4.txt', 'r') as f:
    moves = [int(x) for x in f.readline().split(',')]
    f.readline()
    board = []
    for line in f:
        if line.isspace():
            boards.append(board)
            board = []
        else:
            board.append([int(x) for x in line.split()])

while len(boards) > 0:
    winning_board = []
    winning_board_index = 0
    winning_move = 0
    for move in moves:
        for j, board in enumerate(boards):
            sums = [0 for _ in range(5)]
            for row in board:
                for i, num in enumerate(row):
                    if num == move:
                        row[i] = 0
            for row in board:
                if sum(row) == 0:
                    winning_board = board
                    winning_move = move
                    winning_board_index = j
                    break
                for i, num in enumerate(row):
                    sums[i] += num
            if any(map(lambda x: x == 0, sums)):
                winning_board = board
                winning_board_index = j
                winning_move = move
            if winning_board:
                break
        if winning_board:
            break
    s = 0
    for row in winning_board:
        s += sum(row)
    print (winning_board)
    print(s*winning_move)
    del boards[j]
