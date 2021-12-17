# I can't resist, I love a good visualization. We're making an animated gif here.

from PIL import Image
from io import BytesIO

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

def render(input):
    height = len(input)
    width = len(input[0])
    pixels = []
    for line in input:
        for cell in line:
            pixels += translate(cell)

    image = Image.frombytes('RGBA', (width, height,), bytes(pixels), 'raw')
    return image

def flash_neighbors(pt):
    for modX in [-1, 0, 1]:
        for modY in [-1, 0, 1]:
            try_pt = (pt[0] + modX, pt[1] + modY)
            match (try_pt):
                case x if x == pt: continue
                case (x, _) if x < 0: continue
                case (_, y) if y < 0: continue
                case (x, _) if x > 9: continue
                case (_, y) if y > 9: continue
                case x: yield x

def apply_rules(input):
    
    flashes = []
    for y, row in enumerate(input):
        for x, col in enumerate(input):
            input[y][x] += 1
            if input[y][x] > 9:
                flashes.append((x, y))

    for flash in flashes:
        for (x, y) in flash_neighbors(flash):
            input[y][x] += 1

    new_flashes = []
    while True:
        for y, row in enumerate(input):
            for x, col in enumerate(input):
                if input[y][x] > 9:
                    pt = (x, y)
                    if pt not in flashes:
                        new_flashes.append(pt)
        if len(new_flashes) == 0:
            break
        for flash in new_flashes:
            for (x, y) in flash_neighbors(flash):
                input[y][x] += 1
        flashes += new_flashes
        new_flashes = []

    for (x, y) in flashes:
        input[y][x] = 0

    return input, len(flashes)        


def save_gif(images):
    images[0].save("./day11.gif", save_all=True, append_images=images[1:], optimize=False, duration=100, loops=0)

def single_color(input):
    first = input[0][0]
    for row in input:
        for cell in row:
            if cell != first:
                return False
    return True

input = []
with open("./day11.txt") as f:
    for line in f.readlines():
        input.append(list(map(int, line.strip())))

images = [render(input)]
flash_count = 0
frame_count = 0
while not single_color(input):
    input, flashes = apply_rules(input)
    images.append(render(input))
    flash_count += flashes
    frame_count += 1
save_gif(images)
print(flash_count)
print(frame_count)