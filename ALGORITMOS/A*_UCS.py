import heapq, math
from time import perf_counter

# ====== Config ======
ALLOW_CORNER_CUTTING = False  # Cambia a True para permitir cortar esquinas

# ====== Laberinto ======
maze = [
    [0,0,0,0,0,0,0],
    [0,1,1,1,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,1,0,0,0],
    [0,0,0,1,0,1,0],
    [1,1,0,0,0,0,0],
]
start, goal = (0,0), (5,6)

# Direcciones (8 movimientos posibles)
ALLDIRS = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

def in_bounds(x,y):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0])

def free(x,y):
    return maze[x][y] == 0

def step_cost(dx, dy):
    return math.sqrt(2) if dx != 0 and dy != 0 else 1.0

def can_move(x, y, dx, dy, allow_corner_cutting=ALLOW_CORNER_CUTTING):
    nx, ny = x + dx, y + dy
    if not (in_bounds(nx, ny) and free(nx, ny)):
        return False
    # Si es diagonal y no permitimos cortar esquinas, exige que ambas ortogonales estén libres
    if not allow_corner_cutting and dx != 0 and dy != 0:
        if not (free(x + dx, y) and free(x, y + dy)):
            return False
    return True

def neighbors8_weighted(x,y, allow_corner_cutting=ALLOW_CORNER_CUTTING):
    for dx,dy in ALLDIRS:
        if can_move(x, y, dx, dy, allow_corner_cutting):
            yield (x+dx, y+dy), step_cost(dx, dy)

# ====== Utilidades ======
def path_cost(path):
    if not path:
        return None
    total = 0.0
    for (x1,y1), (x2,y2) in zip(path, path[1:]):
        total += step_cost(x2-x1, y2-y1)
    return total

def draw_path(path):
    chars = [['·' if cell==0 else '█' for cell in row] for row in maze]
    if path:
        for (x,y) in path[1:-1]:
            chars[x][y] = '*'
        sx,sy = path[0]; gx,gy = path[-1]
        chars[sx][sy] = 'S'; chars[gx][gy] = 'G'
    for row in chars:
        print(' '.join(row))

# ====== Algoritmos ======
# UCS / Dijkstra (óptimo en coste con pesos positivos)
def ucs8_path(s,t):
    pq = [(0.0, s)]
    prev = {s: None}
    bestg = {s: 0.0}
    while pq:
        g, u = heapq.heappop(pq)
        if u == t:
            break
        if g > bestg.get(u, float('inf')):
            continue
        x, y = u
        for (v), c in neighbors8_weighted(x, y):
            ng = g + c
            if ng < bestg.get(v, float('inf')):
                bestg[v] = ng
                prev[v] = u
                heapq.heappush(pq, (ng, v))
    if t not in prev:
        return None, float('inf')
    # reconstrucción
    path = []
    cur = t
    while cur is not None:
        path.append(cur); cur = prev[cur]
    path.reverse()
    return path, bestg[t]

# DFS (no óptimo, pero ahora devolvemos coste real del camino hallado)
def dfs8_path(s, t):
    stack = [s]; prev = {s: None}; seen = set()
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        if u == t:
            break
        x, y = u
        for (v), _c in neighbors8_weighted(x, y):
            if v not in seen and v not in prev:
                prev[v] = u
                stack.append(v)
    if t not in prev:
        return None, float('inf')
    path = []
    cur = t
    while cur is not None:
        path.append(cur); cur = prev[cur]
    path.reverse()
    return path, path_cost(path)

# A* 8-dir con heurística octile (admisible para 1/√2)
def octile(a,b):
    dx, dy = abs(a[0]-b[0]), abs(a[1]-b[1])
    return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)

def astar8_weighted_path(s,t):
    pq = []
    heapq.heappush(pq, (octile(s,t), 0.0, s))
    prev = {s: None}
    bestg = {s: 0.0}
    while pq:
        f, g, u = heapq.heappop(pq)
        if u == t:
            break
        if g > bestg.get(u, float('inf')):
            continue
        x, y = u
        for (v), c in neighbors8_weighted(x, y):
            ng = g + c
            if ng < bestg.get(v, float('inf')):
                bestg[v] = ng
                prev[v] = u
                heapq.heappush(pq, (ng + octile(v, t), ng, v))
    if t not in prev:
        return None, float('inf')
    path = []
    cur = t
    while cur is not None:
        path.append(cur); cur = prev[cur]
    path.reverse()
    return path, bestg[t]

# ====== Benchmark ======
def bench(fn, name):
    t0 = perf_counter()
    path, cost = fn(start, goal)
    t1 = perf_counter()
    cc = "ON" if ALLOW_CORNER_CUTTING else "OFF"
    cost_str = f"{cost:.3f}" if cost not in (None, float('inf')) else str(cost)
    print(f"{name} | corner-cutting={cc} -> tiempo={t1-t0:.6f}s | coste={cost_str} | {'ENCONTRÓ' if path else 'SIN CAMINO'}")
    return path, cost

# ====== Ejecución ======
if __name__ == "__main__":
    p_ucs, c_ucs = bench(ucs8_path,            "UCS (Dijkstra 8-dir)")
    p_dfs, c_dfs = bench(dfs8_path,            "DFS 8-dir (no óptimo)")
    p_ast, c_ast = bench(astar8_weighted_path, "A* 8-dir (octile)")

    print("\nCamino UCS:")
    draw_path(p_ucs)
    print("\nCamino DFS:")
    draw_path(p_dfs)
    print("\nCamino A*:")
    draw_path(p_ast)