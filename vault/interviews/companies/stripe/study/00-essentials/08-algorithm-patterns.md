# 08 · 算法模式识别 + 模板代码

> 面向 phone screen 和 onsite（qA01–qA13 那一组），以及 bespoke 题里嵌的算法部分。
> 每个模式：**什么信号触发它 → 模板 → 最易错处**。

---

## 0. 先看数据规模，再选算法

| n 的量级 | 允许的复杂度 | 典型技术 |
|---|---|---|
| n ≤ 12 | O(n!) / O(2ⁿ·n) | 全排列、状压 DP |
| n ≤ 20 | O(2ⁿ) | 子集枚举、状压 |
| n ≤ 500 | O(n³) | Floyd、区间 DP |
| n ≤ 5·10³ | O(n²) | 二维 DP、朴素两重循环 |
| n ≤ 10⁵ | O(n log n) | 排序、堆、二分、并查集 |
| n ≤ 10⁶ | O(n) | 单趟扫描、前缀和、计数 |

**Python 的常数**：大约 10⁷ 次简单操作/秒。10⁶ 条记录的 O(n log n) 排序没问题（~1 s），
10⁵ 条的 O(n²) 就是 10¹⁰ —— 必挂。**写代码前先做这个乘法。**

---

## 1. 前缀和 / 后缀和

**信号**：「在某个位置切一刀，左边一种代价、右边另一种代价，求最优切点」、
「区间和查询」、「最佳关闭时间」。

```python
# 答案空间是 [0, n]（比元素多一个！），平手取最小下标
pre = [0] * (n + 1)                      # pre[i] = a[0..i-1] 之和
for i, x in enumerate(a):
    pre[i + 1] = pre[i] + x
best_i, best_v = 0, cost(0)
for i in range(1, n + 1):
    v = cost(i)
    if v < best_v:                        # 严格小于 = 平手保留更小的 i
        best_i, best_v = i, v
```

**最易错**：
- 答案空间是 `[0, n]` 不是 `[0, n-1]`（"在第一个元素之前关门"和"在最后一个之后关门"都合法）。
- 平手取最小下标 → 更新条件必须是**严格**小于。
- **差分数组**：区间加 `d[l] += v; d[r+1] -= v`，最后前缀和还原。

---

## 2. 双指针 / 滑动窗口

**信号**：「连续子数组/子串」、「最短覆盖」、「窗口内至多 K 个」。

**变长窗口（右扩左缩）**：

```python
left, best = 0, INF
for right, x in enumerate(a):
    add(x)
    while violates():          # 违反不变量就缩左边
        remove(a[left]); left += 1
    if valid():
        best = min(best, right - left + 1)
```

**时间戳窗口**（不是下标窗口）用 `deque`，见 `05-time-and-intervals.md` §5。

**最易错**：
- 窗口边界 `<` 还是 `<=`。
- 缩窗的 `while` 写成了 `if`（一次只能缩一格是错的）。
- 求「最短覆盖」时，答案要在 `while` **里面**更新，不是外面。

---

## 3. 二分

**两种用法，别混：**

**① 在有序数组上找位置** → 直接用 `bisect`，不要手写。

**② 在答案空间上二分**（信号：「最小化最大值」、「最大化最小值」、「是否可行随参数单调」）：

```python
lo, hi = 0, HI                       # 循环不变量：答案在 [lo, hi] 内
while lo < hi:
    mid = (lo + hi) // 2             # 找最小可行解时向下取整
    if feasible(mid):
        hi = mid                     # mid 可行 → 答案 <= mid
    else:
        lo = mid + 1
return lo
```

**最易错**：
- 找**最大**可行解时要用 `mid = (lo + hi + 1) // 2`，否则死循环。
- `feasible` 必须**单调**（可行的都在一侧）。不单调就不能二分。
- 上界 `HI` 要取得足够大（取一个显然可行的值）。

---

## 4. 贪心

**信号**：「最少次数」、「最多能安排多少个」、「按某个顺序处理就最优」。

**做法**：先想出排序键，再想**为什么这个键是对的**（交换论证：
把最优解里相邻两个逆序的元素交换，结果不会变差）。

**经典排序键**：
- 区间调度求最多不重叠 → 按 **end 升序**。
- 区间合并 → 按 **start 升序**。
- 最少箭射爆气球 → 按 **end 升序**。
- 任务调度带截止 → 按 **deadline 升序** + 堆维护已选。

**最易错**：贪心是**需要证明**的。想不出交换论证时，先写 DP/暴力对拍。
面试中说「我先写个 O(n²) DP 保底，再论证贪心」是加分项，不是减分项。

