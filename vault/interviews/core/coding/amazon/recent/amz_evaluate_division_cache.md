# 除法求值与缓存追问（Evaluate Division, caching follow-up）

给一组等式，如 `a / b = 2`、`b / c = 3`，再给一批查询，如 `a / c = ?`，要求出每个查询的值，推不出来就返回 -1.0。把变量当图的节点、等式当边，查询就是找一条路径再把边上的乘数连乘（LeetCode 399）。这一讲的重点是后续问题：同一批等式上被反复查询时怎样加速，以及新等式加入后缓存里哪些结果还能信。

## 题面与约束
给方程 `Ai / Bi = values[i]` 和查询 `Cj / Dj`，求每个查询的值，无法确定返回 -1.0。
约束：`1 <= equations.length <= 20`，`1 <= Ai.length, Bi.length <= 5`，`0.0 < values[i] <= 20.0`，`1 <= queries.length <= 20`，字符串由小写字母和数字组成。

## 开场先问的澄清问题
1. 方程会不会互相矛盾？（题面保证不矛盾。）
2. 查询的变量没出现过，返回 -1.0 吗？
3. 同一批方程上会被**反复查询**吗？方程会**在线新增**吗？

## 基础回顾
把每个变量当节点，等式 a/b=v 当两条边：a→b 的乘数 v，b→a 的乘数 1/v。查询 x/y 就是在图里找 x 到 y 的任意一条路径，乘上路径上所有边的乘数（因为方程一致，路径任选）。BFS 一次 O(V+E)。

## 缓存：想清楚三件事
1. **缓存什么**：键 (x, y) → 结果。已知值缓存，未知（-1.0）也缓存，否则对不连通的查询，每次都要完整 BFS 一遍才能发现无解。
2. **反向免费**：x/y 求出后，y/x = 1/(x/y) 一并放进缓存，反向查询不用再算。
3. **新增等式时怎么失效**：
   - 已缓存的**确定值**是由旧方程推出的，新增方程不会改变它（前提是方程自洽）。所以**保留**。
   - 已缓存的 **-1.0**（未知）可能因为新方程把两个连通块连起来而变成已知。所以**只删掉未知项**。
   - 这比「新增一条就清空整个缓存」好得多，也比「永不失效」正确。

### 为什么不「全清」或「全不清」
全清：每次新增都丢掉全部已知值，写多读多的场景白白重算。不清：新增方程后，对不连通的旧结果仍返回 -1.0，答案错。

```python
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
```

示例：加入 `a/b=2`，`b/c=3`。`query(a,c)=6.0`（BFS 一次）；再次 `query(a,c)` 与 `query(c,a)=1/6` 都命中缓存，BFS 次数不变。`query(a,x)` 得 -1.0（缓存了未知）；加入 `c/x=4` 后再次 `query(a,x)=24.0`（未知项被清掉，重新 BFS）；而 `query(a,c)` 仍命中缓存。

## 与带权并查集的比较
- 带权并查集（weighted union-find）：每个元素存「它相对代表元的乘数」。每次 `find` 均摊 O(α(n))，路径压缩把「到根的乘数」存下来，**本身就是缓存**。新增方程只是一次 union，不需要任何失效逻辑。
- 缓存 + BFS：实现直观，适合方程不变的静态批量查询；在线新增时必须做上面的选择性失效。
- 选择：读多写多的在线场景直接用带权并查集；如果被问到「缓存」，先说并查集本身就免除了缓存失效问题，再展示缓存方案的失效规则。

## 复杂度
BFS 未命中：O(V+E)；命中：O(1)；缓存内存 O(查询对数)，可以用 LRU 限制。

## senior 追问
1. **缓存大小要限制**：LRU（`OrderedDict`）；未知项的 TTL 可以更短，因为它们更可能因新方程而失效。
2. **多线程读写**：读多写少用读写锁；或者写时复制（copy-on-write）整个图快照，缓存和图版本号一起走，旧版本的缓存自然作废。
3. **新增矛盾方程**：检测 `ratio` 不一致就拒绝或报错（并查集版本里已有 `inconsistent equation` 检查）。
4. **精度问题**：浮点连乘误差累积；可以用分数 `Fraction`，或对数域相加。
5. **分布式（方程分片在多台机器上）**：按连通分量分片；跨分片查询先在路由层判断是否同分量。
6. **按需精确失效**：新方程只会合并两个连通分量，因此可以只清除「一个端点在分量 A、另一个在分量 B」的未知项，需要维护变量到分量的映射。

## 自测题
1. 新增方程后，为什么已缓存的确定值不用删？
<details><summary>答案</summary>它们由旧方程推出，且方程自洽，新方程不会改变这些比值，只会让更多比值变成可知。</details>
2. 为什么也要缓存 -1.0？
<details><summary>答案</summary>否则不连通的查询每次都要完整 BFS 才能发现无解。</details>
3. 缓存里 `1 / ans` 在什么条件下不能算？
<details><summary>答案</summary>`ans == 0` 时除零；values 都大于 0 所以不会发生，代码仍做了保护。</details>
