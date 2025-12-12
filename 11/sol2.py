

"""
Solution 2 implements a modified floyd warshall. If we can find the number of paths
between all pairs of points in O(V^3) time, we can count all possibilities of
going through the desired points between start and finish at the very end.
"""

from collections import defaultdict

graph = defaultdict(list)

edges = []
with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip().split()
        key = line[0][:-1]
        for i in range(1, len(line)):
            edges.append((key, line[i]))
            graph[key].append(line[i])


nodes = list(graph.keys())
nodes.append("out")
nodes = sorted(nodes)
nodes_to_inds = {}

for i, node in enumerate(nodes):
    nodes_to_inds[node] = i

for i in range(len(edges)):
    edges[i] = (nodes_to_inds[edges[i][0]], nodes_to_inds[edges[i][1]])

print(len(nodes), len(edges), "desired: ", nodes_to_inds['out'])

num_paths = [[0 for _ in range(len(nodes))] for _ in range(len(nodes))]
for i in range(len(nodes)):
    num_paths[i][i] = float('inf')

def print_num_paths(num_paths):
    for row in num_paths:
        print(row)
    print()

# print_num_paths(num_paths)
for edge in edges:
    num_paths[edge[0]][edge[1]] = 1

# a = float('inf')
# b = a * 1
# b += 1
# print(b)

for a in range(len(nodes)):
    for b in range(len(nodes)):
        for c in range(len(nodes)):
            if a == b or b == c or a == c:
                continue
            num_paths[b][c] += num_paths[b][a]*num_paths[a][c] # use a as intermediary node between b and c

# print_num_paths(num_paths)
int_svr = nodes_to_inds['svr']
int_fft = nodes_to_inds['fft']
int_dac = nodes_to_inds['dac']
int_out = nodes_to_inds['out']

svr_fft = num_paths[int_svr][int_fft]
fft_dac = num_paths[int_fft][int_dac]
dac_out = num_paths[int_dac][int_out]

svr_dac = num_paths[int_svr][int_dac]
dac_fft = num_paths[int_dac][int_fft]
fft_out = num_paths[int_fft][int_out]

print(svr_fft * fft_dac * dac_out + svr_dac * dac_fft * fft_out)
