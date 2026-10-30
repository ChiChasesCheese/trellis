---
id: tlc-clone-graph-2-code
node: b.clone-graph
type: qa
step: 2
---
## Q
**LC 133 克隆图**｜写出 Python 实现

`Node` 有 `val: int` 和 `neighbors: list[Node]`。给定无向连通图中的一个节点（可能是 `None`，节点数 `0` 到 `100`，`val` 互不相同），返回整张图的深拷贝。

## A
**思路。** 递归 DFS。字典 `copies` 把原节点映射到拷贝：`dfs(cur)` 若 `cur` 已在表里就直接返回它的拷贝；否则先建拷贝并登记，再把每个邻居递归克隆的结果作为拷贝的邻居列表。

```python
def clone_graph(node: Node | None) -> Node | None:
    copies: dict[Node, Node] = {}              # 原节点 -> 它的拷贝，同时充当 visited

    def dfs(cur: Node) -> Node:
        if cur in copies:
            return copies[cur]                 # 已经克隆过：直接复用，环到这里就断了
        copies[cur] = clone = Node(cur.val)    # 先登记再递归邻居，遇到环才不会死循环
        clone.neighbors = [dfs(nb) for nb in cur.neighbors]
        return clone

    return dfs(node) if node else None
```

运行：`[[2,4],[1,3],[2,4],[1,3]]` → `[[2,4],[1,3],[2,4],[1,3]]`，克隆图与原图没有共享任何节点对象；`[[]]` → `[[]]`；`[[2],[1]]` → `[[2],[1]]`；空图 → `None`。

**复杂度。** 时间 `O(V + E)`：每个节点只展开一次，每条边在两端各看一次；空间 `O(V)`：字典加递归栈。

**写法要点。** 用节点对象本身当字典的键（默认按身份哈希，不依赖 `val` 唯一）；`copies[cur] = clone = Node(cur.val)` 链式赋值一行完成「建拷贝并登记」，必须在递归邻居之前；邻居列表用列表推导式 `[dfs(nb) for nb in cur.neighbors]`，已克隆的邻居直接从字典命中，环就断在这里；`dfs(node) if node else None` 处理空图。深度：节点上千的链状图会超过 CPython 默认递归上限（约 `1000`），题目限定至多 `100` 个节点没有问题，BFS 写法见追问卡。
