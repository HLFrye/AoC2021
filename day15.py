from types import NoneType
from PIL import Image
from io import BytesIO
from math import sqrt
from dataclasses import dataclass
from colour import Color

def translate(x):
    match x:
        case 0:
            return [0, 0, 0, 0xFF]
        case 1:
            return [0x55, 0, 0, 0xFF]
        case 2:
            return [0xAA, 0, 0, 0xFF]
        case 3: 
            return [0xFF, 0, 0, 0xFF]
        case 4:
            return [0xFF, 0x55, 0, 0xFF]
        case 5:
            return [0xFF, 0xAA, 0, 0xFF]
        case 6:
            return [0xFF, 0xFF, 0, 0xFF]
        case 7:
            return [0xFF, 0xFF, 0x55, 0xFF]
        case 8:
            return [0xFF, 0xFF, 0xAA, 0xFF]
        case 9:
            return [0xFF, 0xFF, 0xFF, 0xFF]

def transform_color(color):
    return [
        int(color.rgb[0] * 255), 
        int(color.rgb[1] * 255), 
        int(color.rgb[2] * 255), 
        0xFF
    ]

path_colors = list(map(transform_color, Color("red").range_to(Color("violet"), 430)))
def path_translate(x):
    return path_colors[x]

def render(input, paths):
    height = len(input)
    width = len(input[0])
    pixels = []
    for y, line in enumerate(input):
        for x, cell in enumerate(line):
            count = 0
            for path in paths:
                if (x, y) in path:
                    count += 1
            if count == 0:
                pixels += translate(cell)
            else:
                pixels += path_translate(count)

    image = Image.frombytes('RGBA', (width, height,), bytes(pixels), 'raw')
    return image

@dataclass
class Node:
    x: int
    y: int
    risk: int
    dist: int | NoneType

class Graph:
    def __init__(self, input):
        self.nodes = []
        for y, row in enumerate(input):
            self.nodes.append([])
            for x, cell in enumerate(row):
                self.nodes[-1].append(Node(x, y, cell, None))

        self.width = len(input[0])
        self.height = len(input)

        self.order = []
        for x in range(self.width):
            for y in range(self.height):
                self.order.append((x, y))

        for x in range(0, 2):
            for y in range(0, 2):
                print(f"{x}, {y} loaded as {self.nodes[y][x]}")

        self.order.sort(key=lambda x: sqrt(x[0]**2 + x[1]**2))
        
        self.nodes[0][0].dist = 0
        self.images = [self.render()]

        print(self.nodes[0][0])

    def render(self, path=None):
        pixels = []
        for y in range(self.height):
            for x in range(self.width):
                if path is not None and (x, y) in path:
                    pixels += [0xFF, 0x00, 0x00, 0xFF]
                elif self.nodes[y][x].dist is None:
                    pixels += translate(self.nodes[y][x].risk)
                else:
                    pixels += path_translate(self.nodes[y][x].dist)

        image = Image.frombytes('RGBA', (self.width, self.height,), bytes(pixels), 'raw')
        return image


    def get_neighbors(self, node):
        def is_valid(x, y):
            return x >= 0 and x < self.width and y >= 0 and y < self.height
        
        for x in [-1, 1]:
            if is_valid(node.x + x, node.y):
                yield self.nodes[node.y][node.x + x]
        for y in [-1, 1]:
            if is_valid(node.x, node.y + y):
                yield self.nodes[node.y + y][node.x]

    def find_path(self):
        iter = 0
        path = []
        curr = self.nodes[-1][-1]
        while curr.dist != 0:
            # if iter < 10:
            #     iter += 1
            #     print(curr)
            path.append((curr.x, curr.y))
            closest = None
            for pt in self.get_neighbors(curr):
                if closest is None:
                    closest = pt
                elif closest.dist > pt.dist:
                    closest = pt
            curr = closest
        path.append((curr.x, curr.y))
        return path

    def calculate_dists(self):
        count = 0
        for pt in self.order:
            node = self.nodes[pt[1]][pt[0]]
            if count < 3:
                print(f"{pt}: {node}")
            for neighbor in self.get_neighbors(node):
                new_risk = node.dist + neighbor.risk
                if count < 3:
                    print(f"  {neighbor} -> {new_risk}")
                match neighbor.dist:
                    case None:
                        neighbor.dist = new_risk
                    case x if x > new_risk:
                        neighbor.dist = new_risk
            count += 1
            if count % 200 == 0:
                self.images.append(self.render())

        path = self.find_path()
        self.images.append(self.render(path))
        self.images[0].save("./day15.gif", save_all=True, append_images=self.images[1:], optimize=False, duration=100, loops=0)
        count = 0
        iter = 0
        print(f"{list(map(lambda x: self.nodes[x[1]][x[0]], path[:5]))} -> {list(map(lambda x: self.nodes[x[1]][x[0]], path[-5:]))}")
        path.reverse()
        print("Starting")
        for pt in path:
            if iter < 10:
                print(f"{pt} -> {node}")
            node = self.nodes[pt[1]][pt[0]]
            count += node.risk
            iter += 1

        # 402 is too high
        # 393 is too high
        print(count)
        print(self.nodes[-1][-1].dist)

input = []
with open("./day15.txt") as f:
    for line in f.readlines():
        input.append(list(map(int, line.strip())))

graph = Graph(input)
graph.calculate_dists()
