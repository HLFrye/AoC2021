def is_opener(c):
    return c in ['<', '(', '[', '{']

def is_closer_for(x, c):
    match x:
        case '<':
            return c == '>'
        case '{':
            return c == '}'
        case '[':
            return c == ']'
        case '(':
            return c == ')'

def get_completion(stack):
    completion = ""
    while len(stack) > 0:
        match stack.pop():
            case '<': completion += '>'
            case '(': completion += ')'
            case '{': completion += '}'
            case '[': completion += ']'
    return completion

def process_line(line):
    stack = []
    for char in line:
        match char:
            case c if is_opener(c):
                stack.append(c)
            case c if is_closer_for(stack[-1], c):
                stack.pop()
            case c:
                return ("syntax", c)
    if len(stack) == 0:
        return ("complete", )
    return ("incomplete", get_completion(stack))

def get_score(c):
    match c:
        case ')': return 3
        case ']': return 57
        case '}': return 1197
        case '>': return 25137
    print(c)

def get_completion_score(completion):
    output = 0
    for c in completion:
        output = output * 5
        match c:
            case ')':
                output += 1
            case ']':
                output += 2
            case '}':
                output += 3
            case '>':
                output += 4
    return output

syntax_score = 0
completion_scores = []

with open("./day10.txt") as f:
    for line in f.readlines():
        result = process_line(line.strip())
        match result:
            case ("syntax", x): syntax_score += get_score(x)
            case ("incomplete", comp): completion_scores.append(get_completion_score(comp))

print(syntax_score)
print(list(enumerate(sorted(completion_scores))))
