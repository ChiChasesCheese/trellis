# 06 · 图：BFS / DFS（网格与图）与拓扑排序（Graph traversal & topological sort）

图（graph）题的第一步是把「格子 / 单词 / 课程」翻译成「点 + 边」。要数连通块或探索所有可能时用 DFS 或 BFS；要最短步数（无权图）时用 BFS，一层对应一步；要处理有依赖关系的顺序时用拓扑排序（topological sort），Kahn 算法同时能检测环。网格题还有 Python 递归深度的坑，大网格要改成显式栈或 BFS。下面从零讲图，再给模板和五道题。

覆盖的题目：LC 200 Number of Islands · 994 Rotting Oranges · 127 Word Ladder（Hard）· 207 Course Schedule（含 210）· 269 Alien Dictionary（Hard）


## 1. 这个模式是什么，为什么存在

### 1.1 从最笨的解法开始

LC 200：二维网格里 `'1'` 是陆地，`'0'` 是水，数岛屿（上下左右相连的陆地为一个岛）。

人手怎么数？找到一块陆地，**把和它相连的所有陆地都涂成已访问**，岛屿数 +1，再找下一块还没涂的陆地。程序同理。「最笨」的错误版本是：不记录访问，看到陆地就递归去看四个邻居——邻居又会递归回来，**死循环**；或者对每个陆地都 +1，岛屿数被重复计算。

LC 127 Word Ladder：从 `hit` 一次改一个字母、每个中间词都要在词典里，变成 `cog` 的最短变换长度。最笨的做法：DFS 枚举所有变换序列取最短——路径数是指数级。

### 1.2 慢在哪里 / 错在哪里

- 没有「已访问（visited）」标记 → 同一个点被反复处理（甚至死循环）。
- 求**最短路径**用 DFS → 找到的第一条路径不一定最短，要枚举全部。

> 因果链：把问题建成图（graph）：点（vertex）= 格子 / 单词 / 课程，边（edge）= 「能一步走到」/「必须先于」。 访问标记让每个点只处理一次 → O(V + E)。BFS 一层一层向外扩张，**第一次到达某点的层数就是最短距离**（无权图）→ 最短路径用 BFS。

### 1.3 图是什么（从零讲）

- **图**：点的集合 + 边的集合。边可以有方向（有向图 directed，如「先修课」）或无方向（无向图，如网格里相邻）。
- **邻接表（adjacency list）**：`graph[u] = [v1, v2, ...]`，Python 里用 `dict` 或 `list[list]`。空间 O(V + E)。
- **网格是隐式图**：格子 `(r, c)` 的邻居是 `(r±1, c)`、`(r, c±1)`（4 连通），不用真的建图，写一个 `neighbours` 函数即可。
- **BFS**（广度优先，breadth-first search）：用队列（`deque`），先进先出，一层一层扩张。适合：最短路径（无权）、按层处理、多源同时扩散。
- **DFS**（深度优先，depth-first search）：用栈（递归调用栈或显式 `list`），一条路走到底再回头。适合：连通分量、可达性、环检测、回溯。
- **Python 的递归深度默认 1000**。一个 1000×1000 的全陆地网格，递归 DFS 会 `RecursionError`。面试中要么用 BFS / 显式栈，要么明确说「我会用迭代版本避免栈溢出」。
- **拓扑排序（topological sort）**：有向无环图（DAG）的点排成一行，使每条边都从前指向后。有环则不存在。**Kahn 算法**：反复取出入度（indegree，指向它的边的数量）为 0 的点，删掉它的出边，更新别人的入度。

## 2. 模板与逐行讲解

