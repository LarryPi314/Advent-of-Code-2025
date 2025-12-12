"""
Part one is O(N^2) bruteforce. 
"""


points = []
with open('input.txt', 'r') as f:
    for line in f:
        points.append(list(map(int, line.strip().split(','))))

def area_rect(pt1, pt2):
    s1 = abs(pt1[0]-pt2[0])+1
    s2 = abs(pt1[1]-pt2[1])+1
    return s1*s2

biggest_rect = 0
for i in range(len(points)):
    for j in range(i+1, len(points)):
        biggest_rect = max(biggest_rect, area_rect(points[i], points[j]))

print(biggest_rect)