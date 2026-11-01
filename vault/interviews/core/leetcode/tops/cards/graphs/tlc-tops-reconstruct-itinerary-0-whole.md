---
id: tlc-tops-reconstruct-itinerary-0-whole
node: graphs.reconstruct-itinerary
type: qa
---
## Q
**LC 332 重新安排行程**｜Hard · 全公司热度第 150 名 · NeetCode 150

给你一份航线列表 `tickets`，其中 `tickets[i] = [from_i, to_i]` 表示飞机出发和降落的机场地点。请对该行程进行重新规划排序。所有这些机票都属于一个从 `JFK` 出发的先生，所以行程必须从 `JFK` 开始。如果存在多种有效的行程，返回字典序最小的行程组合（例如 `["JFK","LGA"]` 比 `["JFK","LGB"]` 更小）。假定所有机票至少存在一种合理的行程，且所有机票必须都用一次且只能用一次。`1 <= tickets.length <= 300`，`from_i`、`to_i` 都是由 3 个大写字母组成的机场代码，`from_i != to_i`。例：`tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]` → `["JFK","MUC","LHR","SFO","SJC"]`；`tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]` → `["JFK","ATL","JFK","SFO","ATL","SFO"]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 欧拉路径（Eulerian path）+ Hierholzer 算法：DFS 后序入栈，最后反转。

**一句话。** 每张机票是一条有向边，要一笔画走完所有边；从 `JFK` 出发做 DFS，每次走字典序最小的未用边，走到死胡同才把机场放进结果，最后把结果整个反转。

**识别。** 「每张票必须恰好用一次」就是一笔画（欧拉路径）；「字典序最小」要求按字典序顺序尝试边。`tickets <= 300`，所以路径长度至多 301，递归深度够用。

**推导。** 暴力回溯：每步按字典序尝试未用的机票，走不通就撤销，最坏指数级。普通贪心（每次走最小的出边）会走进死胡同：`JFK` 有 `KUL`（终点）和 `NRT`（还能回 `JFK`）两张票，先走 `KUL` 就再也回不来。欧拉路径的结构是：从起点走，遇到死胡同的那个点一定是整条路径的终点；把它放在最后，回溯到上一个有剩余边的点再绕一圈，把绕的圈接到前面。后序入栈 + 反转正好实现这件事，每条边只走一次。

```python
def find_itinerary(tickets: list[list[str]]) -> list[str]:
    graph: defaultdict[str, list[str]] = defaultdict(list)
    for src, dst in sorted(tickets, reverse=True):   # 逆序放入，pop() 从尾部取出的就是字典序最小的目的地
        graph[src].append(dst)
    route: list[str] = []

    def dfs(airport: str) -> None:
        while graph[airport]:                        # 还有没用的票：走字典序最小的
            dfs(graph[airport].pop())
        route.append(airport)                        # 后序：走不下去了才入栈，死胡同会最先入栈

    dfs("JFK")
    return route[::-1]                               # 入栈顺序是倒过来的行程
```

运行：示例一 → `['JFK', 'MUC', 'LHR', 'SFO', 'SJC']`，示例二 → `['JFK', 'ATL', 'JFK', 'SFO', 'ATL', 'SFO']`，`[["JFK","KUL"],["JFK","NRT"],["NRT","JFK"]]` → `['JFK', 'NRT', 'JFK', 'KUL']`，`[["JFK","A"]]` → `['JFK', 'A']`。

**复杂度。** 时间 `O(E log E)`（排序主导，DFS 本身 `O(E)`），空间 `O(E)`。

**拓展优化。**
- 递归深度最多 `E + 1 = 301`，在 CPython 默认约 1000 层的上限内；边数更多时改成显式栈，逻辑一样：

```python
def find_itinerary_stack(tickets: list[list[str]]) -> list[str]:
    graph: defaultdict[str, list[str]] = defaultdict(list)
    for src, dst in sorted(tickets, reverse=True):
        graph[src].append(dst)
    stack, route = ["JFK"], []
    while stack:
        while graph[stack[-1]]:                      # 栈顶还有出边就一直往前走
            stack.append(graph[stack[-1]].pop())
        route.append(stack.pop())                    # 栈顶走不下去了：后序入结果
    return route[::-1]
```

- 想要图里是否存在欧拉路径的判定：有向图要求除起点（出度比入度多 1）和终点（入度比出度多 1）外，每个点出度等于入度；这里保证有解，不必判定。

**易错点。**
- 普通贪心不回溯：`[["JFK","KUL"],["JFK","NRT"],["NRT","JFK"]]` 先走字典序更小的 `KUL`，得到 `['JFK', 'KUL']`（正确 `['JFK', 'NRT', 'JFK', 'KUL']`）。
- 忘了反转：`route` 是后序，直接返回得到的是倒序的行程。
- 忘了逆序排序再 `pop()`：用 `pop(0)` 是 `O(n)`；正序存入再 `pop()` 会先走字典序最大的。
- 最坏递归深度 `301`，低于 CPython 默认约 1000 的限制；票数再多就要改成上面的显式栈。

**同模式。** LC 2097 合法重新排列数对、LC 753 破解保险箱、LC 207 课程表、LC 399 除法求值。
