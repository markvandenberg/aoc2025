#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 9: Movie Theater
"""

def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().strip()


def parse_input(data):
    """Parse red tile positions."""
    lines = data.split('\n')
    tiles = []
    for line in lines:
        if line.strip():
            x, y = map(int, line.split(','))
            tiles.append((x, y))
    return tiles


def calculate_area(p1, p2):
    """Calculate area of rectangle with opposite corners at p1 and p2."""
    x1, y1 = p1
    x2, y2 = p2
    # Add 1 because we want to include both endpoints
    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1
    return width * height


def part1(data):
    """Find largest rectangle using two red tiles as opposite corners."""
    tiles = parse_input(data)
    
    max_area = 0
    
    # Try all pairs of tiles as opposite corners
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            area = calculate_area(tiles[i], tiles[j])
            max_area = max(max_area, area)
    
    return max_area


def get_edge_tiles(red_tiles):
    """Get tiles on edges between consecutive red tiles."""
    edge_tiles = set()
    
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % len(red_tiles)]
        
        # Add all tiles between these two red tiles
        if x1 == x2:  # Same column, vertical line
            min_y, max_y = min(y1, y2), max(y1, y2)
            for y in range(min_y, max_y + 1):
                edge_tiles.add((x1, y))
        elif y1 == y2:  # Same row, horizontal line
            min_x, max_x = min(x1, x2), max(x1, x2)
            for x in range(min_x, max_x + 1):
                edge_tiles.add((x, y1))
    
    return edge_tiles


def is_inside_polygon(x, y, polygon):
    """Check if point (x, y) is inside polygon using ray casting algorithm."""
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        
        p1x, p1y = p2x, p2y
    
    return inside


def is_tile_green(x, y, red_tiles_set, edge_tiles_set, red_tiles_list):
    """Check if a tile is green (on edge or inside polygon)."""
    if (x, y) in red_tiles_set:
        return False
    if (x, y) in edge_tiles_set:
        return True
    return is_inside_polygon(x, y, red_tiles_list)


def rectangle_contains_only_red_or_green(p1, p2, red_tiles_set, edge_tiles_set, red_tiles_list):
    """Check if rectangle from p1 to p2 contains only red or green tiles."""
    x1, y1 = p1
    x2, y2 = p2
    
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)
    
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) not in red_tiles_set:
                if not is_tile_green(x, y, red_tiles_set, edge_tiles_set, red_tiles_list):
                    return False
    
    return True


def part2(data):
    """Find largest rectangle using only red and green tiles."""
    tiles = parse_input(data)
    red_tiles_set = set(tiles)
    
    def rectangle_fully_inside(x1, y1, x2, y2):
        """Check if rectangle is fully inside by testing only corners."""
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        
        # Check all 4 corners
        corners = [
            (min_x, min_y), (min_x, max_y),
            (max_x, min_y), (max_x, max_y)
        ]
        
        for x, y in corners:
            if (x, y) not in red_tiles_set and not is_inside_polygon(x, y, tiles):
                return False
        return True
    
    max_area = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]
            
            if rectangle_fully_inside(x1, y1, x2, y2):
                area = calculate_area((x1, y1), (x2, y2))
                if area > max_area:
                    max_area = area
    
    return max_area


def main():
    import sys
    # Read input (use command line argument if provided, otherwise default to input.txt)
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    data = read_input(filename)
    
    # Solve parts
    result1 = part1(data)
    print(f"Part 1: {result1}")
    
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