```python
from collections import deque

# Template G1: BFS by levels (shortest path in an UNWEIGHTED graph; multi-source = many starts at level 0)
def bfs_levels(graph, sources):
    dist = {s: 0 for s in sources}               # dist doubles as the visited set
    queue = deque(sources)
    while queue:
        u = queue.popleft()
        for v in graph.get(u, []):
            if v not in dist:                    # mark when ENQUEUED so a node is queued once
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist

# Template G2: grid neighbours
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
def neighbours(r, c, rows, cols):
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

# Template G3: iterative DFS (no recursion limit) -- same as BFS with a stack
def reachable(graph, start):
    seen, stack = {start}, [start]
    while stack:
        u = stack.pop()
        for v in graph.get(u, []):
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen

# Template G4: topological order with Kahn's algorithm (indegree counting)
def topo_order(n, edges):
    out_edges = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in edges:                           # a must come before b
        out_edges[a].append(b)
        indeg[b] += 1
    queue = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in out_edges[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return order if len(order) == n else None    # None = cycle

g = {"a": ["b", "c"], "b": ["d"], "c": ["d"]}
assert bfs_levels(g, ["a"]) == {"a": 0, "b": 1, "c": 1, "d": 2}
assert bfs_levels(g, ["b", "c"])["d"] == 1       # multi-source
assert sorted(neighbours(0, 0, 2, 2)) == [(0, 1), (1, 0)]
assert reachable(g, "b") == {"b", "d"}
assert topo_order(4, [(0, 1), (0, 2), (1, 3), (2, 3)]) in ([0, 1, 2, 3], [0, 2, 1, 3])
assert topo_order(2, [(0, 1), (1, 0)]) is None
```

逐行讲解：

1. `dist = {s: 0 for s in sources}`：用距离字典**同时当作 visited**；起点距离为 0。多个起点同时入队就是**多源 BFS**（LC 994 腐烂橘子）。
2. `if v not in dist: dist[v] = dist[u] + 1; queue.append(v)`：**入队时就标记已访问**。如果等到出队才标记，同一个点可能被多个邻居重复入队，最坏退化成指数级膨胀。
3. `DIRS` 与 `neighbours`：把边界检查集中在一处；写网格题先写它，避免四处复制 `0 <= nr < rows`。
4. `reachable`（迭代 DFS）：和 BFS 的唯一差别是 `queue.popleft()` 换成 `stack.pop()`。**同一个模板，只换容器。**
5. `topo_order`：`indeg[b] += 1` 统计入度；队列初始放入所有入度为 0 的点；弹出 `u` 后给每个后继入度 −1，减到 0 就入队。结束时 `len(order) == n` 才说明没有环；否则剩下的点都在环上或被环挡住。

## 3. 完整手算（Worked trace）

**拓扑排序**（Kahn）。5 门课，边 `0→1, 0→2, 1→3, 2→3, 3→4`（`a→b` 表示先学 a 再学 b）：

```python
from collections import deque

def kahn_trace(n, edges):
    out_edges = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in edges:
        out_edges[a].append(b)
        indeg[b] += 1
    print("indegree:", indeg)
    queue = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        changed = []
        for v in out_edges[u]:
            indeg[v] -= 1
            changed.append(f"{v}:{indeg[v]}")
            if indeg[v] == 0:
                queue.append(v)
        print(f"pop {u}  decrement {changed or '-'}  queue={list(queue)}  order={order}")
    return order

assert kahn_trace(5, [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]) == [0, 1, 2, 3, 4]
print()

def rotting_trace(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 2)
    fresh = sum(row.count(1) for row in grid)
    minutes = 0
    print(f"minute 0: rotten={list(queue)} fresh={fresh}")
    while queue and fresh:
        newly = []
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
                    newly.append((nr, nc))
        minutes += 1
        print(f"minute {minutes}: newly rotten={newly} fresh={fresh}")
    return minutes if fresh == 0 else -1

assert rotting_trace([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
```

```text
indegree: [0, 1, 1, 2, 1]
pop 0  decrement ['1:0', '2:0']  queue=[1, 2]  order=[0]
pop 1  decrement ['3:1']  queue=[2]  order=[0, 1]
pop 2  decrement ['3:0']  queue=[3]  order=[0, 1, 2]
pop 3  decrement ['4:0']  queue=[4]  order=[0, 1, 2, 3]
pop 4  decrement -  queue=[]  order=[0, 1, 2, 3, 4]

minute 0: rotten=[(0, 0)] fresh=6
minute 1: newly rotten=[(1, 0), (0, 1)] fresh=4
minute 2: newly rotten=[(1, 1), (0, 2)] fresh=2
minute 3: newly rotten=[(2, 1)] fresh=1
minute 4: newly rotten=[(2, 2)] fresh=0
```

前半部分是 Kahn：入度 `[0,1,1,2,1]`，只有 0 的入度为 0，先出。弹出 0 后 1、2 的入度减为 0 入队；弹出 1 时 3 的入度 2→1（还在等 2）；弹出 2 时 3 变成 0 才入队。如果某一步队列空了而 `order` 不足 5 个，就说明有环。

