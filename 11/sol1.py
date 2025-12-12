"""
Solution 1 is a simple dfs to iterate through all possible paths from start and end
keeping track of an answer counter.
"""

from collections import defaultdict

graph = defaultdict(list)

with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip().split()
        key = line[0][:-1]
        for i in range(1, len(line)):
            graph[key].append(line[i])

vis = set()
num_paths = 0
def dfs(node, target):
    global num_paths
    if node == target:
        num_paths += 1
        return
    vis.add(node)
    for neighbor in graph[node]:
        if neighbor not in vis:
            dfs(neighbor, target)
    vis.remove(node)

dfs("you", "out")

print(num_paths)