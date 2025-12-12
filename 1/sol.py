"""
Solution to part 2. This is a straight forward simulation. 
"""
moves = []
with open('input.txt', 'r') as f:
    for line in f:
        moves.append(line.strip())

dial = 50
cnt = 0
for move in moves:
    if move[0] == 'L':
        if int(move[1:]) >= dial:
            cnt += (int(move[1:]) - dial) // 100
            if dial != 0:
                cnt += 1
        dial -= int(move[1:])
        dial %= 100
    elif move[0] == 'R':
        if int(move[1:]) + dial > 99:
            cnt += (int(move[1:]) + dial) // 100
        dial += int(move[1:])
        dial %= 100
    
print(cnt)
