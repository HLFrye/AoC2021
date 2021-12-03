def combine():
    inputs = 0
    items = [(yield), (yield), (yield),]
    while True:
        items[inputs%3] = yield sum(items)
        inputs += 1

count = 0
last = None
combiner = combine()
combiner.send(None)
with open("./day1.txt") as f:
    for line in f.readlines():
        value = int(line.strip())
        value = combiner.send(value)
        if last is not None:
            if value > last:
                count+=1
        last = value
print(count)