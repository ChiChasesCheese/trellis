---
id: tlc-amount-of-time-for-binary-tree-to-be-infected-0-whole
node: a.amount-of-time-for-binary-tree-to-be-infected
type: qa
---
## Q
**LC 2385 感染二叉树需要的总时间**｜Medium · TikTok 高频

给二叉树的根节点 `root`，树中节点的值**互不相同**，再给整数 `start`。第 `0` 分钟，值为 `start` 的节点开始被感染。之后每分钟，满足下面两个条件的节点会被感染：此前没有被感染；与一个已被感染的节点**相邻**（父子相邻）。返回感染整棵树需要的分钟数。节点数在 `[1, 10^5]`，`1 <= Node.val <= 10^5`，值互不相同，树中一定存在值为 `start` 的节点。例：`root = [1,5,3,null,4,10,6,9,2]`，`start = 3` → `4`（第 `0` 分钟 `3`；第 `1` 分钟 `1, 10, 6`；第 `2` 分钟 `5`；第 `3` 分钟 `4`；第 `4` 分钟 `9, 2`）；`root = [1]`，`start = 1` → `0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先把二叉树变成无向图（每个节点既连孩子也连父亲），再从 `start` 做 BFS，一层代表一分钟；BFS 的层数减一（起点是第 `0` 层）就是答案，也就是 `start` 到最远节点的距离。`O(n)`。

**识别。** 「从某个点向四周扩散，每分钟蔓延一圈」是 BFS 按层推进的标准形态，答案是离起点最远的距离。二叉树节点没有父指针，感染要向上走，所以需要把树转成图（或者额外记录父节点）。节点值互不相同，可以直接把值当图里的点编号。

**推导。** 暴力：对每个节点求它到 `start` 的距离，需要找最近公共祖先，复杂 → 只要能「向上走」，问题就是普通图上的单源最短路：遍历一遍树，同时把父子边双向写进邻接表 → 从 `start` 做 BFS，一次处理一整层，层数就是分钟数；`n` 到 `10^5`，树可能是链，建图也用显式栈，避免递归。

```python
from collections import defaultdict, deque


def amount_of_time(root: TreeNode, start: int) -> int:
    graph: defaultdict[int, list[int]] = defaultdict(list)   # 把树变成无向图：值互不相同，直接用值当点
    stack = [root]
    while stack:
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                graph[node.val].append(child.val)
                graph[child.val].append(node.val)
                stack.append(child)
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

运行：`[1,5,3,null,4,10,6,9,2]`，`3` → `4`；`[1]`，`1` → `0`；`[1,2]`，`2` → `1`；`[1,2]`，`1` → `1`；`10^5` 个节点的左斜链、`start = 50000` → `50000`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`（邻接表、`seen`、队列）。

**易错点。**
- 只算 `start` 子树的高度（只向下感染）：示例 1 得到 `1`，正确是 `4`，因为感染也会向上传给父节点，再传到别的分支。
- 没有 `seen`：无向图里来回走，节点被重复入队，层数膨胀甚至死循环。
- 层数从 `0` 开始计、没有减一：单节点树返回 `1`，正确是 `0`。起点那一层不花时间。
- 用递归遍历建图：链状的 `10^5` 个节点会超过 Python 的默认递归深度。

**追问。**
- 不建图的一遍 DFS：后序遍历，每个节点返回子树高度；遇到 `start` 时记录它向下的高度，沿路向上的每个祖先，用「到 `start` 的距离 + 另一侧子树高度」更新答案，`O(n)` 时间、`O(h)` 额外空间。
- 多个起点同时感染：把所有起点一起放进初始队列，其余不变（多源 BFS）。
- 要每个节点被感染的时刻：BFS 时记录 `dist[v] = dist[u] + 1`。

**同模式。** LC 863 二叉树中所有距离为 K 的结点、LC 1740 找到二叉树中的距离、LC 994 腐烂的橘子、LC 542 01 矩阵、LC 1162 地图分析。
