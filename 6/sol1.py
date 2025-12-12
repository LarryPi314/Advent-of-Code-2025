lines = []
with open('input.txt', 'r') as f:
    for line in f:
        lines.append(line.strip())

numbers = [list(map(int, line.split())) for line in lines[:-1]]
operations = lines[-1].split()
results = []

print(len(numbers))
print(operations)
print(len(operations), len(numbers[0]))
for i in range(len(operations)):
    op = operations[i]
    curr_res = 0
    if op == '+':
        for row in numbers:
            curr_res += row[i]
    elif op == '-':
        for row in numbers:
            curr_res -= row[i]
    elif op == '*':
        curr_res = 1
        for row in numbers:
            curr_res *= row[i]
    results.append(curr_res)


print(sum(results))