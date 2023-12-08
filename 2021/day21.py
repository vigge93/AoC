from dataclasses import dataclass

@dataclass
class Player:
    position: int
    score: int = 0

    def move(self, steps):
        self.position = (self.position + steps - 1) % 10 + 1
        self.score += self.position

    def copy(self):
        return Player(self.position, self.score)

player1 = Player(5)
player2 = Player(10)

steps = {}
for i in range(1, 4):
    s = 0
    for j in range(1, 4):
        for k in range(1, 4):
            s = i + j + k
            if s not in steps:
                steps[s] = 0
            steps[s] += 1

def game(player1, player2, player1_turn, depth):
    if player1.score >= 21:
        return [1, 0]
    if player2.score >= 21:
        return [0, 1]
    scores = [0, 0]
    if player1_turn:
        for step in steps:
            player = player1.copy()
            player.move(step)
            res = game(player, player2, False, depth + 1)
            scores[0] += res[0]*steps[step]
            scores[1] += res[1]*steps[step]
        if depth <= 2:
            print(depth, scores)
        return scores
    else:
        for step in steps:
            player = player2.copy()
            player.move(step)
            res = game(player1, player, True,  depth + 1)
            scores[0] += res[0]*steps[step]
            scores[1] += res[1]*steps[step]
        if depth <= 2:
            print(depth, scores)
        return scores

player1_wins, player2_wins = game(player1, player2, True, 1)
print(steps)
print(player1_wins, player2_wins)