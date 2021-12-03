class Ship:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.aim = 0

    def move(self, instr):
        match instr:
            case ("forward", length):
                self.x = self.x + length
                self.y = self.y + (length * self.aim)
            case ("up", length):
                self.aim -= length
            case ("down", length):
                self.aim += length

def parse(line):
    instr = line.strip().split(" ")
    instr[1] = int(instr[1])
    return instr

ship = Ship()

with open("./day2.txt") as f:
    ship = Ship()
    for line in f.readlines():
        ship.move(parse(line))

print(ship.x * ship.y)