后半部分是多源 BFS（腐烂橘子 `[[2,1,1],[1,1,0],[0,1,1]]`）：每一分钟是 BFS 的一层；`minute 4` 时最后一个新鲜橘子被感染，答案 4。注意循环里 `for _ in range(len(queue))` 是「冻结当前层大小」的惯用法。

## 4. 题目

```python
from collections import defaultdict, deque
```

### 4.1 LC 200 · Number of Islands（Medium）

```python
# solutions/200_number_of_islands.py
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = set()
    islands = 0
    for r0 in range(rows):
        for c0 in range(cols):
            if grid[r0][c0] != "1" or (r0, c0) in seen:
                continue
            islands += 1                                   # new island found: sink all of it
            seen.add((r0, c0))
            queue = deque([(r0, c0)])
            while queue:
                r, c = queue.popleft()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1" and (nr, nc) not in seen:
                        seen.add((nr, nc))                 # mark when ENQUEUED, not when popped
                        queue.append((nr, nc))
    return islands
```

- **一句话洞见**：遇到一块未访问的陆地就岛屿数 +1，然后用 BFS / DFS 把整座岛标记为已访问。
- **复杂度**：时间 O(R·C)，空间 O(R·C)（`seen`；用原地改写可降到队列的大小，但会破坏输入）。

**资深追问**

- **规模 ×1000**：网格放不下内存（比如卫星图 10⁵×10⁵）。做法：切成 tile，每块内部求连通分量，再用**并查集（Union-Find）合并跨 tile 边界相邻的分量**；也可以按行扫描：只保留上一行的标签，O(列数) 内存（图像连通域标注的两遍算法）。
- **流式输入**：「岛屿计数 II」（不断 addLand）：并查集在线合并，每次 O(α(n))。
- **内存**：递归 DFS 在 Python 会爆栈；BFS 的队列最多是一层的宽度。原地把 `'1'` 改成 `'0'` 省 `seen`，但**破坏输入**——要先问。
- **并发**：tile 并行 + 边界合并；BFS 可以做「按层并行」，对 `visited` 用原子 compare-and-set。
- **接口 / 边界**：4 连通还是 8 连通？字符 `'1'` 还是整数 `1`？不规则（ragged）网格？空网格？返回数量还是每个岛的面积 / 坐标？
- **测试**：全水、全陆、棋盘（对角线不连通）、蛇形长岛（测试递归深度）、单格；与基于并查集的另一实现互相对拍。

### 4.2 LC 994 · Rotting Oranges（Medium）

```python
# solutions/994_rotting_oranges.py
def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))                  # ALL rotten oranges start together (level 0)
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh:
        for _ in range(len(queue)):                   # process exactly one level = one minute
            r, c = queue.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1
    return minutes if fresh == 0 else -1
```

- **一句话洞见**：所有腐烂橘子**同时**作为 BFS 的第 0 层；一层 = 一分钟；最后检查是否还有新鲜橘子。
- **复杂度**：时间 O(R·C)，空间 O(R·C)（队列）。

**资深追问**

- **规模 ×1000**：同 200：分块 + 边界处理；BFS 只保留当前层（frontier），内存与前沿大小成正比。
- **流式**：新增腐烂源时，对新源再做一次 BFS（只更新距离变小的格子）——增量最短路。
- **内存**：本实现改写了输入网格（`grid[nr][nc] = 2`）；若要求不修改，使用 `seen` 集合或拷贝。
- **并发**：层同步并行 BFS（level-synchronous）：同一层的节点并行扩展，层与层之间同步。
- **接口**：返回 `-1` 表示不可能；没有新鲜橘子返回 0（即使没有腐烂橘子）；对角线是否传播？
- **测试**：不可达的新鲜橘子（返回 −1）、全空、只有新鲜（−1）、已有多个源同时扩散。

### 4.3 LC 127 · Word Ladder（Hard）

```python
# solutions/127_word_ladder.py
def ladder_length(begin, end, word_list):
    if end not in set(word_list):
        return 0
    buckets = defaultdict(list)                       # "h*t" -> ["hot", "hit", ...]
    for w in set(word_list) | {begin}:
        for i in range(len(w)):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)
    queue = deque([(begin, 1)])
    seen = {begin}
    while queue:
        word, steps = queue.popleft()
        if word == end:
            return steps
        for i in range(len(word)):
            key = word[:i] + "*" + word[i + 1:]
            for nxt in buckets.pop(key, []):          # pop: each bucket is expanded only once
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, steps + 1))
    return 0
```

