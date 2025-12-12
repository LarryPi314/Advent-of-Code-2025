lines = []
with open('input.txt', 'r') as f:
    for line in f:
        lines.append(line.strip())

dr = [-1, 1, -1, 1, 1, -1, 0, 0]
dc = [0, 0, -1, 1, -1, 1, -1, 1]

cnt = 0
nrows = len(lines)
ncols = len(lines[0])
new_grid = []
for r in range(nrows):
    new_row = []
    for c in range(ncols):
        num_adj = 0
        if lines[r][c] != '@':
            continue
        for i in range(8):
            if r+dr[i]>=0 and r+dr[i]<nrows and c+dc[i]>=0 and c+dc[i]<ncols and \
            lines[r+dr[i]][c+dc[i]] == '@':
                num_adj += 1
        if num_adj < 4:
            cnt += 1
print(cnt)


