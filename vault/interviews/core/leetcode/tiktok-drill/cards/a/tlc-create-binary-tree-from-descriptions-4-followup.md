---
id: tlc-create-binary-tree-from-descriptions-4-followup
node: a.create-binary-tree-from-descriptions
type: qa
step: 4
---
## Q
**LC 2196 根据描述创建二叉树**｜追问

面试官接着问：（1）输入不保证有效，要怎样检测？（2）要把建好的树按层序输出成数组；（3）描述条数很大时，空间怎么控制？

## A
1. **校验输入**：根必须唯一，即 `len(parents - children) == 1`；同一个父节点的同一侧不能出现两次（记录 `(parent, is_left)` 是否已用）；一个孩子不能有两个父亲（`child` 重复出现）。最后从根遍历一遍，访问到的节点数必须等于 `len(nodes)`，否则存在环或与根不相连的部分。
2. **层序输出**：用 `deque` 做 BFS，缺失的孩子记 `None`，最后去掉末尾多余的 `None`。

```python
from collections import deque


def to_level_order(root: TreeNode | None) -> list[int | None]:
    out: list[int | None] = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        out.append(node.val if node else None)
        if node:
            queue.extend((node.left, node.right))
    while out and out[-1] is None:
        out.pop()
    return out
```

示例 1 → `[50, 20, 80, 15, 17, 19]`，示例 2 → `[1, 2, None, None, 3, 4]`。
3. **空间**：字典里一个值只存一个节点，内存与节点数成正比，和描述条数无关；两个集合可以省掉，改成单独记录每个值的「入度」数组，扫描后找入度为 `0` 的值。

**Python 提醒**：`queue.extend((node.left, node.right))` 一次放入两个孩子，包括 `None`，才能生成带占位的层序；用 `list.pop(0)` 当队列是 `O(n)` 一次，整体变成 `O(n^2)`，必须用 `deque`。
