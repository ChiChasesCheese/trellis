# 15 · 并查集（Union-Find / Disjoint Set Union, DSU）

并查集（Union-Find）维护一组互不相交的集合，只做两件事：查某个元素属于哪个集合（`find`），把两个集合合并（`union`）。边一条条在线加入、随时问「是否连通」「有几个连通块」「最大的块多大」时，它比每次重新 BFS 快得多。路径压缩加按大小合并，让每次操作几乎是常数时间。它不支持删除，也不给出路径或距离，这是和 BFS / DFS 取舍的依据。

> 本讲覆盖：LC 547 Number of Provinces · 130 Surrounded Regions · 399 Evaluate Division（带权并查集）· 721 Accounts Merge · 827 Making A Large Island（Hard）· 305 Number of Islands II（Hard）
> 前置：第 06 讲（图、连通分量、第 4.1 节 Number of Islands 的追问里已经提过并查集）、第 01 讲的 `dict`；LC 128 Longest Consecutive Sequence（第 01 讲）和 LC 200 也可以用并查集写，本讲不重复。
> 读完你应该能：(1) 手写带「路径压缩 + 按大小合并」的 DSU 并说清两个优化各自解决什么；(2) 认出「合并 / 是否连通 / 连通块个数 / 最大块」这类需求，判断用 DSU 还是 BFS / DFS；(3) 做出带权 DSU（399）和稀疏 DSU（305，用 `dict`）；(4) 回答 DSU 的局限（不支持删除、`find` 会修改结构因此读也不是线程安全的）。

## 1. 这个模式是什么，为什么存在

### 1.1 从最笨的解法开始

LC 305 Number of Islands II：一张 `m × n` 的水面，依次在若干位置"造陆地"；每造一块，立即回答现在有几个岛屿。

最笨的做法：每次造完陆地，把整张图用第 06 讲的 flood fill 重新数一遍：每次 O(m·n)，`k` 次操作总计 O(k·m·n)。`m = n = 10⁴`、`k = 10⁴` 时是 10¹² 级别。

更一般的问题："一堆点，不断加入新的边，随时问 `a` 和 `b` 是否连通、有几个连通块"。每次加边都重新跑一遍 BFS，同样是 O(k · (V + E))。

### 1.2 慢在哪里 / 错在哪里

每次加一条边，其实**绝大多数连通关系没有变化**，却把全图重新探索了一遍。真正发生的只是：两个连通块合并成一个。

> 因果链：需要的操作只有两个——"`a` 属于哪个块？"和"把 `a` 的块和 `b` 的块合并" → 给每个块选一个**代表（root）**，每个点记住"我的上级是谁"（`parent`），沿着 `parent` 往上走到根就是所属的块（`find`）；合并 = 让一个根指向另一个根（`union`）。 → 不加优化时，合并可能把链越拉越长（`find` 退化成 O(n)）；加两个优化后，每次操作的平均成本是反阿克曼函数 α(n)，对任何现实的 n 都 ≤ 4——**可以当成常数**。

### 1.3 并查集是什么（从零讲）

- **并查集（Union-Find，也叫 Disjoint Set Union, DSU）**：维护一组互不相交的集合，支持：
  - `find(x)`：返回 `x` 所在集合的代表（根）。两个元素在同一集合 ⟺ 它们的 `find` 相等。
  - `union(a, b)`：把 `a` 和 `b` 所在的集合合并。
- **数据结构**：一个数组 `parent`，`parent[x]` 是 `x` 的"上级"；根的 `parent` 指向自己。可视化成森林，每棵树是一个集合。
- **两个优化**（缺一都可能退化）：
  1. **路径压缩（path compression）**：`find` 走到根的路上，顺手让沿途的点直接指向根（或指向祖父——**路径减半**，path halving，一行写完，更适合面试）。以后再找它们就是 1 步。
  2. **按大小（或秩）合并（union by size / rank）**：合并时总是把**小树挂到大树的根下**，树的高度只会在两棵树一样大时增长，因此高度 ≤ log₂ n。
  只用其中一个，均摊是 O(log n)；两个一起用，均摊 O(α(n))。
