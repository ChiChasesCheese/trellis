---
id: tlc-clone-graph-4-followup
node: b.clone-graph
type: qa
step: 4
---
## Q
**LC 133 克隆图**｜追问

面试官接着问：（1）改成递归 DFS 怎么写，要注意什么？（2）图不连通，给的是节点列表？（3）如果结构是带随机指针的链表（LC 138），思路一样吗？

## A
1. **递归 DFS**：关键仍是先登记再递归。
```python
def clone_graph_dfs(node: Node | None) -> Node | None:
    copies: dict[Node, Node] = {}

    def dfs(cur: Node) -> Node:
        if cur in copies:
            return copies[cur]
        copies[cur] = clone = Node(cur.val)       # 先登记再递归，遇到环才不会死循环
        clone.neighbors = [dfs(nb) for nb in cur.neighbors]
        return clone

    return dfs(node) if node else None
```
这个版本结果与 BFS 相同。节点上千且呈链状时递归深度会超过默认的 `1000`，`5000` 个节点的链会抛 `RecursionError`；BFS 不受影响。
2. **不连通**：对节点列表里每个还不在 `copies` 的节点各跑一次，共用同一张 `copies`，最后返回各自对应的拷贝列表。
3. **随机指针链表**：完全同构。`next` 和 `random` 都是「指向别的节点的引用」，`copies` 字典先给每个节点建拷贝，再第二遍按映射连 `next` / `random`；也可以像上面的 BFS 一样边遍历边建。

**Python 提醒**：`copy.deepcopy(node)` 内部带 memo，能正确处理带环的图，但面试要的是手写；`Node` 若自定义了 `__eq__` 却没写 `__hash__`，它就不能当字典的键。
