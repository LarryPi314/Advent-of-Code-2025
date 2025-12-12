"""
Sequentially compute subproblems from left to right
"""

lines = []
with open('input.txt', 'r') as f:
    for line in f:
        lines.append(line.rstrip('\n'))


def is_all_whitespace(arr): # helpers
    for ch in arr:
        if ch != ' ':
            return False
    return True

def compute_col_sum_product(curr_op, curr_nums): # compute sum or product of row.
    if curr_op == '+':
        res = 0
        for num in curr_nums:
            res += int(num)
        return res
    else:
        res = 1
        for num in curr_nums:
            res *= int(num)
        return res

numbers = [list(line) for line in lines[:-1]]
operations = list(lines[-1]) # contains white space
results = []

width = len(numbers[0])
height = len(numbers)
looking = True # true if still computing current column's sum/product
curr_nums = []
curr_op = operations[0]
for i in range(width):
    curr_col = [numbers[j][i] for j in range(height)]
    if is_all_whitespace(curr_col) and looking: # found all whitespace means to stop looking and compute sum/product
        looking = False
        res = compute_col_sum_product(curr_op, curr_nums)
        results.append(res)
        curr_nums = []
        continue

    if looking:
        num = ''.join(curr_col)
        curr_nums.append(num)
    elif operations[i] != ' ':
        curr_op = operations[i] # curr pointer i must point to non-white space operation
        num = ''.join(curr_col)
        curr_nums.append(num)
        looking = True

res = compute_col_sum_product(curr_op, curr_nums)
results.append(res)

print(sum(results))