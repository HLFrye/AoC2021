def fold(pts, fold):
    fold[1] = int(fold[1])
    match fold:
        case ("x", x):
            for pt in pts:
                if pt[0] > x:
                    yield (x - (pt[0] - x), pt[1])
                else: 
                    yield pt
        case ("y", y):
            for pt in pts:
                if pt[1] > y:
                    yield (pt[0], y - (pt[1] - y))
                else:
                    yield pt

pts = []
folds = []
state = "read_points"
with open("./day13.txt") as f:
    for line in f.readlines():
        if line.strip() == "":
            state="read_folds"
            continue

        match state:
            case "read_points":
                pts.append(tuple(map(int, line.strip().split(","))))
            case "read_folds":
                instr = line.strip().removeprefix("fold along ")
                folds.append(instr.split("="))



setpts = set(pts)
print(len(setpts))
for fld in folds:
    print(f"Folding {fld}")
    setpts = set(fold(setpts, fld))
    print(len(setpts))

maxX = 0
maxY = 0
for pt in setpts:
    maxX = max(maxX, pt[0])
    maxY = max(maxY, pt[1])

for y in range(maxY+1):
    line = ""
    for x in range(maxX+1):
        if (x, y) in setpts:
            line += "#"
        else:
            line += "."
    print(line)