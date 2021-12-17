rules = {}

def add_rule(rule_input):
    parts = rule_input.split(" -> ")
    rules[parts[0]] = parts[0][0] + parts[1] + parts[0][1]

def pairs(input):
    last = None
    for curr in input:
        if last is not None:
            yield last+curr
        last=curr

def get_count(input):
    output = {}
    for c in input:
        output[c] = output.get(c, 0) + 1
    return output

def get_counts(inputs, rules, level):
    if level == 0:
        output = get_count(inputs[1:-1])
        return output
    counts = get_count(inputs[1:-1])
    for pair in pairs(inputs):
        new_input = rules[pair]
        new_counts = get_counts(new_input, rules, level - 1)
        for k, v in new_counts.items():
            counts[k] = counts.get(k, 0) + v
    return counts

def get_overall_counts(base, rules):
    result = get_counts(base, rules, 40)
    result[base[0]] = result.get(base[0], 0) + 1
    result[base[-1]] = result.get(base[-1], 0) + 1
    return result


def update_rules(rules):
    # print(rules)
    new_rules = {}
    for rule, result in rules.items():
        new_output = ""
        for pair in pairs(result):
            if len(new_output) > 0:
                new_output = new_output[:-1]    
            new_output += rules[pair]
        new_rules[rule] = new_output
    return new_rules




with open("./day14.txt") as f:
    base = f.readline().strip()
    f.readline()
    for line in f.readlines():
        add_rule(line.strip())

all_pairs = {k: 1 for k in pairs(base)}

for i in range(40):
    new_pairs = {}
    for key, count in all_pairs.items():
        for pair in pairs(rules[key]):
            print(pair)
            new_pairs[pair] = new_pairs.get(pair, 0) + count
    print(new_pairs)
    # for pair in new_pairs:
    #     if pair in all_pairs:
    #         new_pairs[pair] += all_pairs[pair]

    all_pairs = new_pairs
counts = {}
for key, count in all_pairs.items():
    counts[key[1]] = counts.get(key[1], 0) + count

print(all_pairs)
counts[base[0]] = counts.get(base[0], 0) + 1

# for i in range(4):
#     # print(i)
#     # print(len(rules))
#     print(len(rules["CH"]))
#     rules = update_rules(rules)

# current = base
# for i in range(5):
#     print(f"{i}: {len(current)}")
#     next = ""
#     is_first = True
#     for pair in pairs(current):
#         if is_first:
#             next += rules[pair]
#         else:
#             next += rules[pair][1:]
#     current = next


# counts = get_overall_counts(base, rules)
print(counts)
# counts = get_counts(current)

values = sorted(counts.values())
print(values[-1] - values[0])