---
id: tlc-convert-binary-search-tree-to-sorted-doubly-linked-list-0-whole
node: b.convert-binary-search-tree-to-sorted-doubly-linked-list
type: qa
---
## Q
**LC 426 将二叉搜索树转化为排序的双向链表**｜Medium · LC TikTok 热度 50/100 · CodeTop 国内累计 11 次 · 最近 2024-01-16（CodeTop）

把一棵二叉搜索树（BST）**原地**转成一个已排序的**循环双向链表**：节点的 `left` 指针当作前驱，`right` 指针当作后继，第一个节点的前驱是最后一个节点，最后一个节点的后继是第一个节点。返回链表中最小元素的节点。树中节点数在 `[0, 2000]`，`-1000 <= Node.val <= 1000`，所有值互不相同。例：`root = [4,2,5,1,3]` → 从最小节点出发沿后继依次是 `1,2,3,4,5`，沿前驱依次是 `1,5,4,3,2`；`root = [2,1,3]` → `1,2,3`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** BST 的**中序遍历**（左 → 根 → 右）正好是升序。遍历时记住上一个访问的节点 `prev`：访问当前节点时，令 `prev.right = node`、`node.left = prev`；第一个访问的节点是链表头；遍历结束后把头尾互相连上。`O(n)` 时间，`O(h)` 空间。

**识别。** 「BST + 有序」= 中序遍历；「原地」= 不新建节点，复用 `left`、`right` 指针，所以遍历时**边走边改指针**；「循环」= 最后补一条首尾连线。递归中序最直观；节点数 `2000`、树可能退化成链，递归深度 `2000` 超过 Python 默认的约 `1000`，见易错点。

**推导。** 暴力：中序遍历把节点收进列表，再逐个连接并首尾相连，`O(n)` 额外空间，不算「原地」→ 观察：连接 `prev` 和 `node` 只需要知道上一个访问的节点，列表是多余的 → 遍历时只维护 `prev` 一个变量；第一个访问的节点（`prev` 还为空时）记为 `first`；遍历完 `prev` 就是最后一个节点，补上 `first.left = prev`、`prev.right = first`。改指针的顺序是安全的：访问 `node` 时它的左子树已经走完，`node.left` 可以改写；上一个节点 `prev` 的右子树在上一轮已经通过 `node = node.right` 读走，所以这一轮才能改写 `prev.right`。

```python
def tree_to_doubly_list(root: Node | None) -> Node | None:
    if root is None:
        return None
    first = prev = None

    def inorder(node: Node | None) -> None:    # 中序：左 -> 根 -> 右
        nonlocal first, prev
        if node is None:
            return
        inorder(node.left)
        if prev:
            prev.right, node.left = node, prev # 把上一个节点和当前节点互相连上
        else:
            first = node                       # 中序第一个节点就是最小值
        prev = node
        inorder(node.right)                    # 此时 node.right 还没被改过

    inorder(root)
    first.left, prev.right = prev, first       # 首尾相连成环
    return first
```

运行：`[4,2,5,1,3]` → 沿后继 `1,2,3,4,5` 回到头，沿前驱 `1,5,4,3,2` 回到头；`[2,1,3]` → `1,2,3` 与 `1,3,2`；单节点 → `left` 和 `right` 都指向自己；空树 → `None`；`2000` 个节点的右斜链（调大递归上限后）也能完成，最小节点的前驱值为 `1999`；默认上限下抛 `RecursionError`。

**复杂度。** 时间 `O(n)`；空间 `O(h)`（递归栈），链状树为 `O(n)`；没有新建节点，原地完成。

**易错点。**
- 忘记最后首尾相连：循环链表的最小节点的 `left` 仍为 `None`，沿前驱走不回来。
- 递归深度：`2000` 层的右斜链，递归深度超过 CPython 默认上限约 `1000`，抛 `RecursionError`；要 `sys.setrecursionlimit` 调大，或改成迭代（见追问）。
- 改写指针的时机不对：`prev.right` 必须等 `prev` 的右子树已被读走（`node = node.right`）之后再改，提前改会丢掉右子树。

**追问。**
- 不要循环、只要普通双向链表：去掉最后一行的首尾连线，头的 `left` 与尾的 `right` 保持 `None`。
- 不想动递归上限：迭代中序，用显式栈代替调用栈，连接逻辑相同：
```python
def tree_to_doubly_list_stack(root: Node | None) -> Node | None:
    if root is None:
        return None
    first = prev = None
    stack: list[Node] = []
    node = root
    while stack or node:                       # 迭代中序遍历：左 -> 根 -> 右
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev:
            prev.right, node.left = node, prev
        else:
            first = node
        prev = node
        node = node.right
    first.left, prev.right = prev, first
    return first
```
- 用 `O(1)` 空间：Morris 遍历用临时线索代替栈，`O(n)` 时间 `O(1)` 空间；但同时要改写 `right` 指针，实现很绕。
- 反过来，已排序的链表转平衡 BST（LC 109）：找中点作根，递归左右两半。

**同模式。** LC 94 二叉树的中序遍历、LC 230 二叉搜索树中第 K 小的元素、LC 114 二叉树展开为链表、LC 98 验证二叉搜索树。
