"""
Three possible solutions for part one: 

(1) There aren't that many buttons so brute force all 
possible subsets of button on/off <-this solution doesnt scale with more buttons
(2) Represent problem as graph where each button is a transition 
between two states (nodes). Then BFS from state 0 to desired state. 
States can be represented as bitmasks.
(3) Use bitwise DP. dp [i, j+1] corresponds to min ops to get to i using up to the jth button
Sol 3 and sol 2 have similar runtimes, namely O(2^M B) for M machines and B buttons.

The below implementation is of Sol 3. 
"""

des_lights = []
buttons = []
INF = 999_999_999

with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip().split(' ')
        des_lights.append(list(line[0][1:-1]))
        curr_buttons = []
        for button in line:
            if button[0] == '(':
                button = button[1:-1]
                curr_buttons.append(list(map(int, button.split(','))))
        buttons.append(curr_buttons)

ans = 0

def toggle(ind, curr_buttons, n): # n is total number of machines
    for m in curr_buttons: # m for machine
        m = n-m-1
        mask = 2**m
        ind ^= mask
    return ind
        
for i in range(len(des_lights)):
    des_light = des_lights[i]

    curr_buttons = buttons[i]
    num_lights = len(des_light)
    num_buttons = len(curr_buttons)
    dp = [[INF for _ in range(num_buttons+1)] for _ in range(2**num_lights)]
    dp[0] = [0 for _ in range(num_buttons+1)]

    # dp [i, j+1] corresponds to min ops to get to i using up to the jth button
    for c in range(1, num_buttons+1):
        for r in range(1, 2**num_lights):
            button = curr_buttons[c-1]
            new_ind = toggle(r, button, num_lights)
            dp[r][c] = min(dp[r][c-1], dp[new_ind][c-1]+1)
    
    des_light_num = 0
    for i in range(num_lights-1, -1, -1):
        if des_light[i] == '#':
            des_light_num += 2**(num_lights-i-1)

    ans += dp[des_light_num][-1]

print(ans)
