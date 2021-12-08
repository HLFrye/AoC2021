class FishTracker:
    def __init__(self, inputs):
        self.tracker = [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]
        self.current = 0

        self.waiting = [
            0,
            0,
        ]

        self.waiting_current = 0

        for input in inputs:
            self.tracker[input] += 1
        
    def process(self):
        grown_ups = self.waiting[self.waiting_current]

        # Add the newly born children to the waitlist
        self.waiting[(self.waiting_current + 0) % 2] = self.tracker[self.current]

        # Add the children who have grown up to the main list
        self.tracker[(self.current) % 7] += grown_ups


        self.current = (self.current + 1) % 7
        self.waiting_current = (self.waiting_current + 1) % 2

    def get_result(self):
        return sum([*self.tracker, *self.waiting])

with open("./day6.txt") as f:
    all_fish = map(int, f.readline().strip().split(","))

tracker = FishTracker(all_fish)

for day in range(256):
    tracker.process()

print(f"{tracker.get_result()}")
