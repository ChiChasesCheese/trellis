---
id: tlc-populating-next-right-pointers-in-each-node-0-whole
node: a.populating-next-right-pointers-in-each-node
type: qa
---
## Q
**LC 116 填充每个节点的下一个右侧节点指针**｜Medium · 近一年被问：美国 1 次、国内 0 次 · CodeTop 国内累计 1 次 · 最近 2026-01-06（面试记录）

给一棵完美二叉树（所有叶子在同一层，每个非叶子节点都有两个孩子），节点有 `val`、`left`、`right`、`next` 四个字段。填充每个节点的 `next` 指针，让它指向同一层中右边紧邻的节点；某层最右边的节点，`next` 为 `None`。初始时所有 `next` 都是 `None`。树中节点数在 `[0, 2^12 - 1]` 范围内，`-1000 <= node.val <= 1000`。进阶：只用常量额外空间；递归实现也算符合，递归栈不计入额外空间。例：`[1,2,3,4,5,6,7]` → 按层用 `next` 串起来是 `1 -> None`、`2 -> 3 -> None`、`4 -> 5 -> 6 -> 7 -> None`；空树返回空。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 利用上一层已经连好的 `next` 链，在本层「横着走」给下一层连线：同一个父亲的两个孩子 `node.left.next = node.right`；跨父亲的 `node.right.next = node.next.left`。每一层从最左节点出发，一路向下。`O(n)` 时间，`O(1)` 额外空间。

**识别。** 「同层的下一个节点」本来要层序遍历（BFS）加队列；「常量额外空间」排除队列。完美二叉树保证每个节点要么是叶子、要么有两个孩子，且若 `node.next` 存在，它的左孩子也一定存在，所以连线时不需要判空。

**推导。** 暴力：BFS 层序遍历，同一层的节点前一个的 `next` 指向后一个，队列最宽时有 `n/2` 个节点，`O(n)` 空间 → 浪费：队列只是为了按层取节点，但处理第 `d` 层时，第 `d` 层自己的 `next` 链已经连好，它本身就是这一层的链表 → 洞察：处理第 `d` 层时，沿 `next` 链遍历，给第 `d + 1` 层连线；连完后，第 `d + 1` 层的 `next` 链就位，用同样的方法处理下一层。第 `d + 1` 层的起点就是第 `d` 层最左节点的左孩子。

```python
def connect(root: 'Node | None') -> 'Node | None':
    leftmost = root                          # 每一层的最左节点；上一层的 next 已连好，用它在本层“横着走”
    while leftmost and leftmost.left:
        node = leftmost
        while node:                          # 沿着本层的 next 链走，给下一层连线
            node.left.next = node.right      # 同一个父亲的两个孩子
            if node.next:
                node.right.next = node.next.left   # 跨父亲：右孩子连到右邻居的左孩子
            node = node.next
        leftmost = leftmost.left
    return root
```

运行：`[1,2,3,4,5,6,7]`（按层编号）连完后各层 `next` 串是 `1`；`2 -> 3`；`4 -> 5 -> 6 -> 7`，序列化为 `[1, '#', 2, 3, '#', 4, 5, 6, 7, '#']`；空树 → `None`；高度 `12` 的完美树（`4095` 个节点）每层都满足相邻节点互连、最右节点的 `next` 为 `None`。

**复杂度。** 时间 `O(n)`，每个节点被访问一次；空间 `O(1)`。

**易错点。**
- 只写 `node.left.next = node.right`，漏了跨父亲的连线：`[1,2,3,4,5,6,7]` 里 `5.next` 会是 `None`，正确是 `6`；`2.next = 3` 因为它们是第 `1` 层的兄弟，这一步由上一层的同父亲连线完成。
- 外层循环写成 `while leftmost:`：走到叶子层时，`leftmost.left` 是 `None`，访问 `node.left.next` 会抛 `AttributeError`。循环条件要用 `leftmost.left`。
- 空树：`root` 为 `None` 时 `leftmost and ...` 短路，直接返回 `None`，不需要额外判断。

**追问。**
- 树不是完美二叉树（LC 117）：孩子可能缺失，要一边遍历本层一边把下一层的孩子串成链，用一个哑节点做头。
- 递归写法：先连好当前节点的孩子，再递归，递归深度是树高，空间 `O(h)`。
- 层序遍历（BFS）的 `O(n)` 空间版本：作为对照可以先写，再引出常量空间。

**同模式。** LC 117 填充每个节点的下一个右侧节点指针 II、LC 102 二叉树的层序遍历、LC 199 二叉树的右视图、LC 429 N 叉树的层序遍历。
