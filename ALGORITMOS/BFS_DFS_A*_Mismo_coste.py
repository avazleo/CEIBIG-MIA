from collections import deque
import heapq
from time import perf_counter

# ====== Config ======
ALLOW_CORNER_CUTTING = False  # ← Cambia a True si quieres permitir cortar esquinas

# ====== Laberinto y utilidades ======
maze = [
    [0,0,0,0,0,0,0],
    [0,1,1,1,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,1,0,0,0],
    [0,0,0,1,0,1,0],
    [1,1,0,0,0,0,0],
]
start, goal = (0,0), (5,6)

ALLDIRS = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

def in_bounds(x,y):
    return 0 <= x < len(maze) and 0 <= y < len(maze[0])

def free(x,y):
    return maze[x][y] == 0

def can_move(x, y, dx, dy, allow_corner_cutting=ALLOW_CORNER_CUTTING):
    """Comprueba si se puede ir de (x,y) a (x+dx,y+dy) con reglas de esquina."""
    nx, ny = x + dx, y + dy
    if not (in_bounds(nx, ny) and free(nx, ny)):
        return False
    # Si es movimiento diagonal y NO permitimos cortar esquinas:
    if not allow_corner_cutting and dx != 0 and dy != 0:
        # Requerimos que las ortogonales adyacentes también sean libres
        # (evita pasar "entre" dos muros pegados)
        if not (free(x + dx, y) and free(x, y + dy)):
            return False
    return True

def neighbors8_unweighted(x,y, allow_corner_cutting=ALLOW_CORNER_CUTTING):
    for dx,dy in ALLDIRS:
        if can_move(x, y, dx, dy, allow_corner_cutting):
            yield (x+dx, y+dy)

# ====== Algoritmos ======
# BFS 8-dir (óptimo en nº de pasos con coste uniforme)
def bfs8_path(s, t):
    q = deque([s]); prev = {s: None}; seen={s}
    while q:
        u = q.popleft()
        if u == t: break
        for v in neighbors8_unweighted(*u):
            if v not in seen:
                seen.add(v); prev[v]=u; q.append(v)
    if t not in prev: return None
    path=[]; cur=t
    while cur is not None:
        path.append(cur); cur=prev[cur]
    path.reverse(); return path

# DFS 8-dir (no garantiza óptimo)
def dfs8_path(s, t):
    stack=[s]; prev={s:None}; seen=set()
    while stack:
        u=stack.pop()
        if u in seen: continue
        seen.add(u)
        if u==t: break
        for v in neighbors8_unweighted(*u):
            if v not in seen and v not in prev:
                prev[v]=u; stack.append(v)
    if t not in prev: return None
    path=[]; cur=t
    while cur is not None:
        path.append(cur); cur=prev[cur]
    path.reverse(); return path

# A* 8-dir con Chebyshev (admisible para coste uniforme)
def chebyshev(a,b):
    dx,dy = abs(a[0]-b[0]), abs(a[1]-b[1])
    return max(dx,dy)

def astar8_uniform_path(s,t):
    pq=[]; heapq.heappush(pq,(chebyshev(s,t),0,s))
    prev={s:None}; bestg={s:0}
    while pq:
        f,g,u=heapq.heappop(pq)
        if u==t: break
        for v in neighbors8_unweighted(*u):
            ng=g+1
            if ng < bestg.get(v, float('inf')):
                bestg[v]=ng; prev[v]=u
                heapq.heappush(pq,(ng+chebyshev(v,t), ng, v))
    if t not in prev: return None
    path=[]; cur=t
    while cur is not None:
        path.append(cur); cur=prev[cur]
    path.reverse(); return path

# ====== Utilidad para imprimir el camino ======
def draw_path(path):
    chars = [['·' if cell==0 else '█' for cell in row] for row in maze]
    if path:
        for (x,y) in path[1:-1]:
            chars[x][y] = '*'
        sx,sy = path[0]; gx,gy = path[-1]
        chars[sx][sy] = 'S'; chars[gx][gy] = 'G'
    for row in chars:
        print(' '.join(row))

# ====== Benchmark sencillo y ejecución ======
def bench(fn, name):
    t0 = perf_counter()
    p = fn(start, goal)
    t1 = perf_counter()
    steps = (len(p)-1) if p else None
    cc = "ON" if ALLOW_CORNER_CUTTING else "OFF"
    print(f"{name} | corner-cutting={cc} -> tiempo={t1-t0:.6f}s | pasos={steps} | {'ENCONTRÓ' if p else 'SIN CAMINO'}")
    return p

if __name__ == "__main__":
    p_bfs = bench(bfs8_path, "BFS 8-dir (uniforme)")
    p_dfs = bench(dfs8_path, "DFS 8-dir (uniforme)")
    p_ast = bench(astar8_uniform_path, "A* 8-dir (uniforme, Chebyshev)")

    print("\nCamino BFS:")
    draw_path(p_bfs)
    print("\nCamino DFS:")
    draw_path(p_dfs)
    print("\nCamino A*:")
    draw_path(p_ast)