- **连通块个数**：开始是 `n`；每次 `union` **成功**（两个根不同）就减 1。所以 `union` 要返回布尔值。
- **环检测**：对一条无向边 `(a, b)`，如果 `union` 失败（已经连通），说明这条边在图中形成了环——这就是 LC 684 Redundant Connection，也是 Kruskal 最小生成树里"跳过会成环的边"的判断。
- **局限**（面试常问）：
  - **不支持删除边**。需要删除时：离线则时间倒放（把删除变成添加）；在线则用带回滚的 DSU（放弃路径压缩）、link-cut tree 等。
  - **只表示无向的连通关系**。有向图的可达性、强连通分量不是 DSU 能处理的（用第 06 讲的拓扑排序或 Tarjan / Kosaraju）。
  - **`find` 会修改 `parent`**（路径压缩）。所以即使是"只读查询"，多线程同时调用也不安全。
- **扩展：带权并查集**。让每个点额外保存"相对于父节点的某个量"（比值 / 差 / 奇偶性 / 异或值），`find` 压缩路径时把这个量沿路径累乘 / 累加。399 保存的是"x / 父节点"；"二分图判定（奇偶性）"、"食物链"等经典题都是同一个套路。
- **稀疏 DSU**：元素不是 `0..n-1` 的整数（比如坐标 `(r, c)`、邮箱字符串）或者元素数量远小于坐标范围（305：10⁴ × 10⁴ 的网格只加了 10⁴ 块陆地）时，`parent` 用 `dict` 并**按需创建**。

## 2. 模板与逐行讲解

```python
from collections import deque
from random import Random

# Template U1: union-find with path halving + union by size; union() reports whether it merged anything
class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]     # path halving: skip to the grandparent
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)                  # always work on ROOTS, never on a and b themselves
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra                                 # small tree under the big tree's root
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

    def size_of(self, x):
        return self.size[self.find(x)]


# Template U2: the first thing union-find buys you -- cycle detection (LC 684 Redundant Connection)
def find_redundant_connection(edges):
    dsu = DisjointSet(len(edges) + 1)                        # nodes are 1..n
    for a, b in edges:
        if not dsu.union(a, b):
            return [a, b]                                    # this edge joins two nodes that were already connected
    return []


def _components_bfs(n, edges):
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    seen, count = [False] * n, 0
    for s in range(n):
        if seen[s]:
            continue
        count += 1
        seen[s] = True
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if not seen[v]:
                    seen[v] = True
                    queue.append(v)
    return count


dsu = DisjointSet(5)
assert dsu.union(0, 1) and dsu.union(3, 4) and not dsu.union(1, 0)
assert dsu.connected(0, 1) and not dsu.connected(1, 3) and dsu.components == 3 and dsu.size_of(4) == 2
assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
assert find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
rng = Random(1)
for _ in range(300):
    n = rng.randint(1, 12)
    edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 14))]
    d = DisjointSet(n)
    for a, b in edges:
        d.union(a, b)
    assert d.components == _components_bfs(n, edges)         # components == n - (number of successful unions)
```

逐行讲解：

1. `self.parent = list(range(n))`：开始时每个点自成一个集合，自己是自己的根。
2. `find` 里的 `parent[x] = parent[parent[x]]`：把 `x` 直接接到祖父上，然后继续向上。一遍走完，路径上每个点的深度大约减半；这是循环（不是递归）写法，不会有递归深度问题。
3. `union` 里先 `find` 两个参数：**合并的是根，不是 `a`、`b` 本身**。把 `parent[a] = b` 写成这样是最常见的错误——`a`、`b` 可能不是根，会把整个集合"撕开"。
4. `if self.size[ra] < self.size[rb]: swap`：保证 `ra` 是较大的那棵，小树挂到大树下。`size` 只在**根**上有意义，所以只更新 `size[ra]`。
5. `return False` / `True`：`False` 表示两个点已经连通——环检测（U2）和统计连通块个数都依赖这个返回值。
6. `components -= 1`：每次成功合并少一个块，所以不需要最后再数一遍根。
7. U2 的 684：按顺序加边，第一条使 `union` 失败的边就是答案——它连接的是已经连通的两点，加上它才出现环。
8. 随机对拍：用 BFS 数连通块作为参照，验证 `components == n − 成功合并次数`。

## 3. 完整手算（Worked trace）

下面的输出是真实运行结果：8 个点依次合并，打印每一步 `parent` 数组；然后是 2000 个点的长链实验，对比"朴素合并"和"两个优化都开"的树高。

