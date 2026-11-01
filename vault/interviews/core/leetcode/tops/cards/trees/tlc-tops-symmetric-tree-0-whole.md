---
id: tlc-tops-symmetric-tree-0-whole
node: trees.symmetric-tree
type: qa
---
## Q
**LC 101 对称二叉树**｜Easy · 全公司热度第 206 名 · Hot 100、Top Interview 150

给你一个二叉树的根节点 `root`，检查它是否轴对称（左右镜像）。节点数在 `[1, 1000]`，`-100 <= Node.val <= 100`。例：`root = [1,2,2,3,4,4,3]` → `true`；`root = [1,2,2,null,3,null,3]` → `false`。进阶：你可以运用递归和迭代两种方法解决这个问题吗？

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 两个指针同步递归（DFS）：同一棵树里「外侧对外侧、内侧对内侧」的镜像比较。

**一句话。** 树对称 = 左子树与右子树互为镜像；两棵树 `a`、`b` 互为镜像，当且仅当根值相等，且 `a.left` 与 `b.right` 互为镜像、`a.right` 与 `b.left` 互为镜像。

**识别。** 「对称、镜像」可以化成「两棵树同步走，一个走左另一个走右」，和 LC 100 相同的树是同一个骨架，只是孩子配对交叉。`n <= 1000`，`O(n)`。

**推导。** 把每层的值读出来判回文看似可行，但缺失的节点会让层内位置错位，信息不够。直接递归比较两棵子树：只需要把 LC 100 里的 `(a.left, b.left)` 换成 `(a.left, b.right)`。

```python
def is_symmetric(root: TreeNode | None) -> bool:
    def mirror(a: TreeNode | None, b: TreeNode | None) -> bool:
        if a is None or b is None:
            return a is b                          # 同为空才对称
        return (a.val == b.val
                and mirror(a.left, b.right)        # 外侧对外侧
                and mirror(a.right, b.left))       # 内侧对内侧

    return root is None or mirror(root.left, root.right)
```

运行：`[1,2,2,3,4,4,3]` → `True`；`[1,2,2,null,3,null,3]` → `False`；`[1]` → `True`；`[1,2,3]` → `False`。

**复杂度。** 时间 `O(n)`；空间 `O(h)`，递归栈。

**拓展优化。**
- 迭代（进阶）：队列里每次成对放入要比较的两个节点。
```python
from collections import deque

def is_symmetric_iter(root: TreeNode | None) -> bool:
    if root is None:
        return True
    queue = deque([(root.left, root.right)])
    while queue:
        a, b = queue.popleft()
        if a is None or b is None:
            if a is not b:
                return False
            continue
        if a.val != b.val:
            return False
        queue.append((a.left, b.right))            # 与递归版同一个配对规则
        queue.append((a.right, b.left))
    return True
```

**易错点。**
- 把配对写成 `mirror(a.left, b.left)`：那是在判断「相同」而不是「镜像」，`[1,2,2,3,4,4,3]` 得到 `False`，正确是 `True`。
- 逐层把非空节点的值读出来判回文：`[1,2,2,null,3,null,3]` 第三层读到 `[3,3]` 是回文，会判 `True`，正确是 `False`（两个 `3` 分别在 `2` 的同一侧）。必须比较结构。
- 递归深度：链状树最多 `n` 层；这里 `n <= 1000`，一条 `1000` 层的链会触到 CPython 默认上限，需调高或用迭代版。

**同模式。** LC 100 相同的树、LC 226 翻转二叉树、LC 572 另一棵树的子树、LC 951 翻转等价二叉树。
