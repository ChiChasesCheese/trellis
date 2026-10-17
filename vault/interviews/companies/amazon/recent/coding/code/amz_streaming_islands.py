"""Streaming islands -- the matrix arrives ONE ROW AT A TIME; keep only the previous row's labels (O(n) memory) and union-find."""
from random import Random

# --- solution ---
class StreamIslands:
    def __init__(self, width):
        self.n = width
        self.prev = [0] * width                           # label of each cell in the previous row (0 = water)
        self.parent, self.area = {}, {}                   # only components still touching the previous row live here
        self.next_id = 1
        self.closed = 0                                   # islands that can no longer grow
        self.max_area = 0

    def _find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def feed(self, row):
        cur = [0] * self.n
        for c, cell in enumerate(row):
            if not cell:
                continue
            cur[c] = self.next_id
            self.parent[self.next_id], self.area[self.next_id] = self.next_id, 1
            self.next_id += 1
            for other in (self.prev[c], cur[c - 1] if c else 0):   # neighbour above, neighbour on the left
                if other:
                    a, b = self._find(cur[c]), self._find(other)
                    if a != b:
                        self.parent[a] = b
                        self.area[b] += self.area.pop(a)
        alive = {self._find(x) for x in cur if x}
        for root in [r for r in self.area if r not in alive]:     # touches no cell of this row: finished
            self.closed += 1
            self.max_area = max(self.max_area, self.area.pop(root))
        self.parent = {x: self._find(x) for x in cur if x}        # forget old ids, keep this row's roots
        for root in alive:
            self.parent[root] = root
        self.prev = cur

    def result(self):                                     # (islands, largest area) of everything fed so far
        live = list(self.area.values())
        return self.closed + len(live), max([self.max_area] + live)
# --- end ---

def _brute(grid):
    m, n = len(grid), len(grid[0])
    seen, count, best = set(), 0, 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] and (r, c) not in seen:
                count, size, stack = count + 1, 0, [(r, c)]
                seen.add((r, c))
                while stack:
                    a, b = stack.pop()
                    size += 1
                    for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        x, y = a + da, b + db
                        if 0 <= x < m and 0 <= y < n and grid[x][y] and (x, y) not in seen:
                            seen.add((x, y))
                            stack.append((x, y))
                best = max(best, size)
    return count, best

if __name__ == "__main__":
    s = StreamIslands(5)
    for row in ([1, 1, 0, 0, 1], [0, 1, 0, 1, 1], [0, 0, 0, 0, 0], [1, 0, 1, 1, 0]):
        s.feed(row)
    assert s.result() == (4, 3) and len(s.prev) == 5
    s = StreamIslands(3)                                  # a U shape: two arms are merged only by the bottom row
    for row in ([1, 0, 1], [1, 0, 1], [1, 1, 1]):
        s.feed(row)
    assert s.result() == (1, 7)
    rng = Random(305)
    for _ in range(400):
        m, n = rng.randint(1, 7), rng.randint(1, 7)
        g = [[1 if rng.random() < 0.5 else 0 for _ in range(n)] for _ in range(m)]
        st = StreamIslands(n)
        for row in g:
            st.feed(row)
        assert st.result() == _brute(g), g
        assert len(st.parent) <= 2 * n and len(st.area) <= n          # memory stays O(width), never O(rows); 2n: cells + older roots
    print("OK amz_streaming_islands")