```python
class TraceDSU:
    def __init__(self, n, by_size=True, compress=True):
        self.parent = list(range(n))
        self.size = [1] * n
        self.by_size, self.compress = by_size, compress

    def find(self, x):
        while self.parent[x] != x:
            if self.compress:
                self.parent[x] = self.parent[self.parent[x]]     # path halving
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.by_size and self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

    def depth(self, x):
        d = 0
        while self.parent[x] != x:
            x, d = self.parent[x], d + 1
        return d

d = TraceDSU(8)
print("start        parent =", d.parent)
components = 8
for a, b in [(0, 1), (2, 3), (0, 2), (4, 5), (6, 7), (4, 6), (1, 3), (0, 4)]:
    merged = d.union(a, b)
    components -= merged
    print(f"union({a},{b}) -> {str(merged):5}  parent = {d.parent}  components = {components}")
print("sizes at the roots:", {r: d.size[r] for r in range(8) if d.parent[r] == r})
print("find(7) =", d.find(7), " parent after find(7) =", d.parent)
assert components == 1 and d.find(7) == d.find(3)

# why the two tricks matter: join 0-1, 1-2, 2-3, ... in the unlucky order "(new, old)" so the naive rule builds a chain
n = 2000
naive = TraceDSU(n, by_size=False, compress=False)
smart = TraceDSU(n)
for i in range(n - 1):
    naive.union(i + 1, i)            # naive: the root of the first argument is attached UNDER the root of the second argument
    smart.union(i + 1, i)
print("chain of", n, "nodes: deepest node depth, naive =", max(naive.depth(x) for x in range(n)),
      " union-by-size + path halving =", max(smart.depth(x) for x in range(n)))
```

```text
start        parent = [0, 1, 2, 3, 4, 5, 6, 7]
union(0,1) -> True   parent = [0, 0, 2, 3, 4, 5, 6, 7]  components = 7
union(2,3) -> True   parent = [0, 0, 2, 2, 4, 5, 6, 7]  components = 6
union(0,2) -> True   parent = [0, 0, 0, 2, 4, 5, 6, 7]  components = 5
union(4,5) -> True   parent = [0, 0, 0, 2, 4, 4, 6, 7]  components = 4
union(6,7) -> True   parent = [0, 0, 0, 2, 4, 4, 6, 6]  components = 3
union(4,6) -> True   parent = [0, 0, 0, 2, 4, 4, 4, 6]  components = 2
union(1,3) -> False  parent = [0, 0, 0, 0, 4, 4, 4, 6]  components = 2
union(0,4) -> True   parent = [0, 0, 0, 0, 0, 4, 4, 6]  components = 1
sizes at the roots: {0: 8}
find(7) = 0  parent after find(7) = [0, 0, 0, 0, 0, 4, 4, 4]
chain of 2000 nodes: deepest node depth, naive = 1999  union-by-size + path halving = 1
```

怎么读：

- `union(0,1)` 之后 `parent[1] = 0`：两个大小相同时，第一个参数的根当根。`union(0,2)` 时 `0` 的块和 `2` 的块大小都是 2，`2` 挂到 `0` 下。
- `union(1,3) -> False`：`find(1)` 是 `0`，`find(3)` 沿着 `3 → 2 → 0`，**路径减半**顺手把 `parent[3]` 从 `2` 改成了 `0`（看 `parent` 数组的第 3 项）。两个根相同，所以没有合并，`components` 不变——这也是"这条边会成环"的信号。
- 最后一步 `find(7)` 之后 `parent[7]` 从 `6` 变成了 `4`，树更扁了。查询本身改变了结构，这就是为什么 DSU 的"读"不是线程安全的。
- 长链实验：朴素合并（不按大小、不压缩）把 2000 个点串成深度 1999 的链，一次 `find` 要走 1999 步；两个优化都开时最深只有 1。这是面试里"为什么需要这两个优化"的最好回答——给一个会让朴素版本退化的输入顺序。

## 4. 题目

```python
from collections import defaultdict
```

### 4.1 LC 547 · Number of Provinces（Medium）

```python
# solutions/547_number_of_provinces.py
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
```

- **一句话洞见**：城市 `i` 和 `j` 相连就合并；省份个数 = `n` − 成功合并的次数。邻接矩阵对称，只看上三角（`j > i`）。
- **对比 DFS / BFS**：同样 O(n²)（读邻接矩阵本身就是 n²），写起来 DSU 更短；但如果题目变成"边在不断加入"，只有 DSU 能做到在线回答。
- **复杂度**：时间 O(n² · α(n))，空间 O(n)。

