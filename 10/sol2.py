"""
We can write the joltage equality problem as a system of linear equations
with the added goal that we wish to minimize sum(x1, x2, x3, ...)

Solution 2 leverages the z3 module to solve the system of equations
and optimize for sum(x1, x2, x3, ...). 

I spent a lot of time thinking about DP optimizations and LP formulations and I
dont like how ultimately this problem forces one to leverage a 3rd party package ;-;
"""
import sys
from functools import cache
from collections import defaultdict, Counter, deque
import z3
data = sys.stdin.read().strip().splitlines()

total_min_presses = 0

for line in data:
    words = line.split()

    target_pattern = words[0][1:-1]

    button_specs = words[1:-1]
    button_effects = [
        [int(x) for x in spec[1:-1].split(',')]
        for spec in button_specs
    ]

    joltage_values = [int(x) for x in words[-1][1:-1].split(',')]

    # create a z3 variable for each button: how many times it is pressed
    # note these are symbolic!
    num_buttons = len(button_effects)
    presses = [z3.Int(f"press_{i}") for i in range(num_buttons)]

    solver = z3.Optimize()

    # every press count must be non-negative
    for p in presses:
        solver.add(p >= 0)

    # build the system of linear equations:
    # for each joltage index "i", sum of presses of buttons that
    # affect "i" must equal the joltage value for that index.
    for idx, required_sum in enumerate(joltage_values):
        contributing = []
        for button_idx, effect_list in enumerate(button_effects):
            if idx in effect_list:
                contributing.append(presses[button_idx])

        solver.add(sum(contributing) == required_sum)

    # minimize total number of button presses
    solver.minimize(sum(presses))

    assert solver.check() == z3.sat
    model = solver.model()

    total_min_presses += sum(model[p].as_long() for p in presses)

print(total_min_presses)