"""LC 305 Number of Islands II -- online union-find: each addLand is O(alpha) instead of a full re-scan."""
from random import Random

# --- solution ---
def num_islands_ii(m, n, positions):
    parent = {}                                       # only land cells exist in the structure (sparse, O(#adds) memory)
    size = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    islands, answer = 0, []
    for r, c in positions:
        cell = (r, c)
        if cell in parent:                            # duplicate addLand: nothing changes
            answer.append(islands)
            continue
        parent[cell], size[cell] = cell, 1
        islands += 1                                  # a brand-new island ...
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nb = (r + dr, c + dc)
            if nb in parent:
                ra, rb = find(cell), find(nb)
                if ra != rb:                          # ... which every successful merge reduces by one
                    if size[ra] < size[rb]:
                        ra, rb = rb, ra
                    parent[rb] = ra
                    size[ra] += size[rb]
                    islands -= 1
        answer.append(islands)
    return answer
# --- end ---

def _count(m, n, land):
    seen, count = set(), 0
    for cell in land:
        if cell in seen:
            continue
        count += 1
        stack = [cell]
        seen.add(cell)
        while stack:
            r, c = stack.pop()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nb = (r + dr, c + dc)
                if nb in land and nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
    return count

def _brute(m, n, positions):
    land, out = set(), []
    for p in positions:
        land.add(tuple(p))
        out.append(_count(m, n, land))
    return out

if __name__ == "__main__":
    assert num_islands_ii(3, 3, [[0, 0], [0, 1], [1, 2], [2, 1]]) == [1, 1, 2, 3]
    assert num_islands_ii(1, 1, [[0, 0]]) == [1]
    assert num_islands_ii(1, 1, [[0, 0], [0, 0]]) == [1, 1]
    assert num_islands_ii(2, 2, []) == []
    rng = Random(61)
    for _ in range(400):
        m, n = rng.randint(1, 5), rng.randint(1, 5)
        pos = [[rng.randrange(m), rng.randrange(n)] for _ in range(rng.randint(0, 14))]
        assert num_islands_ii(m, n, pos) == _brute(m, n, pos), (m, n, pos)
    print("ok 305_number_of_islands_ii")
