"""LC 399 Evaluate Division -- weighted union-find: ratio[x] = x / parent[x]; find() multiplies ratios along the path."""
from collections import deque
from random import Random

# --- solution ---
def calc_equation(equations, values, queries):
    parent, ratio = {}, {}                           # ratio[x] == x / parent[x]; a root has ratio 1.0

    def find(x):                                     # returns the root, compresses the path, fixes ratios
        path = []
        while parent[x] != x:
            path.append(x)
            x = parent[x]
        root = x
        for node in reversed(path):                  # closest to the root first, so parent[node] is already compressed
            ratio[node] *= ratio[parent[node]]       # node/parent * parent/root = node/root
            parent[node] = root
        return root

    for (a, b), v in zip(equations, values):         # a / b == v
        for x in (a, b):
            if x not in parent:
                parent[x], ratio[x] = x, 1.0
        ra, rb = find(a), find(b)
        if ra == rb:
            if abs(ratio[a] / ratio[b] - v) > 1e-9 * max(1.0, abs(v)):
                raise ValueError(f"inconsistent equation {a}/{b}")
            continue
        parent[ra] = rb                              # attach ra under rb; solve ratio[ra] = ra / rb
        ratio[ra] = v * ratio[b] / ratio[a]

    out = []
    for a, b in queries:
        if a not in parent or b not in parent or find(a) != find(b):
            out.append(-1.0)
        else:
            out.append(ratio[a] / ratio[b])          # (a/root) / (b/root)
    return out
# --- end ---

def _brute(equations, values, queries):
    # moving from x to y multiplies by (x / y): edge (a -> b) has x/y = a/b = v, edge (b -> a) has b/a = 1/v
    graph = {}
    for (a, b), v in zip(equations, values):
        graph.setdefault(a, []).append((b, v))
        graph.setdefault(b, []).append((a, 1 / v))
    out = []
    for s, t in queries:
        if s not in graph or t not in graph:
            out.append(-1.0)
            continue
        seen, queue = {s: 1.0}, deque([s])
        while queue:
            u = queue.popleft()
            for w, f in graph[u]:
                if w not in seen:
                    seen[w] = seen[u] * f            # s / w  =  (s / u) * (u / w)
                    queue.append(w)
        out.append(seen.get(t, -1.0))
    return out

if __name__ == "__main__":
    got = calc_equation([["a", "b"], ["b", "c"]], [2.0, 3.0], [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]])
    assert [round(x, 5) for x in got] == [6.0, 0.5, -1.0, 1.0, -1.0]
    got = calc_equation([["a", "b"], ["b", "c"], ["bc", "cd"]], [1.5, 2.5, 5.0], [["a", "c"], ["c", "b"], ["bc", "cd"], ["cd", "bc"]])
    assert [round(x, 5) for x in got] == [3.75, 0.4, 5.0, 0.2]
    try:
        calc_equation([["a", "b"], ["a", "b"]], [2.0, 3.0], [])
        assert False
    except ValueError:
        pass
    rng = Random(47)
    names = "abcdefgh"
    for _ in range(400):
        hidden = {c: rng.choice([0.5, 1, 2, 3, 4, 5, 6]) for c in names}
        eqs, vals = [], []
        for _ in range(rng.randint(0, 8)):
            a, b = rng.sample(names, 2)
            eqs.append([a, b]); vals.append(hidden[a] / hidden[b])
        qs = [[rng.choice(names + "z"), rng.choice(names + "z")] for _ in range(6)]
        got, want = calc_equation(eqs, vals, qs), _brute(eqs, vals, qs)
        assert all(abs(g - w) < 1e-9 for g, w in zip(got, want)), (eqs, vals, qs, got, want)
    print("ok 399_evaluate_division")
