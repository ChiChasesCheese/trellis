---
id: tlc-core-symmetric-tree
node: p4.symmetric-tree
type: qa
---
## Q
**LC 101 对称二叉树**｜Easy · LC TikTok 全时段热度 25/100 · 近一年被问：美国 1 次、国内 0 次 · CodeTop 国内累计 63 次 · 最近 2026-08-15（美国面试记录） · 也在：LeetCode Hot 100、Top Interview 150

给二叉树的根节点 `root`，检查它是否轴对称（左右两半互为镜像）。树中节点数在 `[1, 1000]` 内，`-100 <= Node.val <= 100`。例：`root = [1,2,2,3,4,4,3]` → `true`；`root = [1,2,2,null,3,null,3]` → `false`。进阶：递归和迭代两种方法都会写。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 树对称，等价于「左子树和右子树互为镜像」；用栈存放「应当互为镜像的一对子树」，每次弹出一对 `(a, b)`：两个都空就跳过，一空一不空或值不同就失败，否则把**外侧**一对 `(a.left, b.right)` 和**内侧**一对 `(a.right, b.left)` 压栈。`O(n)`。

**识别。** 「轴对称」「镜像」= 同时遍历两棵子树，而且指针是**交叉**配对的。它是「相同的树」（LC 100）的变体：那里配 `(a.left, b.left)`，这里配 `(a.left, b.right)`。`n <= 1000`，对称树深度至多约 500，递归也放得下，但迭代不受递归上限影响，面试里两种都要会。

**推导。** 暴力：真的造一棵镜像树，再逐点比较两棵树 → `O(n)` 时间，但多花 `O(n)` 空间造副本。浪费：镜像不必造出来，比较时让指针交叉走就等价。只比较中序序列是回文也不行：`[1,1,null,1]`（根 1，左孩子 1，左孩子的左孩子 1）的中序是 `1,1,1`，是回文，但并不对称，因为结构不同。洞察：`a` 与 `b` 互为镜像 ⇔ `a.val == b.val` 且 `a.left` 与 `b.right` 互为镜像、`a.right` 与 `b.left` 互为镜像。把这个递归关系展开成栈，就是下面的迭代。

```python
def is_symmetric(root: TreeNode | None) -> bool:
    if root is None:
        return True
    stack = [(root.left, root.right)]   # 每一对是应当互为镜像的两棵子树
    while stack:
        a, b = stack.pop()
        if a is None and b is None:
            continue
        if a is None or b is None or a.val != b.val:
            return False
        stack.append((a.left, b.right))     # 外侧配外侧
        stack.append((a.right, b.left))     # 内侧配内侧
    return True
```

运行：`[1,2,2,3,4,4,3]` → `True`，`[1,2,2,null,3,null,3]` → `False`，`[1]` → `True`，`[1,1,null,1]` → `False`。

**复杂度。** 时间 `O(n)`：每个节点至多在一对里出现一次；空间 `O(h)`，`h` 为树高（栈里同时存在的待比较对）。

**易错点。**
- 同侧配对 `(a.left, b.left)`：`[1,2,2,3,4,4,3]` 被判成 `False`（正确 `True`），`[1,2,2,null,3,null,3]` 被判成 `True`（正确 `False`）。
- 把 `None` 孩子过滤掉不压栈：「一边有孩子、另一边没有」就检查不到。`None` 对必须压栈，由弹出时统一处理。
- 判断顺序：先判两个都空（对称），再判一空一不空（不对称），最后才能访问 `.val`。

**追问。**
- 递归写法：`mirror(a, b)` 中 `if not a or not b: return a is b`，然后 `return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)`。
- 用队列（BFS）每次成对取出两个节点，逻辑完全相同，只是出入顺序不同。
- 判断一棵树是否是另一棵的子树（LC 572）、翻转二叉树（LC 226）。

**同模式。** LC 100 相同的树、LC 226 翻转二叉树、LC 572 另一棵树的子树、LC 951 翻转等价二叉树。
