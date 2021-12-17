from PIL import Image
from io import BytesIO
from math import sqrt

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

def path_translate(x):
    match x:
        case x if x < 5:
            return [0, 0, 0x44, 0xff]
        case x if x < 10:
            return [0, 0, 0x88, 0xff]
        case x if x < 25:
            return [0, 0, 0xCC, 0xff]
        case x if x < 50:
            return [0, 0, 0xFF, 0xff]
        case x if x < 100:
            return [0x44, 0x44, 0xFF, 0xff]
        case x if x < 200:
            return [0x88, 0x88, 0xFF, 0xff]
        case x if x < 300:
            return [0xCC, 0xCC, 0xFF, 0xff]
        case x:
            return [0xff, 0xff, 0xFF, 0xff]


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

def next_step(path):
    for x in [-1, 1]:
        if path[-1][0] + x > 0 and path[-1][0] + x < width:
            yield [*path, (path[-1][0] + x, path[-1][1])] 
    for y in [-1, 1]:
        if path[-1][1] + y > 0 and path[-1][1] + y < height:
            yield [*path, (path[-1][0], path[-1][1] + y)] 

def has_loop(path):
    return path[-1] in path[0:-1]

def risk(path):
    output = 0
    for pt in path[1:]:
        output += input[pt[1]][pt[0]]
    return output

def dist_to_end(path):
    (x, y) = path[-1]
    return sqrt((width - x) ** 2 + (height - y) ** 2)

input = []
with open("./day15.txt") as f:
    for line in f.readlines():
        input.append(list(map(int, line.strip())))

path = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (4, 3), (4, 4), (5, 4), (5, 5), (6, 5), (7, 5), (7, 6), (7, 7), (7, 8), (8, 8), (8, 9), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10), (13, 10), (14, 10), (14, 11), (14, 12), (14, 13), (15, 13), (15, 14), (15, 15), (15, 16), (15, 17), (16, 17), (17, 17), (17, 18), (18, 18), (19, 18), (19, 19), (20, 19), (20, 20), (20, 21), (21, 21), (22, 21), (22, 22), (22, 23), (22, 24), (22, 25), (22, 26), (23, 26), (23, 27), (23, 28), (23, 29), (23, 30), (24, 30), (25, 30), (25, 31), (26, 31), (27, 31), (28, 31), (28, 32), (29, 32), (30, 32), (31, 32), (32, 32), (32, 33), (33, 33), (33, 34), (34, 34), (35, 34), (35, 35), (36, 35), (37, 35), (38, 35), (38, 36), (38, 37), (39, 37), (39, 38), (39, 39), (39, 40), (39, 41), (39, 42), (40, 42), (41, 42), (41, 43), (42, 43), (43, 43), (44, 43), (44, 44), (44, 45), (45, 45), (45, 46), (46, 46), (47, 46), (47, 47), (47, 48), (48, 48), (48, 49), (48, 50), (49, 50), (49, 51), (50, 51), (50, 52), (51, 52), (51, 53), (52, 53), (53, 53), (54, 53), (55, 53), (55, 54), (56, 54), (56, 55), (57, 55), (57, 56), (57, 57), (57, 58), (58, 58), (58, 59), (59, 59), (59, 60), (59, 61), (60, 61), (61, 61), (62, 61), (63, 61), (63, 62), (63, 63), (64, 63), (64, 64), (64, 65), (65, 65), (65, 66), (65, 67), (65, 68), (66, 68), (67, 68), (68, 68), (68, 69), (69, 69), (70, 69), (70, 70), (70, 71), (71, 71), (71, 72), (72, 72), (72, 73), (73, 73), (74, 73), (74, 74), (75, 74), (75, 75), (75, 76), (75, 77), (76, 77), (76, 78), (77, 78), (78, 78), (79, 78), (79, 79), (79, 80), (80, 80), (80, 81), (81, 81), (81, 82), (82, 82), (83, 82), (83, 83), (84, 83), (84, 84), (84, 85), (85, 85), (85, 86), (86, 86), (86, 87), (87, 87), (88, 87), (88, 88), (88, 89), (89, 89), (90, 89), (90, 90), (90, 91), (91, 91), (92, 91), (92, 92), (93, 92), (93, 93), (94, 93), (94, 94), (95, 94), (95, 95), (96, 95), (96, 96), (96, 97), (97, 97), (97, 98), (98, 98), (98, 99), (99, 99)]
print(risk(path))
exit()

height = len(input)
width = len(input[0])

paths = [[(0, 0)]]
final_path = None
images = [render(input, paths)]
for i in range(200):
    if i % 10 == 0:
        print(i)
    paths.sort(key=lambda x: (risk(x) / len(x)) + dist_to_end(x))
    path = paths.pop(0)
    if path[-1] == (width-1, height-1):
        final_path = path
        break
    for next in next_step(path):
        if not has_loop(next):
            paths.append(next)
    images.append(render(input, paths))

print(final_path)
images[0].save("./day15.gif", save_all=True, append_images=images[1:], optimize=False, duration=100, loops=0)
