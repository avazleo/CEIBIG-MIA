from collections import deque

graph = {
    'S': ['A', 'B'],
    'A': ['C', 'D'],
    'B': ['E'],
    'C': [],
    'D': ['F'],
    'E': ['F'],
    'F': []
}

def bfs_order(graph, start):
    visited, order = set(), []
    q = deque([start])
    while q:
        u = q.popleft()
        if u in visited:
            continue
        visited.add(u)
        order.append(u)
        for v in graph.get(u, []):
            if v not in visited:
                q.append(v)
    return order

def dfs_order(graph, start):
    visited, order = set(), []
    def dfs(u):
        visited.add(u)
        order.append(u)
        for v in graph.get(u, []):
            if v not in visited:
                dfs(v)
    dfs(start)
    return order

print("BFS:", bfs_order(graph, 'S'))  # Ej. posible: ['S','A','B','C','D','E','F']
print("DFS:", dfs_order(graph, 'S'))  # Ej. posible: ['S','A','C','D','F','B','E']