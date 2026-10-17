"""LC 399 with caching -- BFS evaluator with a result cache; a new equation drops only the cached MISSES (-1), found ratios never change."""
from collections import deque
from random import Random

# --- solution ---
class Division:
    def __init__(self):
        self.graph = {}                                   # a -> [(b, a/b)]
        self.cache = {}                                   # (x, y) -> x / y, or -1.0 for "unknown"
        self.bfs_runs = 0

    def add_equation(self, a, b, v):                      # a / b == v
        self.graph.setdefault(a, []).append((b, v))
        self.graph.setdefault(b, []).append((a, 1 / v))
        # a found ratio is a consequence of old equations, so it stays true; only "unknown" can become known
        self.cache = {k: r for k, r in self.cache.items() if r != -1.0}

    def query(self, x, y):
        if (x, y) in self.cache:
            return self.cache[(x, y)]
        ans = self._bfs(x, y)
        self.cache[(x, y)] = ans
        if ans != -1.0 and ans != 0:
            self.cache[(y, x)] = 1 / ans                  # the reverse query is free
        return ans

    def _bfs(self, x, y):
        self.bfs_runs += 1
        if x not in self.graph or y not in self.graph:
            return -1.0
        seen, queue = {x: 1.0}, deque([x])                # seen[w] = x / w
        while queue:
            u = queue.popleft()
            for w, f in self.graph[u]:                    # u / w == f
                if w not in seen:
                    seen[w] = seen[u] * f
                    queue.append(w)
        return seen.get(y, -1.0)
# --- end ---

if __name__ == "__main__":
    d = Division()
    d.add_equation("a", "b", 2.0)
    d.add_equation("b", "c", 3.0)
    assert d.query("a", "c") == 6.0 and d.bfs_runs == 1
    assert d.query("a", "c") == 6.0 and abs(d.query("c", "a") - 1 / 6) < 1e-12 and d.bfs_runs == 1   # both from cache
    assert d.query("a", "x") == -1.0 and d.bfs_runs == 2
    d.add_equation("c", "x", 4.0)                         # the miss must be forgotten ...
    assert d.query("a", "x") == 24.0 and d.bfs_runs == 3
    d.query("a", "c")                                     # ... but the hit survives the update
    assert d.bfs_runs == 3
    rng = Random(399)
    names = "abcdef"
    for _ in range(300):
        hidden = {c: rng.choice([1, 2, 3, 4, 5]) for c in names}
        live, fresh = Division(), []
        for _ in range(rng.randint(1, 12)):
            if rng.random() < 0.5:
                a, b = rng.sample(names, 2)
                live.add_equation(a, b, hidden[a] / hidden[b])
                fresh.append((a, b, hidden[a] / hidden[b]))
            else:
                x, y = rng.choice(names + "z"), rng.choice(names + "z")
                ref = Division()
                for a, b, v in fresh:
                    ref.add_equation(a, b, v)
                assert abs(live.query(x, y) - ref.query(x, y)) < 1e-9, (fresh, x, y)
    print("ok 399_evaluate_division_cached")
