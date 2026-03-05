import heapq, math
from time import perf_counter

# ====== Config ======
ALLOW_CORNER_CUTTING = False   # True permite cortar esquinas; False lo prohíbe
SHOW_TRACE = True              # Muestra traza detallada de UCS
SHOW_BEST_TREE = True          # Muestra árbol ASCII de mejores transiciones
MAX_TREE_NODES = 200           # Límite de nodos a imprimir en el árbol

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

# Direcciones (8 movimientos)
ALLDIRS = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

# ====== Utilidades de grid ======
def in_bounds(x,y):  return 0 <= x < len(maze) and 0 <= y < len(maze[0])
def free(x,y):       return maze[x][y] == 0
def step_cost(dx, dy): return math.sqrt(2) if dx != 0 and dy != 0 else 1.0

def can_move(x, y, dx, dy, allow_corner_cutting=ALLOW_CORNER_CUTTING):
    nx, ny = x + dx, y + dy
    if not (in_bounds(nx, ny) and free(nx, ny)):
        return False
    # Si es diagonal y NO permitimos cortar esquinas
    if not allow_corner_cutting and dx != 0 and dy != 0:
        if not (free(x + dx, y) and free(x, y + dy)):
            return False
    return True

def neighbors8_weighted(x,y, allow_corner_cutting=ALLOW_CORNER_CUTTING):
    for dx,dy in ALLDIRS:
        if can_move(x, y, dx, dy, allow_corner_cutting):
            yield (x+dx, y+dy), step_cost(dx, dy)

# ====== Dibujar camino ======
def draw_path(path):
    chars = [['·' if cell==0 else '█' for cell in row] for row in maze]
    if path:
        for (x,y) in path[1:-1]:
            chars[x][y] = '*'
        sx,sy = path[0]; gx,gy = path[-1]
        chars[sx][sy] = 'S'; chars[gx][gy] = 'G'
    for row in chars:
        print(' '.join(row))

# ====== Traza y Árbol ======
def fmt(n): return f"({n[0]},{n[1]})"

def print_frontier(pq, limit=10):
    # Copia ordenada por coste para visualizar
    tmp = sorted(pq)
    items = [f"{fmt(n)}:g={g:.3f}" for (g,n) in tmp[:limit]]
    more = " ..." if len(tmp) > limit else ""
    print("    FRONTERA:", ", ".join(items) + more)

def print_children(children):
    if not children:
        print("    (sin vecinos válidos)")
    else:
        for (v,c,ng) in children:
            print(f"    -> {fmt(v)}  c={c:.3f}  g'={ng:.3f}")

def build_children_map(prev):
    """Construye un mapa padre -> [hijos] a partir de prev (padre óptimo)."""
    children_map = {}
    for node, parent in prev.items():
        if parent is None:
            continue
        children_map.setdefault(parent, []).append(node)
    return children_map

def print_tree_ascii(root, children_map, bestg):
    """Imprime árbol ASCII de mejores transiciones (prev), ordenando por g."""
    print("\nÁRBOL DE MEJORES TRANSICIONES (prev):")
    visited = set()
    count = 0
    def dfs(u, indent=""):
        nonlocal count
        if count >= MAX_TREE_NODES:
            print(indent + "… (límite de impresión alcanzado)");
            return
        count += 1
        print(f"{indent}• {fmt(u)}  g={bestg.get(u,float('inf')):.3f}")
        visited.add(u)
        for v in sorted(children_map.get(u, []), key=lambda n: bestg.get(n,float('inf'))):
            dfs(v, indent + "   ")
    dfs(root)
    print(f"(nodos impresos: {min(count, MAX_TREE_NODES)})\n")

# ====== UCS / Dijkstra con traza ======
def ucs8_path_with_trace(s,t):
    pq = [(0.0, s)]           # (g, nodo)
    prev = {s: None}
    bestg = {s: 0.0}
    expanded = 0

    if SHOW_TRACE:
        print("=== TRAZA UCS (Dijkstra) ===")

    while pq:
        g, u = heapq.heappop(pq)
        # Ignora entradas obsoletas
        if g > bestg.get(u, float('inf')):
            continue

        expanded += 1
        if SHOW_TRACE:
            print(f"\nPaso {expanded}: expandiendo {fmt(u)} con g={g:.3f}")

        # Si llegamos al objetivo, paramos
        if u == t:
            if SHOW_TRACE:
                print("   Objetivo alcanzado. Se detiene la expansión.")
            break

        # Generar vecinos válidos
        x, y = u
        children_info = []
        for (v), c in neighbors8_weighted(x, y):
            ng = g + c
            # Relajación (mejor g encontrado)
            if ng < bestg.get(v, float('inf')):
                bestg[v] = ng
                prev[v] = u
                heapq.heappush(pq, (ng, v))
                children_info.append((v, c, ng))
        if SHOW_TRACE:
            print_children(children_info)
            print_frontier(pq, limit=12)

    # Reconstrucción del camino
    if t not in prev:
        return None, float('inf'), prev, bestg

    path = []
    cur = t
    while cur is not None:
        path.append(cur); cur = prev[cur]
    path.reverse()
    return path, bestg[t], prev, bestg

# ====== A* (para comparar al final si quieres) ======
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
        if g > bestg.get(u, float('inf')):
            continue
        if u == t:
            break
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

# ====== Ejecución ======
if __name__ == "__main__":
    cc = "ON" if ALLOW_CORNER_CUTTING else "OFF"
    print(f"corner-cutting={cc}\n")

    t0 = perf_counter()
    path, cost, prev, bestg = ucs8_path_with_trace(start, goal)
    t1 = perf_counter()

    # Árbol de mejores transiciones (prev)
    if SHOW_BEST_TREE and prev:
        children_map = build_children_map(prev)
        print_tree_ascii(start, children_map, bestg)

    # Resultados finales UCS
    print("=== RESULTADOS UCS ===")
    print(f"Coste total: {cost:.3f}")
    print(f"Tiempo: {t1 - t0:.6f}s")
    print("\nCamino UCS:")
    draw_path(path)

    # (Opcional) Comparar con A*
    # p_ast, c_ast = astar8_weighted_path(start, goal)
    # print("\nA* (octile) -> coste:", round(c_ast,3))