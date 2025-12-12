
lines = []
with open('input.txt', 'r') as f:
    for line in f:
        lines.append(line.strip())

total_volt = 0
for line in lines:
    tens, ones = 0, 0
    max_num = 0
    for i in range(len(line)):
        digit = int(line[i])
        if digit > tens and i != len(line)-1:
            tens = digit
            ones = 0
        elif digit > ones:
            ones = digit
        max_num = max(max_num, tens*10 + ones)
    total_volt += max_num
print(total_volt)
        