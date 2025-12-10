#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 10: Factory
"""
import re
from scipy.optimize import milp, LinearConstraint, Bounds
import numpy as np

def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().strip()


def parse_machine(line):
    """Parse a machine specification line."""
    # Extract the indicator light pattern
    lights_match = re.search(r'\[([.#]+)\]', line)
    lights = lights_match.group(1)
    target_lights = [1 if c == '#' else 0 for c in lights]
    
    # Extract button wirings
    buttons = []
    for match in re.finditer(r'\(([0-9,]+)\)', line):
        button_lights = [int(x) for x in match.group(1).split(',')]
        buttons.append(button_lights)
    
    # Extract joltage requirements
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    target_joltage = [int(x) for x in joltage_match.group(1).split(',')]
    
    return target_lights, buttons, target_joltage


def solve_machine(target, buttons):
    """
    Solve a machine configuration using Gaussian elimination over GF(2).
    Returns the minimum number of button presses needed.
    """
    n_lights = len(target)
    n_buttons = len(buttons)
    
    # Build the matrix where each column represents a button
    # and each row represents a light
    # matrix[i][j] = 1 if button j toggles light i
    matrix = []
    for i in range(n_lights):
        row = []
        for button in buttons:
            row.append(1 if i in button else 0)
        row.append(target[i])  # Augmented column
        matrix.append(row)
    
    # Gaussian elimination over GF(2)
    pivot_row = 0
    pivot_cols = []
    free_cols = []
    
    for col in range(n_buttons):
        # Find pivot
        found_pivot = False
        for row in range(pivot_row, n_lights):
            if matrix[row][col] == 1:
                # Swap rows
                matrix[pivot_row], matrix[row] = matrix[row], matrix[pivot_row]
                found_pivot = True
                break
        
        if not found_pivot:
            free_cols.append(col)
            continue
        
        pivot_cols.append(col)
        
        # Eliminate
        for row in range(n_lights):
            if row != pivot_row and matrix[row][col] == 1:
                for c in range(n_buttons + 1):
                    matrix[row][c] ^= matrix[pivot_row][c]
        
        pivot_row += 1
    
    # Check if system is solvable
    for row in range(pivot_row, n_lights):
        if matrix[row][n_buttons] == 1:  # 0 = 1, inconsistent
            return None
    
    # Try all combinations of free variables to find minimum
    min_presses = float('inf')
    
    for free_val in range(1 << len(free_cols)):
        solution = [0] * n_buttons
        
        # Set free variables
        for i, col in enumerate(free_cols):
            solution[col] = (free_val >> i) & 1
        
        # Back substitution for pivot variables
        for i in range(len(pivot_cols) - 1, -1, -1):
            col = pivot_cols[i]
            row = i
            
            val = matrix[row][n_buttons]
            for c in range(col + 1, n_buttons):
                if matrix[row][c] == 1:
                    val ^= solution[c]
            solution[col] = val
        
        # Count button presses
        presses = sum(solution)
        min_presses = min(min_presses, presses)
    
    return min_presses if min_presses != float('inf') else None


def part1(data):
    """Find minimum button presses for all machines."""
    lines = data.split('\n')
    total = 0
    
    for line in lines:
        if line.strip():
            target_lights, buttons, _ = parse_machine(line)
            presses = solve_machine(target_lights, buttons)
            if presses is not None:
                total += presses
    
    return total


def solve_joltage(target, buttons):
    """
    Solve joltage configuration using mixed-integer linear programming.
    """
    n_counters = len(target)
    n_buttons = len(buttons)
    
    # Build constraint matrix A where A[i][j] = 1 if button j affects counter i
    A = np.zeros((n_counters, n_buttons))
    for j, button in enumerate(buttons):
        for counter_idx in button:
            A[counter_idx][j] = 1
    
    b_lower = np.array(target, dtype=float)
    b_upper = np.array(target, dtype=float)
    
    # Objective: minimize sum of all button presses
    c = np.ones(n_buttons)
    
    # Integer constraints
    integrality = np.ones(n_buttons, dtype=int)
    
    # Bounds: each button press count >= 0
    bounds = Bounds(lb=np.zeros(n_buttons), ub=np.inf)
    
    # Constraints: A @ x == b
    constraints = LinearConstraint(A, lb=b_lower, ub=b_upper)
    
    # Solve integer linear program
    result = milp(c, integrality=integrality, constraints=constraints, bounds=bounds)
    
    if not result.success:
        return None
    
    # Use the objective function value directly (already the sum)
    return int(round(result.fun))


def part2(data):
    """Find minimum button presses for joltage configuration."""
    lines = data.split('\n')
    total = 0
    
    for line in lines:
        if line.strip():
            _, buttons, target_joltage = parse_machine(line)
            presses = solve_joltage(target_joltage, buttons)
            if presses is not None:
                total += presses
    
    return total


def main():
    import sys
    # Read input
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    data = read_input(filename)
    
    # Solve parts
    result1 = part1(data)
    print(f"Part 1: {result1}")
    
    result2 = part2(data)
    if result2 is not None:
        print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
