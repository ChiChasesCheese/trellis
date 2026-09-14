# 03 · 图 / 树模式识别 + ≤15 行模板

> 面向电面 coding（pc02 pc04 pc06 pc10）与 OA（q03 q07 q08 q10）。每种模式给**一眼信号 → ≤15 行模板 → 本 kit 哪题 → 最易错**。
> 代码引用自 `../../problems/q*/solution.py` 与 `../../loop/rounds/03_phone_coding/pc*/solution.py`。

---

## 1. 拓扑序传播（DAG 上的 DP）：RBAC 继承

**一眼信号**：「继承」「祖先的权限/属性会传给后代」「多个父节点」——本质是**在 DAG 的拓扑序上做 DP**，父节点的值必须在子节点读取前算完。

```python
def dp_union(n, order, parents, own):
    # order 是拓扑序（parents before children）；parents[u] 是 u 的直接祖先列表
    value = [set() for _ in range(n)]
    for u in order:
        value[u].update(own[u])
        for p in parents[u]:
            value[u].update(value[p])     # 父节点已经是"自己 + 更早祖先"的并集
    return value
```

**本 kit**：`pc01`（RBAC/DAG 权限继承题族，S01，#1 优先级题）。4 个 part 共用这一个核心：part1 单纯继承、part2 allow/deny 都继承且 deny 赢、part3 deny 只在本地生效（不传播）、part4 反向查询（见 `01-solving-framework.md` §5④）。

**最易错**：
- 拓扑序必须先用 Kahn 算法算出来，**不能假设输入按父在前排列**。
- 多父节点场景：`value[u]` 是所有直接父节点 `value` 的并集，**不是**只取某一个父节点——因为拓扑 DP 的正确性依赖"父节点的值已经是它自己那条链的完整并集"。
- part3 的"deny 不传播"和 part2 的"deny 传播且优先"是两套不同的转移，别在同一个函数里混用。

---

## 2. 多源 BFS：网格上的"最近设施"

**一眼信号**：「网格上有多个源点，求每个格子到最近源点的距离」「多个起点同时扩散」。

```python
from collections import deque
def multi_source_bfs(grid, sources):
    dist = {s: 0 for s in sources}
    dq = deque(sources)                       # 所有源点一起入队，天然按距离分层
    while dq:
        r, c = dq.popleft()
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r+dr, c+dc
            if in_bounds(nr, nc) and (nr,nc) not in dist:
                dist[(nr,nc)] = dist[(r,c)] + 1
                dq.append((nr,nc))
    return dist
```

**本 kit**：`pc02`（Closest Bathroom/Desk on a Grid，S05）。**注意 `pc02` 的参考实现按"整层"而不是单一 FIFO 队列处理**（`_bfs_with_source` 逐层展开 `frontier`），原因是它还要追加"这个格子是被哪个源点最先到达的"（tie-break：更小的源点坐标赢），单一队列下 tie 的胜者会依赖入队顺序，不满足确定性要求。**如果题目只要距离、不要"归属哪个源"，单队列版本（如上）就够用。**

**最易错**：
- 源点要在 BFS 开始前**全部**加入队列/distance 表，不是循环调用单源 BFS 再取 min（那样是 O(sources × cells)，多源 BFS 是 O(cells)）。
- 需要确定"归属"时，同一层内多个源点同时抵达同一格子要显式 tie-break，不能依赖队列的物理弹出顺序。

---

## 3. BFS 路径重建 + 字典序确定性

**一眼信号**：「求最短路径本身（不只是长度）」「多条最短路时按字典序取最小」。

```python
def bfs_path(adj, start, target):
    if start == target:
        return [start]
    visited, parent = {start}, {}
    dq = deque([start])
    while dq:
        node = dq.popleft()
        for nxt in sorted(adj.get(node, [])):     # 排序保证遍历顺序确定
            if nxt in visited:
                continue
            visited.add(nxt); parent[nxt] = node
            if nxt == target:
                dq.clear(); break
            dq.append(nxt)
    if target not in parent and target != start:
        return []
    path, node = [], target
    while node != start:
        path.append(node); node = parent[node]
    path.append(start)
    return path[::-1]
```

