#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 12: Christmas Tree Farm
Polyomino bin packing with rotation/flip
"""
import sys


def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().strip()


def parse_shape(lines):
    """Parse a shape into a frozenset of (row, col) coordinates for '#' cells."""
    coords = set()
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == '#':
                coords.add((r, c))
    return normalize_shape(coords)


def normalize_shape(coords):
    """Normalize shape so min row and col are 0."""
    if not coords:
        return frozenset()
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return frozenset((r - min_r, c - min_c) for r, c in coords)


def rotate_90(coords):
    """Rotate coordinates 90 degrees clockwise."""
    return normalize_shape({(c, -r) for r, c in coords})


def flip_horizontal(coords):
    """Flip coordinates horizontally."""
    return normalize_shape({(r, -c) for r, c in coords})


def generate_orientations(shape):
    """Generate all unique orientations of a shape (up to 8: 4 rotations × 2 flips)."""
    orientations = set()
    current = shape
    
    for _ in range(4):
        orientations.add(current)
        current = rotate_90(current)
    
    flipped = flip_horizontal(shape)
    for _ in range(4):
        orientations.add(flipped)
        flipped = rotate_90(flipped)
    
    return list(orientations)


def parse_input(data):
    """Parse the input data into shapes and regions."""
    lines = data.split('\n')
    
    shapes = []
    regions = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Shape definition: "N:" followed by grid lines
        if line and line[0].isdigit() and line.endswith(':'):
            shape_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip()[0].isdigit():
                shape_lines.append(lines[i])
                i += 1
            shapes.append(parse_shape(shape_lines))
        # Region definition: "WxH: counts..."
        elif line and 'x' in line and ':' in line:
            parts = line.split(':')
            dims = parts[0].strip()
            counts = list(map(int, parts[1].strip().split()))
            w, h = map(int, dims.split('x'))
            regions.append((w, h, counts))
            i += 1
        else:
            i += 1
    
    return shapes, regions


def can_fit_presents(shapes, presents, width, height):
    """Fast backtracking using bitmask with forward checking."""
    if not presents:
        return True
    
    # Quick area check
    total_cells_needed = sum(len(shapes[p]) for p in presents)
    if total_cells_needed > width * height:
        return False
    
    # Pre-compute all placements as bitmasks for each present instance
    placements_by_present = [[] for _ in presents]
    
    for list_idx, present_idx in enumerate(presents):
        shape = shapes[present_idx]
        orients = generate_orientations(shape)
        seen = set()
        for orient in orients:
            max_r = max(r for r, c in orient)
            max_c = max(c for r, c in orient)
            for sr in range(height - max_r):
                for sc in range(width - max_c):
                    mask = 0
                    for r, c in orient:
                        mask |= 1 << ((sr + r) * width + (sc + c))
                    if mask not in seen:
                        seen.add(mask)
                        placements_by_present[list_idx].append(mask)
    
    # Sort presents by number of placements (fewest first = MRV)
    order = sorted(range(len(presents)), key=lambda i: len(placements_by_present[i]))
    
    # Forward checking: filter valid placements for remaining presents
    def backtrack(idx, grid_mask, remaining_placements):
        if idx == len(order):
            return True
        
        present_idx = order[idx]
        valid = [m for m in remaining_placements[present_idx] if not (grid_mask & m)]
        
        if not valid:
            return False
        
        for mask in valid:
            new_grid = grid_mask | mask
            
            # Forward check: ensure all remaining presents still have valid placements
            new_remaining = []
            dead_end = False
            for i in range(idx + 1, len(order)):
                p = order[i]
                filtered = [m for m in remaining_placements[p] if not (new_grid & m)]
                if not filtered:
                    dead_end = True
                    break
                new_remaining.append(filtered)
            
            if dead_end:
                continue
                
            # Build new remaining dict
            new_rem_dict = {order[i]: new_remaining[i - idx - 1] for i in range(idx + 1, len(order))}
            
            if backtrack(idx + 1, new_grid, new_rem_dict):
                return True
        
        return False
    
    initial_remaining = {i: placements_by_present[i] for i in range(len(presents))}
    return backtrack(0, 0, initial_remaining)


def part1(data):
    """Solve part 1."""
    shapes, regions = parse_input(data)
    
    count = 0
    for width, height, counts in regions:
        # Build list of presents to place
        presents = []
        for shape_idx, cnt in enumerate(counts):
            presents.extend([shape_idx] * cnt)
        
        if can_fit_presents(shapes, presents, width, height):
            count += 1
    
    return count


def part2(data):
    """Solve part 2."""
    shapes, regions = parse_input(data)
    # TODO: Implement solution
    return None


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    data = read_input(filename)
    
    result1 = part1(data)
    print(f"Part 1: {result1}")
    
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
