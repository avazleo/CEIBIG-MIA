from time import perf_counter
from collections import deque
import math, heapq

maze = [
    [0,0,0,0,0,0,0],
    [0,1,1,1,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,0,1,0,0,0],
    [0,0,0,1,0,1,0],
    [1,1,0,0,0,0,0],
]
start, goal = (0,0), (5,6)

ORTHO = [(1,0),(-1,0),(0,1),(0,-1)]
ALLDIRS = ORTHO + [(1,1),(1,-1),(-1,1),(-1,-1)]

def neighbors4(x,y):
    for dx,dy in ORTHO:
        nx,ny = x+dx, y+dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny]==0:
            yield (nx,ny)

def neighbors8(x,y):
    for dx,dy in ALLDIRS:
        nx,ny = x+dx, y+dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny]==0:
            yield (nx,ny), (math.sqrt(2) if dx!=0 and dy!=0 else 1)

def bfs_path(s, t):
    q = deque([s]); prev = {s: None}; seen={s}
    while q:
        u = q.popleft()
        if u == t:
            break
        for v in neighbors4(*u):
            if v not in seen:
                seen.add(v); prev[v]=u; q.append(v)
    if t not in prev: return None
    path=[]; cur=t
    while cur is not None: path.append(cur); cur=prev[cur]
    path.reverse()
    return path

def dfs_path(s, t):
    stack=[s]; prev={s:None}; seen=set()
    while stack:
        u=stack.pop()
        if u in seen: continue
        seen.add(u)
        if u==t: break
        for v in neighbors4(*u):
            if v not in seen and v not in prev:
                prev[v]=u; stack.append(v)
    if t not in prev: return None
    path=[]; cur=t
    while cur is not None: path.append(cur); cur=prev[cur]
    path.reverse()
    return path

def octile(a,b):
    dx,dy=abs(a[0]-b[0]),abs(a[1]-b[1])
    return (dx+dy)+(math.sqrt(2)-2)*min(dx,dy)

def astar8_path(s,t):
    pq=[]; heapq.heappush(pq,(octile(s,t),0,s))
    prev={s:None}; bestg={s:0}
    while pq:
        f,g,u=heapq.heappop(pq)
        if u==t: break
        for (v),c in neighbors8(*u):
            ng=g+c
            if ng<bestg.get(v,float('inf')):
                bestg[v]=ng; prev[v]=u
                heapq.heappush(pq,(ng+octile(v,t),ng,v))
    if t not in prev: return None
    path=[]; cur=t
    while cur is not None: path.append(cur); cur=prev[cur]
    path.reverse()
    return path

def bench(fn):
    t0=perf_counter(); p=fn(start, goal); t1=perf_counter()
    length = None
    if p:
        # longitud "pasos" (ortogonales) o nodos; para A* con diagonales puedes sumar coste real si quieres
        length = len(p)-1
    return p, (t1-t0), length

for name, fn in [("BFS", bfs_path), ("DFS", dfs_path), ("A* (8-dir)", astar8_path)]:
    path, dt, L = bench(fn)
    print(f"{name}: tiempo={dt:.6f}s | pasos={L} | {'ENCONTRÓ' if path else 'SIN CAMINO'}")