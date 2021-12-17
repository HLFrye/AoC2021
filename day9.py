from dataclasses import dataclass

@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int

@dataclass
class Cell:
    value: int
    loc: Point
    falls_to: Point

class Board:
    def __init__(self, board):
        self.board = board
        self.cells = []
        self.maxX = len(board[0])
        self.maxY = len(board)

    def get_neighbors(self, cell):
        def output(x, y):
            return ((x,y,), self.board[y][x],)

        if cell.loc.x > 0:
            yield output(cell.loc.x-1, cell.loc.y)
        if cell.loc.x < self.maxX - 1:
            yield output(cell.loc.x+1, cell.loc.y)
        if cell.loc.y > 0:
            yield output(cell.loc.x, cell.loc.y-1)
        if cell.loc.y < self.maxY - 1:
            yield output(cell.loc.x, cell.loc.y+1)

    def init_cells(self):
        for x in range(self.maxX):
            for y in range(self.maxY):
                loc = Point(x, y)
                cell = Cell(self.board[y][x], loc, None)
                lowest_neighbor = None
                for point, neighbor in self.get_neighbors(cell):
                    if neighbor <= cell.value:
                        if lowest_neighbor is None:
                            lowest_neighbor = (point, neighbor)
                        else:
                            if neighbor < lowest_neighbor[1]:
                                lowest_neighbor = (point, neighbor)
                if lowest_neighbor is not None:
                    cell.falls_to = Point(*(lowest_neighbor[0]))
                self.cells.append(cell)

    def calculate_risk(self):
        risk = 0
        for cell in self.cells:
            if cell.falls_to is None:
                print(cell)
                risk += cell.value + 1
        return risk

    def find_basins(self):
        basins = {}

        for cell in self.cells:
            if cell.falls_to is None:
                continue
            last = cell
            falls_to = cell.falls_to
            while falls_to is not None:
                last = self.get_cell(falls_to)
                falls_to = last.falls_to

            cell.falls_to = last.loc

        for cell in self.cells:
            if cell.falls_to is not None and cell.value < 9:
                count = basins.get(cell.falls_to, 1) + 1
                basins[cell.falls_to] = count

        print(basins)

        top_basins = list(sorted(basins.values(), reverse=True))[0:3]
        return top_basins[0] * top_basins[1] * top_basins[2]

    def get_cell(self, pt):
        for cell in self.cells:
            if cell.loc == pt:
                return cell

rows = []
with open("./day9.txt") as f:
    for line in f.readlines():
        rows.append(list(map(int, list(line.strip()))))

board = Board(rows)
board.init_cells()
risk = board.calculate_risk()
print(risk)
basins = board.find_basins()
print(basins)
