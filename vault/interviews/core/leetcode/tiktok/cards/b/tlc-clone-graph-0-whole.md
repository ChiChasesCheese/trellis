---
id: tlc-clone-graph-0-whole
node: b.clone-graph
type: qa
---
## Q
**LC 133 克隆图**｜Medium · 字节高频

给无向**连通**图中一个节点的引用，返回该图的**深拷贝**（deep copy，所有节点都是新建的）。每个节点有整数 `val` 和邻居列表 `neighbors`（`Node` 类：`val: int`，`neighbors: list[Node]`）。给定节点永远是 `val = 1` 的那个。节点数在 `[0, 100]`，`1 <= Node.val <= 100` 且互不相同，无重复边、无自环。例：邻接表 `[[2,4],[1,3],[2,4],[1,3]]` 克隆后结构相同；`[[]]`（单节点无邻居）→ `[[]]`；空图 `[]` → 空。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 遍历图（BFS 或 DFS），用一个哈希表 `copies: 原节点 → 拷贝` 同时承担「已访问」和「找到对应拷贝」两个职责：第一次见到节点就建拷贝并登记，每条边都通过表把新节点连起来。`O(V + E)`。

**识别。** 「复制一个带环的结构」：环意味着不能无脑递归，必须记录哪些节点已经复制过；而新节点之间的连边又需要通过「原节点 → 拷贝」的映射得到，所以同一张表既是 visited 又是映射。同类信号：随机指针链表、对象图拷贝。

**推导。** 朴素递归「克隆自己 + 对每个邻居递归克隆」遇到环 `1-2-1-…` 无限递归 → 加 visited 集合避免死循环，但拿不到已建好的拷贝来连边 → 把 visited 升级成字典，值就是拷贝。BFS 版：入队时建拷贝并登记，出队时把所有邻居的拷贝挂到当前拷贝上；每个节点、每条边各处理一次。

```python
from collections import deque

def clone_graph(node: Node | None) -> Node | None:
    if node is None:
        return None
    copies = {node: Node(node.val)}            # 原节点 -> 它的拷贝，同时充当 visited
    queue = deque([node])
    while queue:
        cur = queue.popleft()
        for nb in cur.neighbors:
            if nb not in copies:               # 第一次见到：先建拷贝再入队
                copies[nb] = Node(nb.val)
                queue.append(nb)
            copies[cur].neighbors.append(copies[nb])
    return copies[node]
```

运行：`[[2,4],[1,3],[2,4],[1,3]]` → `[[2,4],[1,3],[2,4],[1,3]]`（所有节点都是新对象），`[[]]` → `[[]]`，空图 → `None`。

**复杂度。** 时间 `O(V + E)`；空间 `O(V)`（哈希表 + 队列）。

**易错点。**
- 没有「原节点 → 拷贝」映射、每次都新建：相邻节点互为邻居，递归永远走不完。`[[2],[1]]` 抛 `RecursionError`。
- 忘记判空：`[]` 的入参是 `None`，直接 `node.val` 会 `AttributeError`。
- 直接 `copies[cur].neighbors = cur.neighbors`：新图的邻居还指向旧节点，只是「浅拷贝」。

**追问。**
- 递归 DFS 写法：先把拷贝登记进字典，再递归邻居；链状图节点数大时有递归深度风险，BFS 没有。
- 图不连通、只给了节点列表：对每个未复制的节点各跑一次同样的流程，共用同一张 `copies`。
- 一行调用：`copy.deepcopy(node)` 自带 memo 能处理环，但面试要求手写。

**同模式。** LC 138 随机链表的复制、LC 207 课程表（环检测）、LC 797 所有可能的路径、LC 399 除法求值。
