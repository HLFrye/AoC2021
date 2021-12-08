def print_list(l):
    for i in range(0, 5):
        print(l[0+(i*5):5+(i*5)])

class Board:
    def __init__(self):
        self.board = []
        self.matched = []

    def loadrow(self, row):
        for val in row.strip().split():
            self.board.append(int(val))
            self.matched.append(False)

    def has_bingo(self):
        # check rows
        for i in [0, 5, 10, 15, 20]:
            for spot in range(i, i+5):
                if not self.matched[spot]:
                    break
            else:
                return True
        
        # check columns
        for i in [0, 1, 2, 3, 4]:
            for spot in range(i, i+21, 5):
                if not self.matched[spot]:
                    break
            else:
                return True

        return False

    def call_number(self, number):
        if number in self.board:
            self.matched[self.board.index(number)] = True

    def get_score(self, number):
        sum = 0
        for i, val in enumerate(self.matched):
            if not val:
                sum += self.board[i]

        return sum * number

def main():
    boards = []
    with open("./day4.txt") as f:
        order = map(int, f.readline().strip().split(","))
        current = None
        for line in f.readlines():
            if line.strip() == "":
                if current is not None:
                    boards.append(current)
                current = Board()
            else:
                current.loadrow(line)
        boards.append(current)

    last_winner_score = None

    for ball in order:
        for board in boards:
            if board.has_bingo():
                continue
            board.call_number(ball)
            if board.has_bingo():
                last_winner_score = board.get_score(ball)

    print(last_winner_score)

if __name__ == '__main__':
    main()
        