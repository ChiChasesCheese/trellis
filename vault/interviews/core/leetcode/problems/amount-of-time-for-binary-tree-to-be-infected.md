---
slug: amount-of-time-for-binary-tree-to-be-infected
---
## Q
**LC 2385 感染二叉树需要的总时间**｜Medium

节点值互不相同的二叉树，第 `0` 分钟 `start` 节点被感染，之后每分钟感染相邻（父子）的节点。求感染整棵树需要几分钟。

## A
**一句话。** 先把树变成无向图，再从 `start` 做 BFS，层数就是分钟数。

```python
def amount_of_time(root, start):
    graph = defaultdict(list)    # 值互不相同，直接用值当点

    def link(node):
        for child in (node.left, node.right):
            if child:
                graph[node.val].append(child.val)
                graph[child.val].append(node.val)
                link(child)

    link(root)
    queue = deque([start])
    seen = {start}
    minutes = -1                 # 起点那层不花时间
    while queue:
        minutes += 1
        for _ in range(len(queue)):
            u = queue.popleft()
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
    return minutes
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只算 `start` 子树的高度：感染也会向上传，`[1,5,3,null,4,10,6,9,2]`、`start=3` 得 `1`，应为 `4`。
- 层数没减一：单节点树返回 `1`，应为 `0`。
- 没有 `seen`：无向图来回走，节点重复入队甚至死循环。

**追问。**
- 不建图能做吗？：后序 DFS，遇到 `start` 后沿路向上，用「到 `start` 的距离 + 另一侧高度」更新答案。
- 多个起点同时感染？：全部放进初始队列，即多源 BFS。

**同模式。** LC 863 二叉树中所有距离为 K 的结点、LC 1740 找到二叉树中的距离、LC 994 腐烂的橘子、LC 542 01 矩阵
