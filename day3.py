def get_freqs(cands):
    freqs = [[0, 0] for x in cands[0]]
    for cand in cands:
        for i, bit in enumerate(cand):
            freqs[i][int(bit)] += 1
    return freqs

def convert(val):
    output = 0
    for i in val:
        output = (output << 1) | int(i)
    return output

class Puzzle:
    def __init__(self):
        self.inputs = []

    def process_input(self, input):
        self.inputs.append(input)

    def get_result(self):
        oxy = convert(self.get_oxy())
        co2 = convert(self.get_co2())
        print(oxy)
        print(co2)
        return oxy * co2

    def get_oxy(self):
        bit = 0
        cands = list(self.inputs)
        while len(cands) > 1:
            freqs = get_freqs(cands)
            target = 0 if freqs[bit][0] > freqs[bit][1] else 1
            cands = list(filter(lambda x: int(x[bit]) == target, cands))
            bit += 1
        return cands[0]

    def get_co2(self):
        bit = 0
        cands = list(self.inputs)
        while len(cands) > 1:
            freqs = get_freqs(cands)
            target = 1 if freqs[bit][0] > freqs[bit][1] else 0
            cands = list(filter(lambda x: int(x[bit]) == target, cands))
            bit += 1

        return cands[0]

def parse(line):
    return line.strip()

puzzle = Puzzle()
with open("./day3.txt") as f:
    for line in f.readlines():
        input = parse(line)
        puzzle.process_input(input)

print(puzzle.get_result())