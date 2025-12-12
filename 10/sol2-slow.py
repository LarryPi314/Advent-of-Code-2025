import re
import sys

def solve():
    """
    Solves Part 2 of the AoC problem: finding the minimum button presses 
    to satisfy linear equations Ax = b with integer constraints.
    """
    
    # Read the input file
    try:
        with open('input.txt', 'r') as f:
            raw_data = f.read().strip()
    except FileNotFoundError:
        print("Error: 'input.txt' not found.")
        return

    machines = []
    
    # Parse the input
    # Format: [indicator] (btn1) (btn2) ... {targets}
    # We only care about (buttons) and {targets} for Part 2.
    lines = raw_data.split('\n')
    for line in lines:
        if not line.strip(): continue
        
        # Extract targets {}
        target_match = re.search(r'\{(.*?)\}', line)
        if not target_match: continue
        targets = list(map(int, target_match.group(1).split(',')))
        
        # Extract buttons ()
        # There are multiple (x,y,z) groups. re.findall captures them all.
        button_matches = re.findall(r'\((.*?)\)', line)
        buttons = []
        for b_str in button_matches:
            if not b_str.strip():
                # Handling empty button case if any
                indices = []
            else:
                indices = list(map(int, b_str.split(',')))
            buttons.append(indices)
            
        machines.append((buttons, targets))

    total_presses = 0
    for i, (buttons, targets) in enumerate(machines):
        # Solve for a single machine
        min_presses = solve_machine(buttons, targets)
        
        if min_presses == float('inf'):
            print(f"Machine {i+1}: No solution found.")
        else:
            total_presses += min_presses

    print(f"\nTotal minimum presses: {total_presses}")

def solve_machine(buttons, targets):
    num_eqs = len(targets)
    num_buttons = len(buttons)
    
    # Map equation index -> list of button indices that affect it
    # This helps us quickly find which buttons are relevant for a specific equation
    eq_to_buttons = [[] for _ in range(num_eqs)]
    for b_idx, effects in enumerate(buttons):
        for eq_idx in effects:
            if eq_idx < num_eqs: # Safety check
                eq_to_buttons[eq_idx].append(b_idx)
                
    # Identify active buttons (any button that affects at least one target)
    # If a button affects no equations, we simply never press it (for min solution).
    active_buttons = set()
    for b_idx in range(num_buttons):
        affects_something = False
        for effects in buttons[b_idx]:
            if effects < num_eqs:
                affects_something = True
                break
        if affects_something:
            active_buttons.add(b_idx)

    # Heuristic Solver using Memoization
    memo = {}

    def backtrack(current_targets, available_buttons):
        # 1. Base Cases
        # If all targets are 0, we are done. Cost is 0.
        if all(t == 0 for t in current_targets):
            return 0
        
        # If any target is negative, we overshot. Invalid path.
        if any(t < 0 for t in current_targets):
            return float('inf')

        # Memoization Key: Tuple of current targets + available buttons
        # We sort available_buttons to ensure uniqueness
        state_key = (tuple(current_targets), tuple(sorted(list(available_buttons))))
        if state_key in memo:
            return memo[state_key]

        # 2. Heuristic: "Smallest Equation First"
        # Find the equation with the fewest distinct buttons that can still affect it.
        # This reduces the branching factor significantly.
        best_eq_idx = -1
        min_options = float('inf')
        
        found_unsatisfied = False
        
        for eq_idx in range(num_eqs):
            if current_targets[eq_idx] == 0:
                continue # This equation is satisfied
            
            found_unsatisfied = True
            
            # Count how many available buttons affect this equation
            relevant = [b for b in eq_to_buttons[eq_idx] if b in available_buttons]
            
            if len(relevant) == 0:
                # Impossible: Target > 0 but no buttons left to change it
                return float('inf')
            
            if len(relevant) < min_options:
                min_options = len(relevant)
                best_eq_idx = eq_idx
                
        if not found_unsatisfied:
            return 0

        # 3. Branching
        # Pick the first button involved in the "tightest" equation
        # We must decide how many times to press this button.
        
        candidates = [b for b in eq_to_buttons[best_eq_idx] if b in available_buttons]
        chosen_button = candidates[0] # Pick one variable to solve for
        
        # Determine strict upper bound for this button
        # The button increments specific counters. It cannot exceed any of their remaining targets.
        max_presses = float('inf')
        for eq_idx in buttons[chosen_button]:
            if eq_idx < num_eqs:
                max_presses = min(max_presses, current_targets[eq_idx])
        
        # We iterate potential press counts.
        # Since we want the MINIMUM total presses, should we iterate 0..max or max..0?
        # Iterating 0..max is safer for finding the absolute minimum sum usually.
        
        local_min_cost = float('inf')
        
        # Remove the chosen button from available set for the recursive calls
        # (It effectively becomes a constant for that branch)
        remaining_buttons = available_buttons - {chosen_button}
        
        for press_count in range(max_presses + 1):
            # Calculate new targets
            new_targets = list(current_targets)
            possible = True
            for affected_eq in buttons[chosen_button]:
                if affected_eq < num_eqs:
                    new_targets[affected_eq] -= press_count
                    if new_targets[affected_eq] < 0:
                        possible = False
                        break
            if not possible:
                continue
                
            # Recurse
            res = backtrack(new_targets, remaining_buttons)
            
            if res != float('inf'):
                total = press_count + res
                if total < local_min_cost:
                    local_min_cost = total
        
        memo[state_key] = local_min_cost
        return local_min_cost

    return backtrack(targets, active_buttons)

if __name__ == '__main__':
    solve()