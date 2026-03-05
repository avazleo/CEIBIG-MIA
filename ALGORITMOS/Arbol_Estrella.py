import heapq
from math import sqrt

# 0 = libre, 1 = obstáculo
grid = [
    [0,0,0,0,0],
    [0,1,1,1,0],
    [0,0,0,1,0],
    [1,0,0,0,0]
]

DIRS = [(1,0),(-1,0),(0,1),(0,-1), (1,1),(1,-1),(-1,1),(-1,-1)]
MOVE_COST = {(1,0):1,(-1,0):1,(0,1):1,(0,-1):1,(1,1):sqrt(2),(1,-1):sqrt(2),(-1,1):sqrt(2),(-1,-1):sqrt(2)}

def in_bounds(x, y, grid):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

def passable(x, y, grid):
    return grid[x][y] == 0

def octile(a, b):
    dx, dy = abs(a[0]-b[0]), abs(a[1]-b[1])
    return (dx + dy) + (sqrt(2) - 2) * min(dx, dy)

def astar8(start, goal, grid, h=octile):
    open_set = []
    heapq.heappush(open_set, (h(start, goal), 0, start, []))
    best_g = {start: 0}
    visited = set()

    while open_set:
        f, g, node, path = heapq.heappop(open_set)
        if node == goal:
            return path + [node]
        if node in visited:
            continue
        visited.add(node)

        x, y = node
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if not in_bounds(nx, ny, grid) or not passable(nx, ny, grid):
                continue
            ng = g + MOVE_COST[(dx, dy)]
            if ng < best_g.get((nx, ny), float('inf')):
                best_g[(nx, ny)] = ng
                heapq.heappush(open_set, (ng + h((nx, ny), goal), ng, (nx, ny), path + [node]))

    return None

print(astar8((0,0), (3,4), grid))