**资深追问**

- **规模 ×1000**：邻接矩阵是 O(n²) 内存，n = 10⁵ 就不能用了；输入应该是**边列表**，复杂度 O((V + E) α(V))。
- **流式**：边一条条到达，DSU 在线维护连通块个数，每条边 O(α)。
- **内存**：`parent` + `size` 两个长度为 n 的数组，O(n)。
- **并发 / 分布式**：把边分到多个分片，每个分片各自跑 DSU 得到"局部标签"，再把各分片的标签合并（对跨分片的端点再做一次 union）——这是 MapReduce 里求连通分量的标准做法。
- **接口**：矩阵是否保证对称、对角线是否都是 1（都不要依赖）；返回个数，还是返回每个省份的成员？
- **测试**：全不连通（n 个）、全连通（1 个）、单个城市、一条长链（深度测试）；与 DFS 对拍。

### 4.2 LC 130 · Surrounded Regions（Medium）

```python
# solutions/130_surrounded_regions.py
def solve(board):
    """Flips surrounded 'O' to 'X' IN PLACE (the LeetCode contract); returns None."""
    if not board or not board[0]:
        return
    rows, cols = len(board), len(board[0])
    parent = list(range(rows * cols + 1))
    border = rows * cols                                   # dummy node = "connected to the outside"

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != "O":
                continue
            if r in (0, rows - 1) or c in (0, cols - 1):
                union(r * cols + c, border)
            for dr, dc in ((1, 0), (0, 1)):                # right and down are enough: every pair is seen once
                nr, nc = r + dr, c + dc
                if nr < rows and nc < cols and board[nr][nc] == "O":
                    union(r * cols + c, nr * cols + nc)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "O" and find(r * cols + c) != find(border):
                board[r][c] = "X"
```

- **一句话洞见**：被围住的 `O` = 不与边界上的 `O` 连通的 `O`。引入一个**虚拟节点**代表"外面"，把边界上的 `O` 都并到它上面；其余的 `O` 如果和虚拟节点不在同一集合，就翻成 `X`。
- **对比**：最常见的写法是"从边界的 `O` 出发 DFS / BFS，标记所有不会被翻转的 `O`"，同样 O(R·C) 而且更直观——**面试里先说这个**，再说 DSU 版本。DSU 版本的价值在于：如果题目变成"棋盘上不断落子，随时问某块是否被围"，DSU 可以增量维护。
- **复杂度**：时间 O(R·C · α)，空间 O(R·C)。

**资深追问**

- **规模 ×1000**：棋盘大到放不下内存：分块处理，每块内部做 DSU，块与块之间只对边界格子做合并（只需要保存每块的边界标签）。
- **流式**：落子一个一个来：新增一个 `O`，和四邻合并；如果它在边界，就并到虚拟节点；查询某个 `O` 是否被围 = 是否与虚拟节点同集合。
- **内存**：O(R·C) 的 `parent`；DFS 版本用 O(R·C) 的 visited 也一样。
- **并发**：只读棋盘上的并行 DFS 是安全的；翻转必须在所有标记完成之后。
- **接口**：**原地修改**，返回 `None`（LeetCode 约定）；是否要求不修改输入而返回新棋盘；对角线是否算相邻（题目是 4 连通）。
- **测试**：全 `O`、全 `X`、1×N / N×1（全部是边界）、中间一个孤立 `O`、边界上的 `O` 通向内部的"触手"；与边界 DFS 对拍。

### 4.3 LC 399 · Evaluate Division（Medium）

```python
# solutions/399_evaluate_division.py
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
```

- **一句话洞见**：已知 `a / b = v`，等价于在 `a` 和 `b` 之间连一条"比值为 `v`"的边。把变量放进同一个集合，并让每个变量保存"我相对于父节点的比值" `ratio[x] = x / parent[x]`；`find` 压缩路径时把比值沿路径累乘，使 `ratio[x]` 变成 `x / root`。查询 `a / b` 时，若同根，答案是 `ratio[a] / ratio[b]`（两者都除以根，根约掉）。
- **合并时的公式**：`ra` 挂到 `rb` 下，需要 `ratio[ra] = ra / rb`。已知 `a / ratio[a] = ra`，`b / ratio[b] = rb`，所以 `ra / rb = (a / b) · ratio[b] / ratio[a] = v · ratio[b] / ratio[a]`。
- **对比 BFS / DFS**：建图后每次查询 BFS，O(Q · (V + E))。带权 DSU 把预处理做完后每次查询 O(α)；而且**一致性检查**（同根但比值冲突 → 输入矛盾）几乎免费。
- **复杂度**：时间 O((E + Q) α)，空间 O(V)。

