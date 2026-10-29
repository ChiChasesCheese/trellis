---
id: uth-gaps-bfs-4-cascade
node: gaps.bfs
type: qa
step: 4
---
## Q
**删一个 Deployment，下面的怎么跟着删**｜Kubernetes · 1.34 垃圾回收

删除一个 Deployment 后，它的 ReplicaSet 和 Pod 是谁、怎样一层层找出来删掉的？

## A
**背景。** 每个对象的 `ownerReferences` 记着「我属于谁」：Pod 属于 ReplicaSet，ReplicaSet 属于 Deployment。删掉一个，要把它名下的、名下的名下，全找出来。

**结构。** 垃圾回收控制器（GC）在内存里维护一张图，每个节点记着自己的 `dependents`（以它为属主的节点）。收到「属主已删除」的事件，就把它的每个直接下属放进 `attemptToDelete` 工作队列；worker 取出一个，确认没有别的存活属主就删掉，这次删除又产生事件，下一层再入队。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<rect x="120" y="14" width="100" height="26" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">Deployment</text>
<rect x="120" y="74" width="100" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="91" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ReplicaSet</text>
<line x1="170" y1="40" x2="170" y2="68" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M170,74 L166.5,67 L173.5,67 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<rect x="62" y="134" width="56" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="90" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">Pod</text>
<rect x="142" y="134" width="56" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">Pod</text>
<rect x="222" y="134" width="56" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="250" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">Pod</text>
<line x1="170" y1="100" x2="90" y2="127" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M90,134 L86.5,127 L93.5,127 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="170" y1="100" x2="170" y2="127" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M170,134 L166.5,127 L173.5,127 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="170" y1="100" x2="250" y2="127" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M250,134 L246.5,127 L253.5,127 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">用户只删最上面一个 其余由 GC 逐层排队删</text>
</svg>
```

**细节。**

- 队列是 client-go 的先进先出工作队列，同一个对象排着时不会重复入队
- 多个 worker 并行取，所以只是「队列加展开下一层」的 BFS 思路，不保证严格逐层

**坑。** 前台删除（下属删完才删属主）只等 `blockOwnerDeletion=true` 的下属。

**例题：** LC 102 二叉树的层序遍历（同类：LC 199 二叉树的右视图）

给二叉树的根节点 `root`，逐层从左到右返回节点值，每层一个列表。例：`root = [3,9,20,null,null,15,7]` → `[[3],[9,20],[15,7]]`。

```python
from collections import deque


def level_order(root: TreeNode | None) -> list[list[int]]:
    if root is None:
        return []
    res: list[list[int]] = []
    queue = deque([root])
    while queue:
        level: list[int] = []
        for _ in range(len(queue)):     # 先固定本层的节点数，循环里新入队的是下一层
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        res.append(level)
    return res
```