**本 kit**：`q10`（Wiki Minimum Clicks，part1 只要距离、part2 要重建路径）、`pc04`（Web Crawler Shortest Path Reconstruction，同族但仍在 phone_coding 池中开发，只按 id 引用）。`q10` part2 的关键纪律：**每个节点自己的邻居列表要先排序**（`_build_adjacency` 对每个节点的邻接表 `sort()`），这样"第一次发现"就等价于"字典序最小的路径"，不需要额外比较。

**最易错**：
- 路径重建要走 `parent` 字典，**不要**在 BFS 过程中现场拼接字符串/列表（会重复复制，O(n²)）。
- 字典序最小靠的是"邻居排序 + BFS 先到先得"，不是 BFS 完再对所有最短路排序比较（后者要枚举所有最短路，指数级）。
- `start == target` 要单独处理，返回 `[start]` 而不是走一遍 BFS。

---

## 4. Kahn 拓扑排序 + 按层输出

**一眼信号**：「先修课程」「依赖顺序」「最少批次/阶段完成所有任务（每批次可并行）」。

```python
from collections import deque
def kahn_layers(n, edges):        # edges[i] = (a, b): a 必须先于 b
    adj = [[] for _ in range(n)]; indeg = [0]*n
    for a, b in edges:
        adj[a].append(b); indeg[b] += 1
    q = deque(u for u in range(n) if indeg[u] == 0)
    layers, taken = 0, 0
    while q:
        layers += 1
        for _ in range(len(q)):              # 整层一起弹出 = 一个"批次"
            u = q.popleft(); taken += 1
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0: q.append(v)
    return layers if taken == n else -1       # taken < n 说明有环
```

**本 kit**：`q08`（Course Schedule II）两个 part 是同一算法的两种输出需求——part1（LC 210 原版）要**一条具体的拓扑序**、用最小堆代替普通队列保证"每次取当前可选里最小 id"的确定性；part2（LC 1136 型）要**最少批次数**，把队列按"整层"处理，层数就是答案。**同一个 Kahn 算法，换一种出队方式服务两种不同问题**是这道题唯一的设计点。

**最易错**：
- part1 用**堆**不是普通队列——"多个课程同时可选时取最小 id"这句话就是在提示优先队列。
- part2 判环用"`taken != n`"，不要用"队列提前空了就报错"——两者在这道题里等价，但堆版本的实现容易漏掉这一句独立检查。
- 起点是**所有**入度为 0 的节点集合，不是随便挑一个。

---

## 5. 树：深度计算 / 删叶子剪枝 / 换根

**一眼信号**：「树的高度/深度」「删除最少节点使高度 ≤ k」「换根操作使全树满足高度约束」——同一个"树高压缩"题族在 kit 里有三种不同的坐标约定，**不要把三个 part 的下标/深度定义混用**。

**深度计算（BFS from root）**：
```python
depth = {root: 0}                 # 或 1，看题目约定——q03 三个 part 各不相同
dq = deque([root])
while dq:
    v = dq.popleft()
    for c in children[v]:
        depth[c] = depth[v] + 1
        dq.append(c)
```

**删叶子/剪枝（q03 part1/part2）**：
- part1（节点级删除）：深度 > k 的节点必须删，且删除顺序总能安排成"先删更深的"，所以答案就是 `{v : depth[v] > k}` 直接排序输出（不需要额外 DP）。
- part2（整棵子树一起删，更省）：只统计**最靠上**的违规节点（`depth[v] > k and depth[parent[v]] <= k`），因为它的子树删除已经顺带清掉了更深的违规节点。

