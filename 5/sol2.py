"""
This is an interval problem. Sort ranges by start index,
then merge intersecting intervals sequentially while updating 
the num_fresh counter.
"""

ranges = []
is_range = True
with open('input.txt', 'r') as f:
    for line in f:
        if len(line.strip()) == 0:
            is_range = False
            continue
        if is_range:
            ranges.append(list(map(int, line.strip().split('-'))))

ranges = sorted(ranges, key=lambda x:x[0])

curr_l, curr_r = ranges[0]
num_fresh = curr_r - curr_l + 1
for i in range(1, len(ranges)):
    target = ranges[i]
    if target[0] < curr_r and target[1] > curr_r:
        num_fresh += target[1]-curr_r
        curr_r = target[1]
    elif target[0] == curr_r:
        num_fresh += target[1]-target[0]
        curr_l = target[0]
        curr_r = target[1]
    elif target[0] > curr_r:
        num_fresh += target[1]-target[0]+1
        curr_l = target[0]
        curr_r = target[1]

print(num_fresh)






