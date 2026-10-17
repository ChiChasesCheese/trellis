"""Lowest Common Manager -- org chart as an n-ary tree. Parent map + depth, climb the deeper one; binary lifting for many queries."""
from random import Random

# --- solution ---
def build(reports):                                       # reports: {manager: [direct reports]}; returns parent, depth, root
    parent, depth = {}, {}
    boss = {r for rs in reports.values() for r in rs}
    root = next(m for m in reports if m not in boss)
    depth[root], parent[root] = 0, None
    stack = [root]                                        # iterative: an org chart can be thousands of levels deep
    while stack:
        u = stack.pop()
        for v in reports.get(u, []):
            parent[v], depth[v] = u, depth[u] + 1
            stack.append(v)
    return parent, depth, root

def lowest_common_manager(parent, depth, a, b):
    if a not in parent or b not in parent:
        return None                                       # an employee who is not in the chart
    while depth[a] > depth[b]:
        a = parent[a]
    while depth[b] > depth[a]:
        b = parent[b]
    while a != b:
        a, b = parent[a], parent[b]
    return a                                              # an employee can be their own lowest common manager

def lcm_of_many(parent, depth, people):
    people = list(people)
    if not people or any(p not in parent for p in people):
        return None
    acc = people[0]
    for p in people[1:]:                                  # LCA is associative: fold it
        acc = lowest_common_manager(parent, depth, acc, p)
    return acc

class Lifting:                                            # O(n log n) build, O(log n) per query
    def __init__(self, parent, depth):
        self.depth = depth
        up = [{v: (p if p is not None else v) for v, p in parent.items()}]   # up[k][v] = 2^k-th ancestor (root points at itself)
        while 2 ** len(up) <= len(parent):
            prev = up[-1]
            up.append({v: prev[prev[v]] for v in parent})
        self.up = up

    def query(self, a, b):
        if a not in self.depth or b not in self.depth:
            return None
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        gap = self.depth[a] - self.depth[b]
        for k, table in enumerate(self.up):
            if gap >> k & 1:
                a = table[a]
        if a == b:
            return a
        for table in reversed(self.up):
            if table[a] != table[b]:
                a, b = table[a], table[b]
        return self.up[0][a]
# --- end ---

def _brute(parent, a, b):
    if a not in parent or b not in parent:
        return None
    chain = set()
    while a is not None:
        chain.add(a)
        a = parent[a]
    while b not in chain:
        b = parent[b]
    return b

if __name__ == "__main__":
    reports = {"ceo": ["a", "b"], "a": ["c", "d"], "b": ["e"], "d": ["f"]}
    parent, depth, root = build(reports)
    assert root == "ceo" and lowest_common_manager(parent, depth, "f", "c") == "a"
    assert lowest_common_manager(parent, depth, "f", "e") == "ceo"
    assert lowest_common_manager(parent, depth, "a", "f") == "a"
    assert lowest_common_manager(parent, depth, "a", "ghost") is None
    assert lcm_of_many(parent, depth, ["f", "c", "d"]) == "a" and lcm_of_many(parent, depth, ["f", "e", "c"]) == "ceo"
    chain = {i: [i + 1] for i in range(5000)}             # 5000 levels deep: no recursion anywhere
    p, d, r = build(chain)
    assert lowest_common_manager(p, d, 4999, 10) == 10 and Lifting(p, d).query(4999, 10) == 10
    rng = Random(11)
    for _ in range(300):
        n = rng.randint(1, 30)
        reports = {}
        for v in range(1, n):
            reports.setdefault(rng.randrange(v), []).append(v)
        reports = reports or {0: []}
        parent, depth, root = build(reports)
        lift = Lifting(parent, depth)
        for _ in range(10):
            a, b = rng.randrange(n + 1), rng.randrange(n + 1)
            want = _brute(parent, a, b)
            assert lowest_common_manager(parent, depth, a, b) == want == lift.query(a, b), (reports, a, b)
    print("OK amz_lowest_common_manager")