**换根（q03 part3）**：给定"最多 max_operations 次重定位"，二分答案高度 H，对每个候选 H 用记忆化 DFS `fix(v, d)` 判定"v 的整棵原始子树能否在 H 内达标"：
```python
def fix(v, d):                    # d = v 当前深度；返回让 v 子树满足高度 H 的最少操作数
    if d + height[v] <= H: return 0
    if d > H: return 1 + sum(fix(c, 1) for c in children[v])     # v 自己必须重定位到深度 1
    cut = 1 + sum(fix(c, 1) for c in children[v])                 # 方案 A：现在就重定位 v
    keep = sum(fix(c, d+1) for c in children[v])                  # 方案 B：留着 v，压子节点
    return min(cut, keep)
```

**本 kit**：`q03`（S04；三个 part 分别来自三个不同来源，坐标约定各异，见 `../../problems/q03_tree_height_reduction/solution.py` 头部注释）。

**最易错**：
- **三个 part 的根深度不同**（part1 根深度=1，part2 根深度=0），照抄一个 part 的代码去改另一个会系统性偏移 1。
- part3 的 `H == 0` 是特判：重定位后新深度**总是 1，不是 0**（只有根节点本身深度为 0），所以 `H == 0` 时任何非根节点都不可能通过重定位变得合法。
- 换根类问题优先想"二分答案 + 判定函数"，不要直接想复杂的树形 DP 一步到位。

---

## 6. Morris 遍历：O(1) 空间的中序遍历

**一眼信号**：「不用额外栈/递归」「bonus point if constant space」——这是 `01-solving-framework.md` §5① "压复杂度" follow-up 的树版本。

```python
def morris_inorder(root):
    out, node = [], root
    while node:
        if node.left is None:
            out.append(node.val); node = node.right
            continue
        pred = node.left
        while pred.right and pred.right is not node:
            pred = pred.right
        if pred.right is None:
            pred.right = node; node = node.left        # 第一次到达：穿线，往左走
        else:
            pred.right = None                            # 第二次到达（走线回来）：拆线，输出，往右走
            out.append(node.val); node = node.right
    return out
```

**本 kit**：`q07`（part1 递归 O(h) 栈 → part2 显式栈迭代 → part3 Morris O(1)，三者输出必须字节一致）。

**最易错**：
- 忘记**拆线**（`pred.right = None`）——不拆会让原树结构被永久破坏，且下一次遍历会死循环。
- 找"前驱"（predecessor）的循环条件是 `pred.right and pred.right is not node`，用 `is not` 而不是 `!=`（比较节点身份而不是值）。

---

## 7. 判环：Floyd 快慢指针（O(1) 空间）

**一眼信号**：「Happy Number」「链表判环」「函数迭代序列会不会进入循环」——本质都是"从某个起点反复应用一个确定性函数，判断轨迹是否回到之前访问过的状态"。

```python
def has_cycle_via_floyd(start, step):    # step(x) 返回 x 的下一个状态
    slow = fast = start
    while True:
        slow = step(slow)
        fast = step(step(fast))
        if fast == 1:            # Happy Number 场景：走到 1 说明不是循环
            return False
        if slow == fast:         # 快慢相遇 = 进入了循环（且不是终点）
            return True
```

**本 kit**：`pc06`（Happy Number，题面本身是 O(n) 空间 HashSet 判环，追问 "constant space" 才是 Floyd；仍在 phone_coding 池开发中，按 id 引用）。这是 `01-solving-framework.md` §5① 的另一个"压复杂度"例子：HashSet 存访问过的状态 O(1) 判重但 O(n) 空间 → Floyd 双指针同样能判环，空间降到 O(1)。

**最易错**：
- 快指针每步走两次 `step`，慢指针每步走一次——写反会退化成两者永远不相遇。
- 判"到达目标值就提前返回"要放在**每次移动之后**都检查，不能只在循环末尾检查一次（否则快指针可能跳过目标值）。