- **一句话洞见**：用通配符桶 `h*t` 把「只差一个字母」的词归到同一个桶，邻居查找从 O(N·L) 变成 O(L)；然后 BFS 求最短变换链。
- **复杂度**：时间 O(N·L²)（N 个词、长度 L；每个词 L 个桶、每个桶键的构造 O(L)），空间 O(N·L²)。
- **加速**：**双向 BFS**（从起点和终点同时扩张，每次扩张较小的前沿）：搜索量从 b^d 降到约 2·b^(d/2)（b 为分支因子，d 为深度）。

**资深追问**

- **规模 ×1000**：词典 10⁶ 词：桶索引只构建一次，多次查询复用；单次查询用双向 BFS 剪枝。
- **流式**：词典增量更新时，只需把新词加入对应的 L 个桶，已有索引不需要重建。
- **内存**：桶键 `h*t` 总数约 N·L 个；可以用哈希值代替字符串键，或不建桶而逐位尝试 26 个字母（时间 O(N·L·26)，内存更省）。
- **并发**：索引只读，多个查询并行；单次 BFS 做层同步并行。
- **接口**：`beginWord` 不必在词典里；`endWord` 不在词典里返回 0；返回长度（长度含起点，所以 +1）还是具体路径（LC 126，需要记录父指针并回溯所有最短路径）？
- **测试**：终点不在词典、起点等于终点、词典很小、存在多条等长路径（对拍一个朴素 BFS）。

### 4.4 LC 207 · Course Schedule（Medium）；附 LC 210

```python
# solutions/207_course_schedule.py
def can_finish(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:            # edge pre -> course
        graph[pre].append(course)
        indegree[course] += 1
    queue = deque(c for c in range(num_courses) if indegree[c] == 0)
    taken = 0
    while queue:
        c = queue.popleft()
        taken += 1
        for nxt in graph[c]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:               # all of nxt's prerequisites are done
                queue.append(nxt)
    return taken == num_courses                  # leftover nodes sit on a cycle


def find_order(num_courses, prerequisites):      # LC 210: same loop, keep the order
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    queue = deque(c for c in range(num_courses) if indegree[c] == 0)
    order = []
    while queue:
        c = queue.popleft()
        order.append(c)
        for nxt in graph[c]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == num_courses else []
```

- **一句话洞见**：能修完所有课 ⟺ 依赖图无环 ⟺ Kahn 算法能取出全部 n 个点。LC 210 只需要把出队顺序记录下来。
- **复杂度**：时间 O(V + E)，空间 O(V + E)。
- **DFS 三色标记**是另一种解法（白 / 灰 / 黑；碰到灰色点 = 有环），但递归深度同样可能超过 1000。

**资深追问**

- **规模 ×1000**：线性；边多时用紧凑的数组表示（CSR）。图放不下内存：外存图计算（按点的出入度分块），或分布式（Pregel 式迭代）。
- **流式 / 在线**：边不断加入，要实时判环 → 动态拓扑排序（如 Pearce–Kelly 算法）或每次新增边 `u→v` 检查 `v` 能否到达 `u`。
- **内存**：邻接表 O(V + E)；入度数组 O(V)。
- **并发**：Kahn 天然并行：每一轮中所有入度为 0 的点互不依赖，可同时执行——这就是构建系统（make / Bazel）并行调度任务的原理。
- **接口**：只返回布尔值，还是返回一个合法顺序（210）？有环时是否要**报告环上的点**（排查依赖用，比单纯 `False` 有用得多）？重复边、自环（`[0,0]`）、课程编号越界怎么办？
- **测试**：随机生成 DAG（先随机排列再只允许从前向后连边）必须返回 True，再加一条反向边必须返回 False；自环、菱形（diamond）、空依赖。

### 4.5 LC 269 · Alien Dictionary（Hard）

```python
# solutions/269_alien_dictionary.py
def alien_order(words):
    graph = {ch: set() for w in words for ch in w}        # every letter is a node, even with no edges
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                graph[x].add(y)                           # first difference decides: x < y
                break
        else:
            if len(a) > len(b):                           # "abc" before "ab" is impossible
                return ""
    indegree = {ch: 0 for ch in graph}
    for ch in graph:
        for nxt in graph[ch]:
            indegree[nxt] += 1
    queue = deque(ch for ch in graph if indegree[ch] == 0)
    out = []
    while queue:
        ch = queue.popleft()
        out.append(ch)
        for nxt in graph[ch]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return "".join(out) if len(out) == len(graph) else ""   # cycle -> no valid order
```

