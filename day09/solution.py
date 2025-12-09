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



def get_polygon_edges(tiles):
    """Get all edges of the polygon formed by connecting consecutive red tiles."""
    edges = []
    for i in range(len(tiles)):
        p1 = tiles[i]
        p2 = tiles[(i + 1) % len(tiles)]
        edges.append((p1, p2))
    return edges


def point_on_segment(px, py, x1, y1, x2, y2):
    """Check if point (px, py) is on segment from (x1, y1) to (x2, y2)."""
    if x1 == x2:  # Vertical segment
        if px == x1 and min(y1, y2) <= py <= max(y1, y2):
            return True
    else:  # Horizontal segment
        if py == y1 and min(x1, x2) <= px <= max(x1, x2):
            return True
    return False


def point_on_boundary(px, py, edges):
    """Check if a point is on the polygon boundary."""
    for (x1, y1), (x2, y2) in edges:
        if point_on_segment(px, py, x1, y1, x2, y2):
            return True
    return False


def point_inside_polygon(px, py, edges):
    """Check if a point is strictly inside the polygon using ray casting."""
    # Cast ray to the right, count crossings
    crossings = 0
    
    for (x1, y1), (x2, y2) in edges:
        if x1 == x2:
            # Vertical segment - can cross our horizontal ray
            if x1 > px:  # Segment is to the right
                min_y, max_y = min(y1, y2), max(y1, y2)
                if min_y < py < max_y:  # Ray passes through (not touching endpoints)
                    crossings += 1
                elif py == min_y or py == max_y:
                    # Ray touches an endpoint - count as 0.5 to handle corners
                    crossings += 0.5
    
    return crossings % 2 == 1


def point_inside_or_on_boundary(px, py, edges):
    """Check if point is inside or on the boundary of the polygon."""
    if point_on_boundary(px, py, edges):
        return True
    return point_inside_polygon(px, py, edges)


def segment_inside_polygon(x1, y1, x2, y2, edges):
    """Check if a horizontal or vertical segment is entirely inside or on the polygon."""
    # Both endpoints must be inside or on boundary
    if not point_inside_or_on_boundary(x1, y1, edges):
        return False
    if not point_inside_or_on_boundary(x2, y2, edges):
        return False
    
    # Check if segment crosses any boundary edge (going outside and back in)
    if x1 == x2:  # Vertical segment
        seg_x = x1
        seg_min_y, seg_max_y = min(y1, y2), max(y1, y2)
        
        for (ex1, ey1), (ex2, ey2) in edges:
            if ey1 == ey2:  # Horizontal edge
                edge_y = ey1
                if seg_min_y < edge_y < seg_max_y:
                    # Check if edge crosses our segment
                    edge_min_x, edge_max_x = min(ex1, ex2), max(ex1, ex2)
                    if edge_min_x < seg_x < edge_max_x:
                        return False
    else:  # Horizontal segment
        seg_y = y1
        seg_min_x, seg_max_x = min(x1, x2), max(x1, x2)
        
        for (ex1, ey1), (ex2, ey2) in edges:
            if ex1 == ex2:  # Vertical edge
                edge_x = ex1
                if seg_min_x < edge_x < seg_max_x:
                    # Check if edge crosses our segment
                    edge_min_y, edge_max_y = min(ey1, ey2), max(ey1, ey2)
                    if edge_min_y < seg_y < edge_max_y:
                        return False
    
    return True


def rectangle_inside_polygon(min_x, min_y, max_x, max_y, edges):
    """Check if entire rectangle is inside or on boundary of polygon."""
    # Check all 4 corners
    corners = [(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)]
    for cx, cy in corners:
        if not point_inside_or_on_boundary(cx, cy, edges):
            return False
    
    # Check all 4 edges of the rectangle
    # Top edge
    if not segment_inside_polygon(min_x, max_y, max_x, max_y, edges):
        return False
    # Bottom edge
    if not segment_inside_polygon(min_x, min_y, max_x, min_y, edges):
        return False
    # Left edge
    if not segment_inside_polygon(min_x, min_y, min_x, max_y, edges):
        return False
    # Right edge
    if not segment_inside_polygon(max_x, min_y, max_x, max_y, edges):
        return False
    
    # Check that no polygon edge passes through the interior of the rectangle
    for (ex1, ey1), (ex2, ey2) in edges:
        if ex1 == ex2:  # Vertical edge
            edge_x = ex1
            if min_x < edge_x < max_x:
                edge_min_y, edge_max_y = min(ey1, ey2), max(ey1, ey2)
                # Check if this vertical edge passes through the rectangle interior
                if edge_min_y < max_y and edge_max_y > min_y:
                    # The edge intersects the rectangle's y range
                    # Check if it actually passes through interior (not just touching)
                    if edge_min_y < max_y and edge_max_y > min_y:
                        # If any part of the edge is strictly inside the rectangle's interior
                        if not (edge_max_y <= min_y or edge_min_y >= max_y):
                            return False
        else:  # Horizontal edge
            edge_y = ey1
            if min_y < edge_y < max_y:
                edge_min_x, edge_max_x = min(ex1, ex2), max(ex1, ex2)
                # Check if this horizontal edge passes through the rectangle interior
                if edge_min_x < max_x and edge_max_x > min_x:
                    if not (edge_max_x <= min_x or edge_min_x >= max_x):
                        return False
    
    return True


def part2(data):
    """Find largest rectangle using only red and green tiles."""
    tiles = parse_input(data)
    edges = get_polygon_edges(tiles)
    
    max_area = 0
    
    # Try all pairs of red tiles as opposite corners
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]
            
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            
            if rectangle_inside_polygon(min_x, min_y, max_x, max_y, edges):
                area = calculate_area(tiles[i], tiles[j])
                max_area = max(max_area, area)
    
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
