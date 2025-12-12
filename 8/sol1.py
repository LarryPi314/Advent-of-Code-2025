"""
Solution is union find. This is akin to kruskal's MST algorithm.
"""

coords = []
with open('input.txt', 'r') as f:
    for line in f:
        coords.append(list(map(int, line.strip().split(','))))

parents = [i for i in range(len(coords))] # ith index stores parent of box i
repr_cnt = [1 for _ in range(len(coords))] # size of circuit

def find(a):
    while parents[a] != a:
        a = parents[a]
    return a

def merge(a, b):
    p_a, p_b = find(a), find(b)
    if p_a == p_b:
        return
    
    if repr_cnt[a] < repr_cnt[b]:
        repr_cnt[p_b] += repr_cnt[p_a]
        parents[p_a] = p_b
    else:
        repr_cnt[p_a] += repr_cnt[p_b] 
        parents[p_b] = p_a

def dist(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2

pairwise_dists = [(i, j, dist(coords[i], coords[j])) for i in range(len(coords)) for j in range(i+1, len(coords))]
pairwise_dists = sorted(pairwise_dists, key=lambda x: x[2])

for i in range(1000):
    d = pairwise_dists[i]
    merge(d[0], d[1])

circuit_sizes = []
for i in range(len(parents)):
    if parents[i] == i:
        circuit_sizes.append(repr_cnt[i])

circuit_sizes = sorted(circuit_sizes, reverse=True)

print(circuit_sizes[0]*circuit_sizes[1]*circuit_sizes[2])