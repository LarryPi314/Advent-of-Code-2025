"""
Brute force
"""
line = ''
with open('input.txt', 'r') as f:
    line = f.readline().strip()


def has_pattern(n):
    n_str = str(n)
    for i in range(1, len(n_str)):
        if len(n_str) % i == 0:
            num_blocks = len(n_str) // i
            candidate = n_str[:i] * num_blocks
            candidate = int(candidate)
            if candidate == n:
                return True
    
    return False

ranges = line.split(',')
num_invalid = 0
ans = 0
for r in ranges:
    start, end = r.split('-')
    start_int, end_int = int(start), int(end)
    for i in range(start_int, end_int+1):
        if has_pattern(i):
            num_invalid += 1
            ans += i


print(ans, num_invalid)