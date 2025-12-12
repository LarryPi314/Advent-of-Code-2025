

ranges = []
targets = []
is_range = True
with open('input.txt', 'r') as f:
    for line in f:
        if len(line.strip()) == 0:
            is_range = False
            continue
        if is_range:
            ranges.append(list(map(int, line.strip().split('-'))))
        else:
            targets.append(int(line.strip()))

cnt = 0
for target in targets:
    for range in ranges:
        if target >= range[0] and target <= range[1]:
            cnt += 1
            break
print(cnt)