**资深追问**

- **规模 ×1000**：线性于输入；100 万个变量时用整数编号代替字符串键，`parent`/`ratio` 用数组。
- **流式**：新的等式随时到达，DSU 在线合并；每条新等式顺便检查是否与已有关系矛盾（示例抛 `ValueError`；真实系统应该记录并报告冲突的两条等式）。
- **内存**：`parent` 和 `ratio` 两个 `dict`，O(V)。连乘会**上溢 / 下溢**（浮点）：可以对数变换，存 `log(ratio)`，乘变加，数值更稳定；要求精确时用 `fractions.Fraction`。
- **并发**：`find` 会修改 `parent` 和 `ratio`（路径压缩），所以**只读查询也不是线程安全的**——用互斥锁，或者建好后"冻结"：对所有变量先 `find` 一遍使每个点直接指向根，之后的查询只读，可以放心并发。
- **接口**：未知变量的 `x / x` 返回 `-1.0`（LeetCode 约定）；除数为 0 的等式（`v = 0` 会让反向边无意义）怎么办；浮点比较要带容差。
- **测试**：链式（`a/b, b/c` → `a/c`）、反向（`b/a`）、孤立变量、`a/a`、矛盾输入；随机生成"隐藏真值"的一致等式，与 BFS 乘积对拍。

### 4.4 LC 721 · Accounts Merge（Medium）

```python
# solutions/721_accounts_merge.py
def accounts_merge(accounts):
    parent = list(range(len(accounts)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    owner = {}                                         # email -> index of the first account that listed it
    for i, acc in enumerate(accounts):
        for email in acc[1:]:
            if email in owner:
                parent[find(i)] = find(owner[email])   # same email => same person
            else:
                owner[email] = i
    groups = defaultdict(set)
    for email, i in owner.items():
        groups[find(i)].add(email)
    return [[accounts[root][0]] + sorted(emails) for root, emails in groups.items()]
```

- **一句话洞见**：两个账号只要共享**任意一个**邮箱就是同一个人（传递：A 与 B 共享、B 与 C 共享，则 A、B、C 同人）。用 DSU 合并**账号下标**：`owner[email]` 记录第一个出现该邮箱的账号；之后再遇到就把两个账号并起来。最后把每个邮箱按 `find(owner)` 分组、排序。
- **陷阱**：**名字相同不代表同一个人**，不能按名字合并；最终输出的名字取自组内任意账号（它们同名）。分组必须调用 `find`，不能直接读 `parent[i]`（还没压缩）。
- **复杂度**：设邮箱总数为 E，时间 O(E α + E log E)（排序是主导），空间 O(E)。

**资深追问**

- **规模 ×1000**：10⁹ 个账号：内存放不下 `owner` 字典。外存方案——按邮箱做外排序，相邻相同邮箱的账号 ID 合并；用 MapReduce 迭代求连通分量（label propagation）或分片 DSU + 边界合并。
- **流式**：新账号到达时：对每个邮箱查 `owner`，命中就 `union`，没命中就登记；成员列表需要"按根维护集合"（或延迟到查询时物化）。
- **内存**：`owner`（邮箱 → 下标）和 `groups`；字符串可以 `sys.intern` 或存哈希。
- **并发**：写入需要锁（`union` 修改多个数组）；分片后合并是更好的扩展方式。
- **接口**：输出里账号的顺序不保证；邮箱是否要区分大小写 / 规范化（Gmail 的点号）；**邮箱是个人信息（PII）**，日志里不要打印；账号内部有重复邮箱要容忍。
- **测试**：链式传递合并（A–B、B–C）、同名不同人保持分开、同一账号里重复邮箱、单个账号、空输入；与"邮箱图上的 DFS 连通分量"对拍。

### 4.5 LC 827 · Making A Large Island（Hard）

