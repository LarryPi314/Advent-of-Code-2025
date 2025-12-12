"""
Solution is to simulate the beams splitting
"""

grid = []
with open('input.txt', 'r') as f:
    for line in f:
        grid.append(list(line.strip()))

num_splits = 0
width = len(grid[0])
beams = set()
beams.add(width//2)

for i in range(1, len(grid)):
    row = grid[i]
    to_add = set()
    to_remove = set()
    for beam in beams:
        if row[beam] == '^':
            num_splits += 1
            to_remove.add(beam)
            if beam+1 < len(grid):
                to_add.add(beam+1)
            if beam-1 >= 0:
                to_add.add(beam-1)
    for b in to_remove:
        beams.remove(b)
    for b in to_add:
        beams.add(b)

print(num_splits)