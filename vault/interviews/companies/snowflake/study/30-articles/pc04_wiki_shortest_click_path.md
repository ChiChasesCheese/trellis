# pc04 · Wiki Shortest Click Path：练的是"最短路径要字典序最小，就先反向 BFS"

> [!tldr]
> - Part 1、Part 2 有来源（fastprep Phone Screen 2026-09 + OA/电面双池）；**Part 3 抓取可能失败的懒加载爬虫是 (reconstructed)**
> - 这题考的是：有向图 BFS 最短点击数 → 所有最短路径里字典序最小的那条 → 边要现抓且可能失败
> - 三步套路：正向 BFS 求距离 → 从终点**反向** BFS 求"到终点距离"，再从起点每步选"距离减 1 的最小邻居" → 懒加载时失败页当死路计数
> - 最值得带走的一个模式：**"正向贪心每步选最小邻居"是错的**——它可能走进死胡同；反向距离表保证每一步都还在某条最短路上

## 1. 题目在说什么（人话版)

页面之间有超链接（有向边）。从 A 页点到 D 页最少点几次？Part 2：最短的走法可能有好几条，要名字拼起来字典序最小的那条。Part 3：你手上没有整张图，只能一页一页去抓链接，抓取可能失败——失败的页当作没有出链，记下失败次数，但不能停。

小例子（Part 2）：
```
A→B, A→C, B→D, C→D
最短 2 步；两条最短路 A,B,D 和 A,C,D → 选 A,B,D
```

## 2. 读题：把文字变成模型

- **输入格式**：第一行边数 e，随后恰好 e 行 `u v`，最后一行 `start end`（**先数边数**，这是本题测试曾经写错过的地方）。
- **输出**：Part 1 距离（不可达 -1）；Part 2 逗号分隔路径（不可达空行）；Part 3 路径（不可达 `-`）+ 失败次数。
- **状态**：邻接表、访问集合、Part 2 的反向图与 `dist_to_end`、Part 3 的 `parent` 表。
- **一句话建模**：这是一个 **"无权有向图最短路 + 确定性路径重建"** 问题。

> [!note] 为什么正向贪心不对
> 从 A 出发，名字最小的邻居是 B，但 B 可能到不了 D，或者经过 B 要多走一步。BFS 定下的距离不会回头改，所以"先选最小的走下去"没有回溯机会。反向 BFS 先告诉你"每个节点离终点还有几步"，正向时只在"还剩 k−1 步"的邻居里挑最小，就一定在最短路上。

## 3. 下笔顺序

1. **问清**：有向还是无向？`start == end` 返回什么？字典序按元素比较还是按拼接字符串比较？
2. **Part 1**：BFS，扩展到 end 时返回 `d+1`；`start == end` 返回 0。
3. **Part 2**：建反向图；从 end 反向 BFS 得 `dist_to_end`；start 不在表里 → 空；否则从 start 往前走，每步 `min(n for n in graph[cur] if dist_to_end.get(n) == dist_to_end[cur] − 1)`。
4. **Part 3**：出队时才 `fetch(node)`，异常计数 `continue`；新邻居**排序后**入队，首次发现即定 parent；到 end 回溯 parent。
5. **收尾**：说清 Part 3 为什么不再保证全局字典序最小（拿不到整张图，无法反向 BFS）。

## 4. 代码怎么组织

```
shortest_path_length(graph, s, e)     # Part 1
_reverse_graph(graph)
shortest_path(graph, s, e)            # Part 2：反向 BFS + 正向挑最小
crawl_shortest_path(fetch, s, e)      # Part 3：懒加载 + 失败计数
_read_graph / part1..part3            # 边数先行的解析
```

## 5. 核心代码骨架

```python
def shortest_path(graph, start, end):
    if start == end:
        return [start]
    rev = {}
    for u, vs in graph.items():
        for v in vs:
            rev.setdefault(v, []).append(u)
    dist = {end: 0}; q = deque([end])
    while q:
        x = q.popleft()
        for p in rev.get(x, []):
            if p not in dist:
                dist[p] = dist[x] + 1; q.append(p)
    if start not in dist:
        return []
    path, cur = [start], start
    while cur != end:
        cur = min(n for n in graph.get(cur, []) if dist.get(n) == dist[cur] - 1)
        path.append(cur)
    return path

def crawl_shortest_path(fetch, start, end):
    if start == end:
        return [start], 0
    seen, parent, fails, q = {start}, {}, 0, deque([start])
    while q:
        node = q.popleft()
        try:
            nbrs = fetch(node)
        except Exception:
            fails += 1; continue                  # 失败页当死路，不中断
        for nxt in sorted(nbrs):
            if nxt not in seen:
                seen.add(nxt); parent[nxt] = node
                if nxt == end:
                    path = [end]
                    while path[-1] != start:
                        path.append(parent[path[-1]])
                    return path[::-1], fails
                q.append(nxt)
    return [], fails
```

## 6. 每个 part 叠加什么

| Part | 改动 | 保证 |
|---|---|---|
| 1 | BFS 距离 | 最短 |
| 2 | 反向距离表 + 正向挑最小 | 最短且全局字典序最小 |
| 3 | 懒加载、失败计数 | 最短（某一条），不保证全局字典序最小 |

## 7. 常见坑

- 正向贪心选最小邻居（测试专门构造"小名字邻居通向死胡同"的图）。
- `start == end` 三个 part 的返回值。
- Part 3 起点本身抓取失败：空路径、失败数 1。
- Part 3 失败后没继续处理队列里其它页。
- 输入解析：边数与实际行数必须一致。

## 8. 追问怎么接

1. **图很大、只关心一对页面？** 双向 BFS，从两端同时扩展，层数减半。
2. **Part 3 也要全局字典序最小？** 先懒加载把 BFS 距离范围内的子图抓全，再在子图上做 Part 2；代价是多抓页面。
3. **抓取有速率限制、可重试？** 失败页进入重试队列带退避；重试上限后当死路。
4. **分布式爬虫？** 按域名分片的前沿队列、全局去重（Bloom filter）、礼貌性限速——就是 `sd10`。

## 9. 自测清单

- [ ] 构造一个正向贪心出错的图
- [ ] 写出反向 BFS + 正向挑最小
- [ ] 说清 Part 3 为什么保证弱于 Part 2

## 相关题与 skills

S05 图 BFS / 路径重建 · S08 同复杂度下加强保证。相关：`q10` Wiki Min Clicks（OA 版）、`pc02` 多源 BFS、`sd10` 并发爬虫。
