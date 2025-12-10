#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 10: Factory
"""
import re

def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().strip()


def parse_machine(line):
    """Parse a machine specification line."""
    # Extract the indicator light pattern
    lights_match = re.search(r'\[([.#]+)\]', line)
    lights = lights_match.group(1)
    target = [1 if c == '#' else 0 for c in lights]
    
    # Extract button wirings
    buttons = []
    for match in re.finditer(r'\(([0-9,]+)\)', line):
        button_lights = [int(x) for x in match.group(1).split(',')]
        buttons.append(button_lights)
    
    return target, buttons


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
            target, buttons = parse_machine(line)
            presses = solve_machine(target, buttons)
            if presses is not None:
                total += presses
    
    return total


def part2(data):
    """Solve part 2."""
    # TODO: Implement when part 2 is revealed
    return None


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
