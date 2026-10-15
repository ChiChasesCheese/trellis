"""LC 547 Number of Provinces -- union-find over the adjacency matrix; components = n - successful unions."""
from random import Random

# --- solution ---
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]     # path halving: point at the grandparent
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                                     # already connected: this edge would close a cycle
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra                                 # union by size: the small tree hangs under the big one
        self.size[ra] += self.size[rb]
        return True


def find_circle_num(is_connected):
    n = len(is_connected)
    dsu, components = DSU(n), n
    for i in range(n):
        for j in range(i + 1, n):                            # the matrix is symmetric: look at one triangle
            if is_connected[i][j] and dsu.union(i, j):
                components -= 1
    return components
# --- end ---

def _brute(m):
    n, seen, count = len(m), set(), 0
    for s in range(n):
        if s in seen:
            continue
        count += 1
        stack = [s]
        seen.add(s)
        while stack:
            u = stack.pop()
            for v in range(n):
                if m[u][v] and v not in seen:
                    seen.add(v)
                    stack.append(v)
    return count

if __name__ == "__main__":
    assert find_circle_num([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
    assert find_circle_num([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
    assert find_circle_num([[1]]) == 1
    rng = Random(41)
    for _ in range(400):
        n = rng.randint(1, 9)
        m = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for _ in range(rng.randint(0, n)):
            a, b = rng.randrange(n), rng.randrange(n)
            m[a][b] = m[b][a] = 1
        assert find_circle_num(m) == _brute(m), m
    print("ok 547_number_of_provinces")
