---
id: tlc-clone-graph-4-followup
node: b.clone-graph
type: qa
step: 4
---
## Q
**LC 133 克隆图**｜追问

面试官接着问：（1）链状图有几千个节点，递归会怎样，怎么改成不递归？（2）图不连通，给的是节点列表？（3）如果结构是带随机指针的链表（LC 138），思路一样吗？

## A
1. **深图与 BFS**：递归深度等于最长路径，节点上千的链状图会超过 CPython 默认递归上限（约 `1000`），`5000` 个节点的链会抛 `RecursionError`。改成 BFS：字典先登记再入队，出队时给拷贝接上每个邻居的拷贝；结果与递归版相同。
```python
from collections import deque


def clone_graph_bfs(node: Node | None) -> Node | None:
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
2. **不连通**：对节点列表里每个还不在 `copies` 的节点各跑一次，共用同一张 `copies`，最后返回各自对应的拷贝列表。
3. **随机指针链表**：完全同构。`next` 和 `random` 都是「指向别的节点的引用」，`copies` 字典先给每个节点建拷贝，再第二遍按映射连 `next` / `random`；也可以像上面的 BFS 一样边遍历边建。

**Python 提醒**：`copy.deepcopy(node)` 内部带 memo，能正确处理带环的图，但面试要的是手写；`Node` 若自定义了 `__eq__` 却没写 `__hash__`，它就不能当字典的键。
