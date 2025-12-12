
line = ''
with open('input.txt', 'r') as f:
    line = f.readline().strip()

ranges = line.split(',')
num_invalid = 0
ans = 0
for r in ranges:
    start, end = r.split('-')
    start_int, end_int = int(start), int(end)
    # 123 - 43355320
    # naive solution:
    for i in range(start_int, end_int+1):
        i_str = str(i)
        if len(i_str) % 2 == 0:
            half_len = len(i_str) // 2
            first_half = i_str[:half_len]
            candidate = int(first_half + first_half)
            if candidate == i:
                ans += i
                num_invalid += 1

    # optimized solution would run in o(sqrt(n)) time and would involve:
    # finding the smallest invalid # larger than start_int and the largest invalid # smaller than end_int
    # then ranging over the half number interval. 

print(ans, num_invalid)