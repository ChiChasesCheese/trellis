# 公交路线（Bus Routes, LC 815）

城市里有若干条环线公交，`routes[i]` 是第 i 路车循环经过的站点。你从 `source` 站出发，想到 `target` 站，每上一辆车算一次乘车。问最少乘几次车；到不了返回 -1。难点在于「代价」的定义：代价按上车次数算，而不是按经过多少站算，所以普通的「站点图 BFS」不能直接用。

## 题面与约束
`routes[i]` 是第 i 路公交循环经过的站点；从 `source` 站出发，每次**上一辆车**算一次乘车，问到 `target` 的最少乘车次数，到不了返回 -1。
约束：`1 <= routes.length <= 500`，`1 <= routes[i].length <= 10^5`，`sum(routes[i].length) <= 10^5`，站点编号 `0..10^6-1`，`routes[i]` 内元素互不相同。

## 开场先问的澄清问题
1. 起点等于终点时返回 0 吗？（是。）
2. 同一站可以有多路车经过吗？可以换乘多次吗？
3. 求的是乘车次数而不是站数，对吗？（对。）

## 先补一点基础：把「谁是节点」想清楚
BFS 求最少步数的前提是**一步的代价是 1**。这里的代价是「上车一次」，不是「走一站」。如果把站点当节点，同一路车上的相邻站之间的边代价是 0（不用下车），而换乘才是 1，边权不统一，普通 BFS 给不出正确答案。解决办法有两个：把**车（route）当节点**，或者用 0-1 BFS。下面选前者，因为它让每条边的代价都是 1。

## 最笨解
把每对「有共同站点的路线」连边，建路线图，再 BFS。建图要比较 500² 对路线各自的站点集合，最坏 O(500²·L)，L 是路线长度；比直接从站点入手还慢。

## 逐步改进
1. **问题**：两两比较太慢。
2. **想法**：建倒排索引 `stop -> [经过它的 route]`。一个站点上的所有路线互相可以换乘，不需要两两比较。
3. **BFS**：队列里放 (route, 乘车次数)。出队一条路线后，遍历它的每个站点：若是 target 就返回当前次数；否则把这个站点上还没访问的路线全部入队（次数 +1）。
4. **关键剪枝**：站点也要打 visited。一个站点被展开过一次，它上面的所有路线已经入队了，再展开是重复劳动。没有这条剪枝，一个被 500 路车共有的站点会被展开 500 次，退化成 O(500·sum(len))。
5. 起点的第一批路线次数是 1；起点等于终点特判为 0，因为次数从 1 起算（已经上了第一辆车），不特判会得到错误结果。

```python
def num_buses_to_destination(routes, source, target):
    if source == target:
        return 0
    stop_to_routes = {}
    for i, route in enumerate(routes):
        for stop in route:
            stop_to_routes.setdefault(stop, []).append(i)
    queue = deque((r, 1) for r in stop_to_routes.get(source, []))
    seen_routes = {r for r, _ in queue}
    seen_stops = {source}
    while queue:
        r, rides = queue.popleft()
        for stop in routes[r]:
            if stop == target:
                return rides
            if stop in seen_stops:                        # every route through this stop was queued already
                continue
            seen_stops.add(stop)
            for nxt in stop_to_routes[stop]:
                if nxt not in seen_routes:
                    seen_routes.add(nxt)
                    queue.append((nxt, rides + 1))
    return -1
```

示例：`[[1,2,7],[3,6,7]]`，1 到 6：先坐路线 0 到 7，再换路线 1 到 6，答案 2。`[[7,12],[4,5,15],[6],[15,19],[9,12,13]]` 从 15 到 12：15 只能到 {4,5,15,19}，永远到不了 12，答案 -1。

## 复杂度
设 S = sum(len(routes[i]))，R = routes.length。建索引 O(S)；每个站点至多展开一次，每条路线至多入队一次，总 O(S + R) 的集合操作（加上字典均摊）。

## senior 追问
1. **站点编号很大（1e6）**：用字典索引（上面的代码已是），不要开 1e6 长度的数组。
2. **在线查询很多个 (source, target) 对**：预处理路线图的连通分量（并查集），不同分量直接 -1；同分量再 BFS。
3. **要输出换乘方案**：BFS 时记录每条路线的前驱路线和换乘站点，回溯。
4. **有等车时间或班次表**：边权变成时间，BFS 换成 Dijkstra，状态扩展成 (stop, 时间)。
5. **路线是单向且不循环**：站点的出边只指向后续站点；索引里要存「该站在路线中的位置」，展开时只遍历该位置之后的站点。
6. **双向 BFS**：从 source 和 target 同时扩，路线数 500 时收益有限，但站点数巨大时有用。

## 自测题
1. 为什么节点选「路线」而不是「站点」？
<details><summary>答案</summary>同一路线上任意两站之间不需要换乘（代价 0），换乘才代价 1；以路线为节点后每条边代价都是 1，普通 BFS 即可。</details>
2. 删掉 `seen_stops` 会怎样？
<details><summary>答案</summary>结果仍然正确，但共用站点会被重复展开，最坏每个站点展开「经过它的路线数」次，时间退化。</details>
3. `source == target` 为什么要单独处理？
<details><summary>答案</summary>BFS 里次数从 1 起算（上了第一辆车），不特判会返回 1 或 -1。</details>

## 来源
- Hello Interview 社区题目 `bus-routes-815`，约 2026-09-20，中级 APAC：https://www.hellointerview.com/community/questions/bus-routes-815 ；公司页 https://www.hellointerview.com/community/questions?company=Amazon 。报告只记录了题目名「Leetcode 815. Bus Routes」，摘要为 find the minimum number of bus rides from source to target。
- LC 官方 https://leetcode.com/problems/bus-routes/ （约束取自该页）。
- 代码：`../../coding/solutions/815_bus_routes.py`。
