"""
This solution relies on an extension of the first part. 
We store a candidates array (length 12) where the ith candidate 
represents the largest possible element in the ith digits place
we've encountered thus far. 

"""
lines = []
with open('input.txt', 'r') as f:
    for line in f:
        lines.append(line.strip())

total_volt = 0
for line in lines:
    candidates = [0 for i in range(12)]
    max_num = 0
    L = len(line)
    for i in range(L):
        digit = int(line[i])
        for a in range(12): # digits place we tryna change
            if i <= L-(12-a) and digit > candidates[a]: # only change candidate if its not too late
                candidates[a] = digit
                candidates[a+1:] = [0 for _ in range(12-a-1)]
                break
        # 1 2 3 4 5 6 7 8 9 10 11 12 13
        # 0 1 2 3 4 5 6 7 8 9 10 11
        candidate_num = int(''.join(list(map(str, candidates))))
        max_num = max(candidate_num, max_num)
    # print(candidates)
    # print(max_num)
    total_volt += max_num
print(total_volt)
        