---
id: tlc-clone-graph-2-code
node: a.clone-graph
type: qa
step: 2
---
## Q
**LC 133 克隆图**｜写出 Python 实现

`Node` 有 `val: int` 和 `neighbors: list[Node]`。给定无向连通图中的一个节点（可能是 `None`，节点数 `0` 到 `100`，`val` 互不相同），返回整张图的深拷贝。

## A
**思路。** BFS。字典 `copies` 把原节点映射到拷贝，入队前先建拷贝并登记。每次出队一个原节点，把它每个邻居对应的拷贝追加到自己拷贝的 `neighbors` 里；遇到没见过的邻居就先建拷贝再入队。

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

运行：`[[2,4],[1,3],[2,4],[1,3]]` → `[[2,4],[1,3],[2,4],[1,3]]`，克隆图与原图没有共享任何节点对象；`[[]]` → `[[]]`；空图 → `None`；`5000` 个节点的链状图也能完成（BFS 无递归）。

**复杂度。** 时间 `O(V + E)`：每个节点入队一次，每条边在两端各看一次；空间 `O(V)`：字典和队列。

**写法要点。** 用节点对象本身当字典的键（默认按身份哈希，不依赖 `val` 唯一）；`deque.popleft()` 是 `O(1)`，`list.pop(0)` 是 `O(n)`；「先登记、后入队」保证每个节点只入队一次；边的连接放在循环里统一做，不分「新节点 / 旧节点」两种情况。
