def is_complete(path):
    return path[-1] == "end"

def is_big(x: str):
    return not x.islower()

def not_visited(path, x):
    return not x in path

def can_double(path):
    seen = []
    for step in path:
        if is_big(step):
            continue
        if step in seen:
            return False
        seen.append(step)
    return True

class Day12:
    def __init__(self):
        self.links = {}
        with open("./day12.txt") as f:
            for line in f.readlines():
                begin, end = line.strip().split("-")
                if not begin in self.links:
                    self.links[begin] = []
                self.links[begin].append(end)
                if not end in self.links:
                    self.links[end] = []
                self.links[end].append(begin)

    def choices(self, path):
        for next_step in self.links[path[-1]]:
            if next_step == "start":
                continue
            elif is_big(next_step):
                yield [next_step]
            elif not_visited(path, next_step) or can_double(path):
                yield [next_step]            

    def traverse(self, path):
        if is_complete(path):
            yield path
        else:
            for choice in self.choices(path):
                yield from self.traverse(path + choice)

puzzle = Day12()
paths = puzzle.traverse(["start"])
count = 0
for path in paths:
    count += 1
    print(f"{count}: {path}")