# 3,4,3,1,2 -> 5934
# f(3) * 2 + f(4) + f(2) + f(1) = 5934

class Lanternfish:
    def __init__(self, x):
        self.family = [x]

    def send(self, _):
        new_fam = []
        for i in range(len(self.family)):
            match self.family[i]:
                case 0:
                    new_fam.append(8)
                    self.family[i] = 6
                case _:
                    self.family[i] -= 1
        self.family = self.family + new_fam
        return len(self.family)

    def get_family(self):
        return self.family

    def get_info(self):
        fish_counts = {}
        for fish in self.family:
            fish_counts[fish] = fish_counts.get(fish, 0) + 1

        return fish_counts

def init(input):
    new_fish_count = {}
    for fish_str in input:
        fish = int(fish_str)
        new_fish_count[fish] = new_fish_count.get(fish, 0) + 1
    fish_trackers = {k: Lanternfish(k) for k in new_fish_count.keys()}
    return new_fish_count, fish_trackers
    
def recompile(fish_trackers, fish_counts):
    new_fish_count = {}
    for fish_num, count in fish_counts.items():
        fish = fish_trackers[fish_num]
        for new_fish, new_count in fish.get_info().items():
            new_fish_count[new_fish] = new_fish_count.get(new_fish, 0) + new_count * count


    fish_trackers = {k: Lanternfish(k) for k in new_fish_count.keys()}
    print(new_fish_count)
    return new_fish_count, fish_trackers

with open("./day6.txt") as f:
    all_fish = f.readline().strip().split(",")

fish_counts, fish_trackers = init(all_fish)

for epoch in range(16):
    for day in range(16):
        count = 0
        for k, fish in fish_trackers.items():
            count += fish.send(None) * fish_counts[k]
        print(f"{day}: {count}")
    fish_counts, fish_trackers = recompile(fish_trackers, fish_counts)
