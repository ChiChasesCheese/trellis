# 重新安排行程（Reconstruct Itinerary, LC 332）

> 来源：Hello Interview `reconstruct-itinerary`，约 2026-09-20 中级，https://www.hellointerview.com/community/questions/reconstruct-itinerary ；公司页 https://www.hellointerview.com/community/questions?company=Amazon ；LC 官方 https://leetcode.com/problems/reconstruct-itinerary/ （约束取自该页）。
> 代码：`../../coding/solutions/332_reconstruct_itinerary.py`。

## 面经原话
报告写的是：「You are given a list of airline tickets where tickets[i] = [fromi, toi] represent the departure and the arrival airports of one flight. Reconstruct the itinerary in order and return it.」

## 题面与约束
所有行程从 `"JFK"` 出发，每张机票恰好用一次；有多个合法行程时返回字典序最小的。保证至少存在一个合法行程。
约束：`1 <= tickets.length <= 300`，`tickets[i].length == 2`，`fromi.length == toi.length == 3`，由大写字母组成，`fromi != toi`。

## 开场先问的澄清问题
1. 「字典序最小」按整个序列比较，对吗？（对，逐个机场比较。）
2. 允许同一张票重复出现（重复边）吗？（允许。）
3. 保证有解吗？（保证。）

## 先补一点基础：欧拉路径（Eulerian path）
- **是什么**：一条经过图中**每条边恰好一次**的路径。该题的图是有向图，机场是点，机票是边。
- **为什么需要**：「每张票用一次」不是「每个机场去一次」。把它当成走遍点的哈密顿路径（Hamiltonian path）会陷入 NP 难；欧拉路径有线性算法。
- **存在条件**：有向图中，起点出度比入度多 1、终点入度比出度多 1，其他点出入度相等（或所有点相等，成为回路）。该题保证有解。
- **Hierholzer 算法的直觉**：沿着边一直走，走不动（死路）的那个点一定是整条路径的**最后一个点**，因为它已无出边；把它记下来，回退一步再继续走剩下的边。最后把记下来的点倒过来，就是路径。

## 最笨解
回溯（DFS）：从 JFK 出发，每次按字典序尝试一张未使用的票，走到死路就撤销。最坏指数级；300 张票时经常会走进「先走字典序小的死路」再回头，反复回溯（见 `_brute`，仅用于小数据对拍）。

## 逐步改进
1. **问题**：回溯因为「先选了字典序小但会把后面的票卡死的边」而浪费。
2. **想法**：不要判断这条边「会不会卡死」，而是**允许走进去**，卡死的那个点（出度为 0）反正只能是路径的结尾部分，把它放到答案的最后面。
3. **为什么对**：卡死的点必然在欧拉路径的某个后缀，其他没用完的边是一个回路，会在回退过程中被「接」到前面。
4. **字典序**：每个机场的出边按字典序**降序**排列，用 `pop()` 取最小。这样每次都优先走最小的目的地。
5. **迭代**：用显式栈替代递归，避免栈过深（该题最多 300 张票，但 Python 递归 1000 层的限制在加长数据时会触碰；迭代是更稳的写法）。

```python
def find_itinerary(tickets):
    graph = {}
    for a, b in sorted(tickets, reverse=True):            # reverse-sorted so pop() yields the smallest destination
        graph.setdefault(a, []).append(b)
    stack, route = ["JFK"], []
    while stack:
        while graph.get(stack[-1]):                       # walk until stuck (this is the dead end)
            stack.append(graph[stack[-1]].pop())
        route.append(stack.pop())                         # a stuck airport is the LAST of what remains
    return route[::-1]
```

示例：`[["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]` 得到 `JFK, MUC, LHR, SFO, SJC`。`[["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]` 得到 `JFK, ATL, JFK, SFO, ATL, SFO`：先走 ATL（字典序小），回到 JFK 再走 SFO。

## 复杂度
排序 O(E log E)，Hierholzer 每条边只处理一次 O(E)；E = tickets.length。空间 O(E)。

## senior 追问
1. **不保证有解**：先检查出入度条件和连通性；或运行后检查 `len(route) == E + 1`，不满足返回空。
2. **票很多（1e6）**：排序的 `O(E log E)` 是瓶颈，可以按机场分桶排序，每个机场的出边单独排；内存放不下则外部排序。
3. **起点不固定**：先找出度比入度大 1 的点作为起点（没有则任取一个）。
4. **要所有合法行程**：数量可能指数级，需要问清楚；一般只输出个数用 BEST 定理或输出 k 个。
5. **机票有时间窗口**：欧拉路径不再适用，转为带时间约束的路径规划，通常 DP/最短路。
6. **并发更新机票**：把 `graph` 做成不可变快照，每次请求在快照上算，更新时换指针。

## 自测题
1. 为什么出边要降序排序后 `pop()`？
<details><summary>答案</summary>`pop()` 取列表末尾，降序列表的末尾是最小元素，取最小是 O(1)。</details>
2. 为什么最后要 `route[::-1]`？
<details><summary>答案</summary>死路点先入 `route`，也就是路径的结尾先被记录，倒过来才是从起点开始。</details>
3. 把 `while graph.get(stack[-1])` 改成 `if` 会怎样？
<details><summary>答案</summary>每次循环只前进一步就弹栈，会把还有未用出边的点过早记入答案，路径错乱。</details>