- **一句话洞见**：把「相邻两个词的第一个不同字母 `x ≠ y`」读成一条边 `x → y`，字母顺序就是这个图的拓扑序。
- **两个陷阱**：(1) 前缀违规：`"abc"` 排在 `"ab"` 前面是不可能的 → 返回 `""`；(2) 没有任何约束的字母也必须出现在结果里（先给所有字母建点）。
- **复杂度**：时间 O(总字符数 + 字母数²)，空间 O(字母数²)。

**资深追问**

- **规模 ×1000**：只比较相邻词，边数最多是 `词数 × 词长`，去重后 ≤ 字母表大小²；线性于输入。
- **流式**：词按序流入时，每对相邻词增量产生边，增量拓扑排序；有环时可立刻报告冲突的那一对词。
- **内存**：边集合存成 `set`（去重），字母表小。
- **并发**：边的提取可以按相邻对并行，合并边集合后再做拓扑排序。
- **接口**：答案不唯一（无约束字母的相对顺序任意）——要和面试官确认返回任意一个合法顺序；非法输入（环、前缀违规）返回 `""` 还是抛异常；字符集是小写字母还是 Unicode。
- **测试**：**不要断言唯一输出**（除非约束完全确定），而是写一个验证器：检查输出是否包含所有字母、且按这个顺序相邻词确实有序；加上环、前缀违规、单个词、重复词的用例。

## 5. 常见 bug

1. **出队时才标记 visited**：同一个点被多次入队，最坏指数级膨胀 / 重复计数。入队时标记。
2. **BFS 数层数时少一或多一**：Word Ladder 的长度包含起点（所以起点层数从 1 开始）；Rotting Oranges 在没有新鲜橘子时要返回 0（用 `while queue and fresh`）。
3. **递归 DFS 爆栈**：Python 默认递归深度 1000。用迭代，或 `sys.setrecursionlimit`（后者有风险，要说明）。
4. **网格题邻居越界**：`0 <= nr < rows and 0 <= nc < cols`，注意是 `and`；列数用 `len(grid[0])`。
5. **拓扑排序忘记检测环**：最终 `len(order) != n` 就是有环。
6. **边的方向弄反**：`prerequisites = [course, pre]` 的边是 `pre → course`。
7. **Alien Dictionary 漏掉前缀情况** 或 **只给出现在边里的字母建点**。
8. **修改了正在遍历的网格但没告诉面试官**：原地标记很常用，但要明说。

## 6. 自测题

1. 为什么求无权最短路用 BFS 不用 DFS？
   <details><summary>答案</summary>BFS 按距离从小到大一层一层访问，第一次访问某点时的层数就是最短距离；DFS 先走到的路径不一定短，需要枚举所有路径。</details>
2. 「入队时标记」和「出队时标记」有什么区别？
   <details><summary>答案</summary>出队时标记会让一个点在被弹出前被多个邻居重复入队（队列膨胀，甚至在有环图上不停增长）；入队时标记保证每个点最多入队一次，总时间 O(V + E)。</details>
3. Kahn 算法结束后 `len(order) < n` 说明什么？
   <details><summary>答案</summary>图里有环：环上每个点的入度都被环上的前驱占着，永远减不到 0。</details>
4. 小编程：用 BFS 求网格中从左上到右下的最短路径长度（`0` 可走，`1` 是墙，4 连通）。
   <details><summary>答案</summary>`queue = deque([(0,0,1)])`；`seen = {(0,0)}`；每次弹出 `(r,c,d)`，到终点返回 `d`；邻居可走且未访问则入队 `d+1` 并标记。起点或终点是墙则返回 −1。O(R·C)。</details>
5. 多源 BFS 和单源 BFS 的区别？
   <details><summary>答案</summary>只是初始时把多个源点一起放入队列（距离都为 0）；其余完全相同。等价于加一个连向所有源点的虚拟超级源。</details>
6. 资深追问：构建系统有 10 万个任务和依赖，怎么调度才能最大化并行度？
   <details><summary>答案</summary>Kahn 的分层版本：每一层的所有入度为 0 的任务可以并行执行；用线程池 / 工作队列，任务完成后对后继的入度做原子减 1，减到 0 就提交。还要考虑关键路径（critical path）、失败重试、缓存命中。</details>
