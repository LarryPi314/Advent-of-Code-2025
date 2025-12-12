"""
This is a topological sort where we iterate over all nodes
accessable by fork lifts, removing them from the picture.
"""
import queue

lines = []
with open('input.txt', 'r') as f:
    for line in f:
        lines.append(line.strip())

dr = [-1, 1, -1, 1, 1, -1, 0, 0]
dc = [0, 0, -1, 1, -1, 1, -1, 1]

cnt = 0
nrows = len(lines)
ncols = len(lines[0])
neighbor_cnts = []
q = queue.Queue()
vis = set()
for r in range(nrows):
    cnts = [0 for _ in range(ncols)]
    for c in range(ncols):
        if lines[r][c] != '@':
            continue
        for i in range(8):
            if r+dr[i]>=0 and r+dr[i]<nrows and c+dc[i]>=0 and c+dc[i]<ncols and \
            lines[r+dr[i]][c+dc[i]] == '@':
                cnts[c] += 1
        if cnts[c] < 4:
            q.put((r, c))
    neighbor_cnts.append(cnts)

# for row in neighbor_cnts:
#     print(row)

removed_cnt = 0

while not q.empty():
    curr = q.get()
    r, c = curr
    vis.add(curr)
    removed_cnt += 1
    for i in range(8):
        if r+dr[i]>=0 and r+dr[i]<nrows and c+dc[i]>=0 and c+dc[i]<ncols and \
        lines[r+dr[i]][c+dc[i]] == '@':
            neighbor_cnts[r+dr[i]][c+dc[i]] -= 1
            # print(f"original: {(r, c)}, neighbor: {(r+dr[i], c+dc[i])}, neighbor cnts: {neighbor_cnts[r+dr[i]][c+dc[i]]}")
            if neighbor_cnts[r+dr[i]][c+dc[i]] == 3 and (r+dr[i], c+dc[i]) not in vis:
                # print("shrek", (r+dr[i], c+dc[i]))
                q.put((r+dr[i], c+dc[i]))

print(removed_cnt)


