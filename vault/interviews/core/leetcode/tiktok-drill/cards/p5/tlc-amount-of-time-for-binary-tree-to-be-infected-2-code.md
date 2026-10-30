---
id: tlc-amount-of-time-for-binary-tree-to-be-infected-2-code
node: p5.amount-of-time-for-binary-tree-to-be-infected
type: qa
step: 2
---
## Q
**LC 2385 感染二叉树需要的总时间**｜写出 Python 实现

二叉树 `root`（节点数 `[1, 10^5]`，节点值互不相同，范围 `1` 到 `10^5`）和整数 `start`（树中必有该值）。第 `0` 分钟 `start` 节点被感染，之后每分钟感染与已感染节点相邻的未感染节点，返回感染整棵树的分钟数。

## A
**思路。** 递归遍历树，把每对父子的值双向写入邻接表。再从 `start` 出发做 BFS：每轮处理队列中当前所有节点（同一层），把未见过的邻居入队；每轮结束代表过了一分钟。

```python
from collections import defaultdict, deque


def amount_of_time(root: TreeNode, start: int) -> int:
    graph: defaultdict[int, list[int]] = defaultdict(list)   # 把树变成无向图：值互不相同，直接用值当点

    def link(node: TreeNode) -> None:                        # 递归遍历，把每条父子边双向写进邻接表
        for child in (node.left, node.right):
            if child:
                graph[node.val].append(child.val)
                graph[child.val].append(node.val)
                link(child)

    link(root)
    queue = deque([start])
    seen = {start}
    minutes = -1                                   # 第 0 层（起点）不花时间
    while queue:
        minutes += 1
        for _ in range(len(queue)):                # 一次处理完一整层 = 过一分钟
            u = queue.popleft()
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
    return minutes
```

运行：`[1,5,3,null,4,10,6,9,2]`，`3` → `4`；`[1]`，`1` → `0`；`[1,2]`，`2` → `1`；`[1,2]`，`1` → `1`；`10^5` 个节点的左斜链，`start = 50000` → `50000`（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`：建图和 BFS 各遍历每个节点常数次；空间 `O(n)`（含最深 `O(n)` 的递归栈）。

**写法要点。** `link` 是嵌套函数，直接往外层的 `graph` 里写，不用返回值；`for child in (node.left, node.right)` 把左右孩子写成一个循环；`defaultdict(list)` 省去判断键是否存在；`for _ in range(len(queue))` 先固定本层的节点数，再弹出，下一层的节点留在队列后面，层与层互不混淆；`minutes = -1` 让只有起点的情形自然得到 `0`；只有一个节点时 `graph[start]` 会被 `defaultdict` 自动建出空列表，不会 `KeyError`。
