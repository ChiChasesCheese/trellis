---
id: tlc-flatten-binary-tree-to-linked-list-0-whole
node: b.flatten-binary-tree-to-linked-list
type: qa
---
## Q
**LC 114 二叉树展开为链表**｜Medium · CodeTop 国内累计 26 次 · 最近 2026-06-14（CodeTop）

给二叉树的根节点 `root`，原地把它展开成一个单链表：仍用 `TreeNode`，`right` 指向链表的下一个节点，`left` 始终为 `null`，顺序与先序遍历相同。节点数在 `[0, 2000]`，`-100 <= Node.val <= 100`。例：`[1,2,5,3,4,null,6]` → `[1,null,2,null,3,null,4,null,5,null,6]`；`[]` → `[]`；`[0]` → `[0]`。进阶：用 `O(1)` 额外空间。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 递归：先把左、右子树各自展开成链并拿到各自的尾节点，然后把原右子树接到左链的尾后面，再把左链搬到 `right`、`left` 置空；返回整条链的尾节点（右链有尾用右链的，否则左链的，否则自己）。`O(n)` 时间，`O(h)` 递归栈。

**识别。** 「原地」+「先序顺序」：先序是「根、左子树、右子树」，展开后左子树必须排在右子树前面，所以对每个节点只需要两件事：子树各自已经是链，再把两条链按「左、右」接起来。这是典型的「子问题的结果自己已经满足要求，只要在根处拼接」的树递归（分治）。接口上让递归返回尾节点，拼接才是 `O(1)`，否则每次都要重新沿右链找末端。`n` 到 `2000`，递归深度可达 `2000`，会超过 Python 默认的 `1000` 层递归上限，见易错点。

**推导。** 暴力：先序遍历把节点收进列表，再逐个改指针，`O(n)` 时间 `O(n)` 空间 → 洞察：不需要列表，子树的先序序列本身就是它展开后的链；假设 `flatten(左)`、`flatten(右)` 已经做完，整棵树的先序 = `根` + 左链 + 右链，只要把右链挂到左链的尾后面，再把左链挂到根的 `right` 上 → 为了不重复沿右链找末端，让递归顺便返回链尾，每个节点只做 `O(1)` 的指针操作。进阶要求 `O(1)` 额外空间时，换成沿 `right` 走、用左子树的最右下节点做拼接的迭代写法，见追问。

```python
def flatten(root: TreeNode | None) -> None:
    def dfs(node: TreeNode | None) -> TreeNode | None:   # 把 node 子树展开成链，返回链的尾节点
        if node is None:
            return None
        left_tail = dfs(node.left)                       # 左子树展开后的尾
        right_tail = dfs(node.right)                     # 右子树展开后的尾
        if left_tail:                                    # 有左子树才需要拼接
            left_tail.right = node.right                 # 原右子树接在左链后面
            node.right = node.left                       # 左链搬到右边
            node.left = None
        return right_tail or left_tail or node           # 整条链的尾：优先右链，其次左链，最后是自己

    dfs(root)
```

运行：`[1,2,5,3,4,null,6]` → `[1,null,2,null,3,null,4,null,5,null,6]`，`[]` → `[]`，`[0]` → `[0]`；深度 2000 的左链在默认递归上限下抛 `RecursionError`，调高上限后展开，沿 `right` 数到 `2000` 个节点。

**复杂度。** 时间 `O(n)`：每个节点只被 `dfs` 访问一次，拼接是常数次指针操作；空间 `O(h)`：递归栈，`h` 是树高，链状树时 `O(n)`。

**易错点。**
- 顺序：必须**先**把原右子树接到左链的尾 `left_tail.right`，**再**覆盖 `node.right`。漏掉接右子树这一步，`[1,2,5,3,4,null,6]` 只剩 `[1,null,2,null,3]`，正确有 `6` 个节点。
- 返回的尾节点要对：始终返回 `node` 当尾，`[1,2,5,3,4,null,6]` 会得到 `[1,null,2,null,5,null,6]`（`3`、`4` 被覆盖掉），正确的尾是右链优先的 `right_tail or left_tail or node`。
- 左指针要置 `None`，否则展开后还留着指向旧子树的 `left`，形成环或重复访问。
- 递归深度：深度 2000 的链深度就是 `2000`，CPython 默认递归上限约 `1000`，会抛 `RecursionError`；要么 `sys.setrecursionlimit` 调高，要么改成迭代（见追问）。

**追问。**
- 进阶 `O(1)` 额外空间：沿 `right` 向下走，遇到有左子树的 `cur`，找到左子树的最右下节点 `pred`，先把原右子树接到 `pred.right`，再把左子树搬到 `cur.right`、`cur.left` 置空（先序顺序不变，这是 Morris 遍历的核心操作）；递归栈也没有了，不受递归上限影响：
```python
def flatten_o1(root: TreeNode | None) -> None:
    cur = root
    while cur:
        if cur.left:
            pred = cur.left                # 从左孩子出发，沿右链走到头
            while pred.right:
                pred = pred.right
            pred.right = cur.right         # 先把原右子树接在右链末端
            cur.right = cur.left           # 再把左子树整体搬到右边
            cur.left = None
        cur = cur.right
```
- 显式栈：先序遍历时记 `prev`，每弹出一个节点就让 `prev.right = node`、`prev.left = None`；右孩子先入栈、左孩子后入栈，`O(h)` 空间。
- 逆后序递归：按「右、左、根」访问，维护 `prev`，`node.right = prev; node.left = None; prev = node`，不需要返回尾节点。
- 展开成中序链表（LC 426 的变体）或展开多级双向链表（LC 430）：换遍历顺序或多一个 `prev` 指针。

**同模式。** LC 430 扁平化多级双向链表、LC 426 将二叉搜索树转化为排序的双向链表、LC 144 二叉树的先序遍历、LC 94 二叉树的中序遍历（Morris 遍历）。