---

## 5. BFS / DFS / 连通分量

```python
from collections import deque

def bfs(g, src):
    dist = {src: 0}
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v in g[u]:
            if v not in dist:              # 入队时就标记，不是出队时
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist
```

**迭代 DFS**（10⁵ 节点必须迭代，递归会爆栈）：

```python
stack, seen = [src], {src}
while stack:
    u = stack.pop()
    for v in g[u]:
        if v not in seen:
            seen.add(v); stack.append(v)
```

**最易错**：
- **入队时标记 visited**，出队时标记会让同一个节点重复入队 → 退化成指数级。
- BFS 只在**无权图**（或全 1 权）上给最短路。
- 递归深度默认 1000。

---

## 6. 并查集（DSU）

**信号**：「分组」、「共享某个标识符的算同一伙」、「连通分量个数」、「是否成环」。

```python
class DSU:
    def __init__(self):
        self.p = {}
        self.sz = {}
    def find(self, x):
        self.p.setdefault(x, x); self.sz.setdefault(x, 1)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]     # 路径压缩（半路压缩）
            x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        if self.sz[ra] < self.sz[rb]: ra, rb = rb, ra
        self.p[rb] = ra; self.sz[ra] += self.sz[rb]
        return True
```

**建图的关键洞察**：「共享 email / 设备 / 银行卡的用户算一伙」，
**不要**在用户之间两两连边（O(k²)）。建**二部图**：用户 ↔ 标识符，
每个标识符把它的所有用户 union 到一起（O(k)）。

```python
for user, ident in pairs:
    dsu.union(("U", user), ("I", ident))       # 用带前缀的元组避免命名冲突
```

分组输出：

```python
groups = defaultdict(list)
for u in users:
    groups[dsu.find(("U", u))].append(u)
result = sorted([sorted(g) for g in groups.values() if len(g) >= MIN_SIZE])
```

---

## 7. 最短路

**Dijkstra**（非负权，求单源最短）：

```python
import heapq
def dijkstra(g, src):
    dist = {src: 0}
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, INF): continue      # 惰性删除过期条目
        for v, w in g[u].items():
            nd = d + w
            if nd < dist.get(v, INF):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist
```

**Bellman-Ford 按轮**（有跳数上限 ≤ K —— **Dijkstra 在这里是错的**）：

```python
def cheapest_k_stops(n, flights, src, dst, K):
    dist = [INF] * n; dist[src] = 0
    for _ in range(K + 1):                     # K 次中转 = K+1 条边
        prev = dist[:]                         # ← 必须用上一轮的副本
        for u, v, w in flights:
            if prev[u] + w < dist[v]:
                dist[v] = prev[u] + w
    return dist[dst] if dist[dst] < INF else -1
```

**为什么必须用 `prev` 副本**：不复制的话，同一轮里 `u` 的更新会立刻被 `v` 用上，
一轮就走了多跳，跳数限制失效。**这是这道题唯一的难点。**

**乘积权重**（汇率、除法求值）：把 `+w` 换成 `*w`，求最大乘积时用最大堆
（或取 `-log` 转成最短路）。反向边是 `1/w`。

---

## 8. 拓扑排序 / 带权 DAG

```python
from collections import deque
def topo_longest(n, edges, w):        # w[v] = 节点 v 自身的耗时
    g = defaultdict(list); indeg = [0] * n
    for u, v in edges:
        g[u].append(v); indeg[v] += 1
    finish = [0] * n
    dq = deque(u for u in range(n) if indeg[u] == 0)
    for u in list(dq): finish[u] = w[u]
    seen = 0
    while dq:
        u = dq.popleft(); seen += 1
        for v in g[u]:
            finish[v] = max(finish[v], finish[u] + w[v])
            indeg[v] -= 1
            if indeg[v] == 0: dq.append(v)
    if seen != n: raise ValueError("cycle")     # 有环
    return max(finish)
```

**最易错**：
- 起点是**所有**入度为 0 的点，不是某一个。
- 有环的判据是「出队总数 < n」。
- `finish[v] = max(...)` 要在**每次**松弛时更新，不是入度归零时才算。

---

## 9. 动态规划

**四问法**（面试时说出来）：
1. **状态**是什么？（`dp[i][j]` 表示什么，一句话说清）
2. **转移**是什么？
3. **初值**是什么？
4. **答案**在哪个格子？

**一维**（如打家劫舍、最大子段和）：滚动变量即可，O(1) 空间。

**状压 DP**（n ≤ 20）：

