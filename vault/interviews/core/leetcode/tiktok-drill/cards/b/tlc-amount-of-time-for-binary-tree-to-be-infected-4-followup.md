---
id: tlc-amount-of-time-for-binary-tree-to-be-infected-4-followup
node: b.amount-of-time-for-binary-tree-to-be-infected
type: qa
step: 4
---
## Q
**LC 2385 感染二叉树需要的总时间**｜追问

面试官接着问：（1）不建图，一遍遍历做完？（2）有多个起点同时被感染？（3）要知道每个节点是第几分钟被感染的？分别怎么改。

## A
1. **不建图**：用后序遍历，每个节点返回一个值。子树里没有 `start` 时，返回子树高度（正数）；`start` 在子树里时，返回 `-(start 到当前节点的距离 + 1)`（负数表示"在这一侧"）。在 `start` 节点本身，用它左右子树高度的最大值更新答案；对于 `start` 的每个祖先，用「到 `start` 的距离 + 另一侧子树的高度」更新答案。时间 `O(n)`，额外空间 `O(h)`。写起来比建图复杂，但省去了邻接表。
2. **多个起点**：把所有起点一起放进初始队列并加入 `seen`，其余完全不变（多源 BFS）。层数仍是最远节点到「最近起点」的距离。
3. **每个节点的感染时刻**：用字典 `dist` 代替 `seen`：

```python
from collections import defaultdict, deque


def infection_times(root: TreeNode, start: int) -> dict[int, int]:
    graph: defaultdict[int, list[int]] = defaultdict(list)
    stack = [root]
    while stack:
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                graph[node.val].append(child.val)
                graph[child.val].append(node.val)
                stack.append(child)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist
```

   `[1,5,3,null,4,10,6,9,2]`，`start = 3` 的结果里 `max(dist.values())` 是 `4`，与上面的答案一致。

**Python 提醒**：`dist` 既是距离表又兼任 `seen`，用 `v not in dist` 判断；`defaultdict` 在用 `graph[u]` 读取不存在的键时会插入新键，遍历期间不要对同一个字典边遍历边读未知键，上面只读取已建图的节点，没问题。
