# q10 · Wiki Minimum Clicks：有向图 BFS 最短路 + 路径重建，练的是"确定性遍历顺序"

> [!tldr]
> - **本题 Part 1 基础题面是 (reconstructed)**（只恢复出标题和 Graph/BFS 标签，没有逐字题面，按标题精确形式化）；**Part 2 是完全原创的 follow-up**（没有对应的 follow-up 报告）
> - 这题考的是：有向图上两点间最短路（点击数），以及重建具体路径
> - 三步套路：建有向邻接表（邻居按字母序排序）→ Part 1 标准 BFS 求距离 → Part 2 加父指针字典，回溯重建路径
> - 最值得带走的一个模式：**多个节点同时并列最短时，路径不是唯一的——必须约定一套确定性 tie-break**（FIFO 出队顺序 + 邻居字母序）才能让重建的路径可测试

## 1. 题目在说什么（人话版）
维基页面之间的超链接是有向边：A 链接到 B，不代表 B 也链接回 A。给一批边、一个起点、一个终点，求从
起点点击到终点最少需要几次点击（Part 1），以及具体点了哪些页面（Part 2）。不可达就返回 `-1`/`[]`。

三行小例子：
```
edges=[(A,B),(A,C),(B,D),(C,D),(D,E)], start=A, target=E
BFS: A的邻居排序后=[B,C]，先发现B后发现C(父都是A)；出队B发现D(父=B)；出队D发现E(父=D)
part1=3, part2=[A,B,D,E]
```

## 2. 读题：把文字变成模型
- **实体**：页面（图节点）、超链接（有向边）。
- **输入长什么样**：`PART n` + 边数 `E` + `E` 行 `from,to` + 一行 `start,target`。
- **输出要什么**：Part 1 一个整数（距离，`-1` 不可达）；Part 2 一行逗号连接的页面路径（空行不可达）。
- **状态**：邻接表 `adj: dict[str, list[str]]`（每个节点的邻居按字母序排序）、`visited` 集合；Part 2
  额外要一个 `parent` 字典记录"谁第一个发现了它"。
- **一句话建模**：这是标准的 **单源 BFS 最短路**，Part 2 是"BFS + 父指针回溯"的标准扩展，唯一需要
  额外交代清楚的是**确定性 tie-break**（多条最短路存在时，题目只认一条）。

> [!note] 为什么选这个数据结构
> BFS 天然保证第一次访问到某节点时的距离就是最短距离，`visited` 集合防止重复入队。路径重建需要知道
> "每个节点是被谁第一个发现的"，所以要在第一次标记 `visited` 的同时记录 `parent`。多条最短路存在时
> （比如样例里 B 和 C 都在距离 1 被发现），题目约定"FIFO 出队顺序 + 每个节点自己的邻居按字母序遍历"，
> 这样"谁先把某节点标记为已发现"就是唯一确定的。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 解析边表和 `start,target`，调 `part1`/`part2`，按格式打印。
2. **Part 1 最小可用**：`start==target` 直接返回 0；否则建邻接表（每个节点邻居排序），标准 BFS 记
   `(node, dist)`，第一次发现 `target` 就返回 `dist+1`；队列耗尽还没找到就返回 `-1`。
3. **Part 2 叠加**：同样的 BFS，改成只存 `parent[nxt]=node`（不存距离），发现 `target` 就提前清空
   队列跳出循环；最后从 `target` 沿 `parent` 回溯到 `start`，反转得到路径。
4. **收尾**：自环、不连通、死胡同页面（有入边没出边）、只作为边目标从未作为源出现的节点、重复边
   等边界过一遍。

## 4. 代码怎么组织
```
_build_adjacency(edges) -> dict[str, list[str]]   # 有向邻接表，每个节点邻居按字母序排序
part1(edges, start, target) -> int                # 标准 BFS 求最短距离
part2(edges, start, target) -> list[str]           # BFS + 父指针 + 回溯重建路径
main(stdin, stdout)                                 # 解析、按 PART 分派
```
邻接表构建独立成一个 helper，两个 part 共用，且"排序"这一步统一在这里做一次，保证两个 part 的遍历
顺序完全一致（这对 tie-break 的确定性很重要，即使 Part 1 的距离结果本身不受排序影响）。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
def _build_adjacency(edges):
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
    for node in adj:
        adj[node].sort()                    # 字母序，保证确定性
    return adj

def part1(edges, start, target):
    if start == target:
        return 0
    adj = _build_adjacency(edges)
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        node, dist = queue.popleft()
        for nxt in adj.get(node, []):
            if nxt not in visited:
                if nxt == target:
                    return dist + 1
                visited.add(nxt)
                queue.append((nxt, dist + 1))
    return -1

def part2(edges, start, target):
    if start == target:
        return [start]
    adj = _build_adjacency(edges)
    visited = {start}
    parent = {}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in adj.get(node, []):        # FIFO 出队 + 邻居字母序 = 确定性发现顺序
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = node
            if nxt == target:
                queue.clear()                 # 找到就提前结束，不用继续扩展
                break
            queue.append(nxt)
    if target not in visited:
        return []
    path = [target]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「这是有向图上的最短路，我先确认自环、死胡同、不连通这几种情况怎么处理；因为可能有多条
  等长最短路，我会约定一套确定性的遍历顺序（邻居按字母序、FIFO 出队）保证路径唯一。」
- 写 Part 1 时：「标准 BFS，第一次到达 target 时的距离就是答案，用 `visited` 防止重复访问。」
- 写 Part 2 时：「在 Part 1 的基础上加一个 `parent` 字典，第一次发现某节点时记下是谁发现的它，
  最后从 target 沿 parent 往回走到 start，再反转，就是最短路径。」
- 交付时：「三个官方样例都过了；自环、死胡同、只作为边目标出现的节点这些边界单独测了；1e5 规模的
  稀疏图做了性能测试，远低于 2 秒预算。」

## 7. 常见跑偏（方法层面，3 条）
- **多条最短路存在时没有约定确定性 tie-break**：路径重建题如果不固定"谁先发现谁"的规则，测试会因为
  实现细节（比如用 set 而不是排序 list 存邻居）得到不同但同样合法的路径，对不上样例。
- **自环没有被 `visited` 正确挡住**：`A->A` 这种边如果不检查 `visited`，会导致同一个节点被重复处理
  甚至死循环。
- **忘记处理"只作为边目标出现、从未作为源出现"的节点**：查询它的邻居列表时 `adj.get(node, [])`
  不能写成 `adj[node]`（后者会在 `defaultdict` 里意外创建一个空列表项，虽然不算严重 bug，但容易在
  别的实现里变成 `KeyError`）。

## 8. 同族题 / 延伸
- 与 `q08_course_schedule_ii` 同属图论/BFS 家族，但那题是拓扑排序（DAG 特定结构），这题是通用有向图
  最短路（可以有环，只是环不影响 BFS 距离计算）。
- 延伸思考：如果链接是无向的（互相抵消方向性），只需要建图时把边加两次（正反各一次），BFS 逻辑不变。
- 如果部分链接权重更高（站内 vs 外链），需要把 BFS 换成 Dijkstra。
- 练习命令：`python3 loop/mock.py start q10`
