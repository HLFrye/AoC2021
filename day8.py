from functools import reduce

def matches(filter_func, values):
    for value in values:
        if filter_func(value):
            values.remove(value)
            return value

def has_length(x):
    def checker(code):
        return len(code) == x
    return checker

def missing(known, num):
    def checker(code):
        return len(known.difference(code)) == num
    return checker

def both(a, b):
    return lambda x: a(x) and b(x)

def solve(input, output):
    key = {}
    unknowns = list(map(set, input.split()))
    key[1] = matches(has_length(2), unknowns)
    key[7] = matches(has_length(3), unknowns)
    key[4] = matches(has_length(4), unknowns)
    key[8] = matches(has_length(7), unknowns)
    key[6] = matches(both(has_length(6), missing(key[1], 1)), unknowns)
    key[0] = matches(both(has_length(6), missing(key[4], 1)), unknowns)
    key[9] = matches(has_length(6), unknowns)
    key[3] = matches(both(has_length(5), missing(key[1], 0)), unknowns)
    key[5] = matches(both(has_length(5), missing(key[6], 1)), unknowns)
    key[2] = matches(has_length(5), unknowns)

    assert len(unknowns) == 0

    result = 0
    for digit in map(set, output.split()):
        for outval, inval in key.items():
            if digit == inval:
                result = result * 10 + outval
    return result

# five char digits: 2, 3, 5
# six char digits: 0, 6, 9
# a = 7 - 1
# 6 = missing one of the chars in 1
# 0 = missing one of the chars in 4
# 9 - the other six
# 2 - the five digit with one of the missing chars in 9
# 3 - the five digit with both of the chars in 1
# 5 - the other five
# that missing char is the midbar

count = 0
with open("./day8.txt") as f:
    for line in f.readlines():
        [input, output] = line.split(" | ")
        count += solve(input, output)
print(count)