---
id: tlc-tops-binary-tree-right-side-view-0-whole
node: trees.binary-tree-right-side-view
type: qa
---
## Q
**LC 199 二叉树的右视图**｜Medium · 全公司热度第 190 名 · NeetCode 150、Hot 100、Top Interview 150、LeetCode 75

给定一个二叉树的根节点 `root`，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值。二叉树的节点个数的范围是 `[0, 100]`，`-100 <= Node.val <= 100`。

例：`root = [1,2,3,null,5,null,4]` → `[1,3,4]`；`root = [1,2,3,4,null,null,null,5]` → `[1,3,4,5]`；`root = [1,null,3]` → `[1,3]`；`root = []` → `[]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 按深度分层的树遍历：DFS 时「先右后左 + 每层只取第一个到达的结点」，等价于 BFS 每层最后一个。

**一句话。** 先右后左做 DFS，每个深度第一次到达的结点就是该层最右边能看到的结点。

**识别。** 「每层一个值」「从某一侧看」是按层取代表结点的信号；注意被看到的不一定在右子树里，右边没有结点时左子树的结点会露出来（例 2 的 `4` 和 `5`）。`n <= 100`，线性。

**推导。** 只沿右孩子一路走会漏掉左子树比右子树深的部分。正确说法是：每一层最靠右的那个结点可见。BFS 取每层最后一个即可；DFS 里也能做到：规定先访问右子树，那么对任何一个深度，第一次到达它的必然是该层最右的结点，之后同深度的都被挡住。用 `len(res)` 当「已经看到的最大深度」，一个条件就搞定。

```python
def right_side_view(root: TreeNode | None) -> list[int]:
    res: list[int] = []

    def dfs(node: TreeNode | None, depth: int) -> None:
        if not node:
            return
        if depth == len(res):       # 这个深度第一次出现：先走右，所以它就是该层最右的
            res.append(node.val)
        dfs(node.right, depth + 1)  # 先右后左
        dfs(node.left, depth + 1)

    dfs(root, 0)
    return res
```

**运行。** `[1,2,3,null,5,null,4]` → `[1, 3, 4]`；`[1,2,3,4,null,null,null,5]` → `[1, 3, 4, 5]`；`[1,null,3]` → `[1, 3]`；`[]` → `[]`。

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**拓展优化。**
- BFS 写法：逐层遍历，每层只取最后一个结点的值，空间 `O(w)`。树非常深而不宽时更稳（没有递归上限问题）。
```python
from collections import deque


def right_side_view_bfs(root: TreeNode | None) -> list[int]:
    res: list[int] = []
    q = deque([root] if root else [])
    while q:
        res.append(q[-1].val)               # 队列末尾就是本层最右的结点
        for _ in range(len(q)):
            node = q.popleft()
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
    return res
```
- 左视图只需交换访问顺序；每层最大值、每层平均值也是同一骨架。

**易错点。**
- 只沿右孩子走：例 2 `[1,2,3,4,null,null,null,5]` 得到 `[1, 3]`，丢掉了左子树里更深的 `4` 和 `5`。
- 先左后右却仍用「第一次到达」：得到的是左视图，例 1 输出 `[1, 2, 5]`。
- 递归深度等于树高：`n <= 100` 时安全；树更深时（链状上万结点）会超过 CPython 默认约 1000 的递归上限，需要改用 BFS。

**同模式。** LC 102 二叉树的层序遍历、LC 515 在每个树行中找最大值、LC 1161 最大层内元素和、LC 116 填充每个节点的下一个右侧节点指针。
