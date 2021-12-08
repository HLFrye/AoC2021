import math

class Line:
    def __init__(self, input):
        points = input.split(" -> ")
        p1 = points[0].split(",")
        p2 = points[1].split(",")
        self.x1 = int(p1[0])
        self.y1 = int(p1[1])
        self.x2 = int(p2[0])
        self.y2 = int(p2[1])
        self._points = None

    def is_valid(self):
        return True
#        return self.x1 == self.x2 or self.y1 == self.y2

    def points(self):
        if self._points is None:
            self._points = []
            slope = ((self.x2 - self.x1), (self.y2 - self.y1))
            slope = (0 if slope[0] == 0 else slope[0]/abs(slope[0]), 0 if slope[1] == 0 else slope[1]/abs(slope[1]))
            point = (self.x1, self.y1)
            end = (self.x2, self.y2)
            self._points.append(point)
            while not (point[0] == end[0] and point[1] == end[1]):
                point = (point[0] + slope[0], point[1] + slope[1])
                self._points.append(point)
        return self._points

def find_intersections(lines):
    for i in range(len(lines)):
        if lines[i].is_valid():
            line1_pts = lines[i].points()
            for j in range(i+1, len(lines)):
                if lines[j].is_valid():
                    line2_pts = lines[j].points()
                    for pt in line1_pts:
                        if pt in line2_pts:
                            yield pt

lines = []

with open("./day5.txt") as f:
    for line in f.readlines():
        lines.append(Line(line.strip()))
    
intersections = find_intersections(lines)
print(len(set(intersections)))