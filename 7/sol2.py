"""
Solution is path DP.
"""

grid = []
with open('input.txt', 'r') as f:
    for line in f:
        grid.append(list(line.strip()))

width, height = len(grid[0]), len(grid)

dp = [[0 for _ in range(width)] for _ in range(height)] # dp[i][j] represents number of timelines ending at current cell
dp[0][width//2] = 1
dp[1][width//2] = 1
for i in range(2, height):
    row = grid[i]
    dp[i] = dp[i-1].copy()
    for j in range(width):
        if row[j] == '^':
            if j-1 >= 0: # cells to right and left get more timelines
                dp[i][j-1] += dp[i-1][j]
            if j+1 < width:
                dp[i][j+1] += dp[i-1][j]
            dp[i][j] = 0
        
for row in dp:
    print(row)
print(sum(dp[-1]))