```python
# solutions/827_making_a_large_island.py
def largest_island(grid):
    rows, cols = len(grid), len(grid[0])
    parent = list(range(rows * cols))
    size = [1] * (rows * cols)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]

    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for r in range(rows):
        for c in range(cols):
            if grid[r][c]:
                for dr, dc in ((1, 0), (0, 1)):
                    nr, nc = r + dr, c + dc
                    if nr < rows and nc < cols and grid[nr][nc]:
                        union(r * cols + c, nr * cols + nc)
    best = max((size[find(i)] for i in range(rows * cols) if grid[i // cols][i % cols]), default=0)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                roots = set()                                    # a SET: one island touching the cell twice counts once
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc]:
                        roots.add(find(nr * cols + nc))
                best = max(best, 1 + sum(size[x] for x in roots))
    return best
```

- **一句话洞见**：先用 DSU 把所有岛屿合并好并记录每个岛的大小；然后对每个 `0` 格子，看它**四个邻居所属的岛**（用 `set` 去重），翻成 `1` 后的岛大小 = 1 + 这些不同岛的大小之和。取最大值。
- **陷阱**：同一个岛可能同时出现在这个格子的两个以上的邻居上（比如岛屿弯成 U 形把一个 `0` 围住）——**不用集合去重会重复相加**。全是陆地的棋盘没有 `0` 可翻，答案是 `R·C`（代码里由第一个 `best` 覆盖）；全是水则答案是 1。
- **复杂度**：时间 O(R·C · α)，空间 O(R·C)。暴力解（每个 `0` 翻一次再重新数）是 O((R·C)²)。

**资深追问**

- **规模 ×1000**：线性于格子数；超大棋盘分块 + 只保存块边界上的 `(岛标签, 大小)`。
- **流式**：格子随时变成陆地：DSU 在线维护岛大小；"翻转一个水格的收益"要实时查询四个邻居的根，仍然是 O(α)。注意变成**水**（删除）DSU 不支持，需要离线倒放。
- **内存**：`parent` + `size` 两个数组；可以用二进制压缩 `size`。
- **并发**：DSU 构建阶段按行分块并行再合并边界；评估每个 `0` 的收益时只读（但 `find` 会压缩路径！先对所有格子 `find` 一遍冻结结构，再并行评估）。
- **接口**：只允许翻一个格子；允许翻 `k` 个会变成 NP-hard 风格的优化，要先问清楚；4 连通。
- **测试**：全 0、全 1、`[[1,0],[0,1]]` 对角线（翻一格得 3）、U 形岛围住一个 0（去重测试）；与"逐个翻转 + 重新数最大岛"的暴力解对拍。

### 4.6 LC 305 · Number of Islands II（Hard）

```python
# solutions/305_number_of_islands_ii.py
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
```

- **一句话洞见**：把"造陆地"看成加入一个新节点，岛屿数先 `+1`；然后对四个邻居中已经是陆地的，每成功合并一次就 `-1`。每次操作 O(α)，完全不需要重新扫描网格。
- **稀疏 DSU**：`parent`、`size` 用 `dict`，只有陆地才有条目；内存 O(操作数)，与网格大小无关（10⁴ × 10⁴ 的棋盘不会分配 10⁸ 个格子）。
- **陷阱**：对同一个位置重复 `addLand` 要直接返回当前计数（不能当作新节点，否则会 `+1` 然后合并自己）。
- **复杂度**：总时间 O(k α(k))，空间 O(k)（k = 操作数）。

**资深追问**

- **规模 ×1000**：k = 10⁶ 次操作：线性；坐标范围极大时（1e9 × 1e9）稀疏 `dict` 版本仍然可行，数组版本不可行。
- **流式**：这类问题本身就是流式的——这就是 DSU 的主场；输出可以边算边写。
- **内存**：每块陆地一个 `dict` 条目（键是元组，较贵）；可以编码成整数 `r * n + c`。
- **并发**：多生产者提交 `addLand`：串行化更新（单线程事件循环或加锁）；或者按区域分片，每个分片一个 DSU，跨边界用一个小的协调层合并。
- **接口**：`removeLand` **不支持**——要说明 DSU 不能删除，替代方案：离线倒放（把删除变成添加）、带回滚的 DSU（放弃路径压缩，按秩合并，O(log n)）；越界坐标应抛 `ValueError` 还是忽略。
- **测试**：重复位置、一条线上依次连接、对角线不连通、先造外围后造中心（一次合并多个岛）；与每次重新 flood fill 的暴力解对拍。