```python
from functools import lru_cache
@lru_cache(maxsize=None)
def solve(mask):                       # mask 的第 i 位 = 第 i 个已处理
    if mask == FULL: return 0
    ...
```

**带状 DP**（编辑距离 ≤ k）：只算主对角线附近 `2k+1` 条带，O(nk) 而不是 O(n²)。

**最易错**：`lru_cache` 的参数必须可哈希（不能是 list / dict）。
用 `tuple` 或整数 mask。

---

## 10. 回溯 / 枚举

```python
def backtrack(i, path, out):
    if i == n:
        out.append(path[:]); return       # path[:] 复制！否则全是同一个引用
    for choice in options(i):
        if not ok(choice, path): continue  # 剪枝越早越好
        path.append(choice)
        backtrack(i + 1, path, out)
        path.pop()                        # 回溯
```

**计数而不枚举**：要「有多少种」时不要真的生成，用乘法原理递推。
要「第 k 个」时用**排名法**：逐位确定，每位算出以该字符开头的方案数，
k 大于它就减掉、换下一个字符。

**最易错**：
- `out.append(path)` 忘了 `[:]` → 所有结果都是最后那个。
- 剪枝改变了最优性（剪掉了可能更优的分支）。
- 输出要求排序 / 去重时，别忘了最后 `sorted(set(...))`。

---

## 11. 字符串

**Luhn 校验**（从右往左，偶数位×2，>9 减 9）：

```python
def luhn_ok(num: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(num)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9: d -= 9
        total += d
    return total % 10 == 0
```

**一次编辑距离**（LC 161）：

```python
def one_edit(a, b) -> bool:
    if abs(len(a) - len(b)) > 1: return False
    if len(a) > len(b): a, b = b, a          # 保证 len(a) <= len(b)
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return a[i+1:] == b[i+1:] if len(a) == len(b) else a[i:] == b[i+1:]
    return len(a) + 1 == len(b)              # 前缀全同 → 只能是末尾多一个
```

**注意**：完全相同时返回 `False`（"one edit" 是**恰好一次**）。

**通配符补全**：`itertools.product("0123456789", repeat=k)`，k ≤ 6 才行。

---

## 12. 结算 / 匹配

**最少转账次数结清债务**（LC 465）：

```python
# ① 先净额化 —— 这一步是关键，不做就没法算最优
net = defaultdict(int)
for frm, to, amt in txs:
    net[frm] -= amt; net[to] += amt
debts = [v for v in net.values() if v != 0]

# ② DFS + 剪枝（n <= 12）
def dfs(i):
    while i < len(debts) and debts[i] == 0: i += 1
    if i == len(debts): return 0
    best = INF
    for j in range(i + 1, len(debts)):
        if debts[i] * debts[j] < 0:            # 只和异号的配对（剪枝）
            debts[j] += debts[i]
            best = min(best, 1 + dfs(i + 1))
            debts[j] -= debts[i]
    return best
```

**FIFO 消耗批次**（积分、库存）：按时间排序，从最早的批次开始扣：

```python
from collections import deque
lots = deque(sorted(lots, key=lambda l: l.ts))
while need > 0 and lots:
    lot = lots[0]
    take = min(need, lot.amount)
    lot.amount -= take; need -= take
    if lot.amount == 0: lots.popleft()
```

**最少负载分配**（堆 + 惰性删除）：见 `03-python-cheatsheet.md` §3。

---

## 13. 模式识别速查

| 题面出现 | 想到 |
|---|---|
| "连续的子数组/子串" | 滑动窗口 / 前缀和 |
| "区间和查询" | 前缀和 |
| "在某点切开" | 前缀 + 后缀 |
| "最少 / 最多多少个" | 贪心（先想排序键）或 DP |
| "最小化最大值" | 二分答案 |
| "分组 / 一伙 / 团伙" | 并查集 |
| "依赖 / 先修课 / 编译顺序" | 拓扑排序 |
| "最短 / 最便宜的路径" | BFS（无权）/ Dijkstra（正权）/ Bellman-Ford（有跳数限制） |
| "至多 K 次中转" | **Bellman-Ford 按轮**（不是 Dijkstra） |
| "有多少种方案" | DP 或组合计数 |
| "第 k 个" | 排名法，不要枚举 |
| "n ≤ 20" | 状压 / 子集枚举 |
| "最近使用 / 淘汰" | LRU（OrderedDict） |
| "某时刻的值" | 按 key 存有序版本列表 + `bisect` |
| "最闲的服务器 / top-k" | 堆 + 惰性删除 |
| "结清债务 / 最少转账" | 先净额化，再 DFS 剪枝 |
| "FIFO 消耗" | `deque` |