## 5. 常见 bug

1. **合并时没用根**：写成 `parent[a] = b`，而 `a` 不是根，会把 `a` 的整个集合撕开。永远 `ra, rb = find(a), find(b)`，然后 `parent[ra] = rb`。
2. **忘了按大小合并**，或者更新了错误节点的 `size`：`size` 只在根上有意义，合并后只更新新根的 `size`。
3. **统计连通块时数 `parent[i] == i`**，却忘了只有**根**才满足；更稳妥是维护 `components` 计数（每次成功合并 `-1`），或最后对每个点 `find`。
4. **分组时直接读 `parent[i]`**：没压缩过时不是根；必须 `find(i)`（721）。
5. **递归版 `find` 在长链上爆栈**：Python 默认递归深度 1000；用循环 + 路径减半（本讲写法）。
6. **带权 DSU 压缩路径的顺序**：必须**离根最近的节点先更新**，这样 `ratio[parent[node]]` 已经是 `parent / root`；顺序反了就会用到旧的比值（399 的 `reversed(path)`）。
7. **827 不去重邻居的根**：同一个岛被加了两次。
8. **305 对重复位置重复计数**；或把二维坐标映射到一维下标时 `cols` 写错（`r * cols + c`）。
9. **把 DSU 用在有向图或需要删除的场景**：DSU 只表示无向连通，且不支持删除。
10. **并发读时忘记 `find` 会写**：路径压缩改变了 `parent`；多线程只读也要加锁或先"冻结"。

## 6. 自测题

1. 路径压缩和按大小合并分别解决什么问题？只用一个够吗？
   <details><summary>答案</summary>按大小合并限制树高 ≤ log n（防止合并出长链）；路径压缩让之后的查询把路径摊平。只用一个均摊 O(log n)，两个一起是 O(α(n))（反阿克曼，实际 ≤ 4）。</details>
2. 为什么 `union` 要返回布尔值？
   <details><summary>答案</summary>返回 `False` 表示两个点已经在同一个集合——这意味着这条边会形成环（684、Kruskal），并且不应该把连通块计数减 1。`True` 表示发生了一次真正的合并，`components -= 1`。</details>
3. DSU 为什么不支持删除边？有什么变通？
   <details><summary>答案</summary>合并后只保留了"根"这一粒度的信息，路径压缩更是丢掉了原来的树结构，无法还原删除一条边之后的连通性。变通：离线时把时间倒放（删除变添加）；在线时用带回滚的 DSU（按秩合并、不压缩、用栈记录合并），或 link-cut tree / 动态连通性数据结构。</details>
4. 小编程：判断无向图加入某条边后会不会出现环，要求支持连续加边。
   <details><summary>答案</summary>`dsu = DisjointSet(n)`；对每条边 `if not dsu.union(a, b): 有环`。每条边 O(α)。</details>
5. 399 里为什么 `find` 压缩路径时要把比值累乘？
   <details><summary>答案</summary>`ratio[x]` 的含义是 `x / parent[x]`。把 `x` 直接接到根上时，新的含义变成 `x / root`，等于 `x / parent[x]` 乘以 `parent[x] / root`；若不累乘，改了 `parent` 却没改 `ratio`，查询结果就错了。</details>
6. 什么时候 BFS / DFS 比 DSU 更合适？
   <details><summary>答案</summary>静态图且只需要一次性回答连通性 / 最短路径（DSU 给不了路径或距离）；需要遍历顺序或层数（BFS 最短路）；有向图。DSU 更合适：边在线加入、随时问连通性、要维护块大小 / 块个数、Kruskal。</details>
7. 资深追问：服务里用 DSU 维护"同一账号的设备组"，并发读写很高，怎么办？
   <details><summary>答案</summary>`find` 的路径压缩会写，所以读也要同步。方案：(1) 读写锁 + 读时使用不压缩的 `find`（O(log n) 但只读）；(2) 写入走单线程队列，定期生成"冻结快照"（所有点直接指向根）供读线程无锁使用；(3) 无锁 DSU（对 `parent` 做 CAS，Anderson–Woll），实现复杂；(4) 按键分片，跨片合并走异步协调。同时持久化 union 日志以便恢复，并考虑"拆分设备组"（需求变成删除）时改用带回滚结构或定期重建。</details>
