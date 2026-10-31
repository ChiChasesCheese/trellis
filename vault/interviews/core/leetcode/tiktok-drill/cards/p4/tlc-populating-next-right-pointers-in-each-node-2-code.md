---
id: tlc-populating-next-right-pointers-in-each-node-2-code
node: p4.populating-next-right-pointers-in-each-node
type: qa
step: 2
---
## Q
**LC 116 填充每个节点的下一个右侧节点指针**｜写出 Python 实现

完美二叉树的节点有 `val`、`left`、`right`、`next`（节点数在 `[0, 2^12 - 1]`）。让每个节点的 `next` 指向同层右边紧邻的节点，最右边节点的 `next` 为 `None`。只用常量额外空间，返回根节点。

## A
**思路。** `leftmost` 指向当前层最左节点。外层循环逐层向下，条件是 `leftmost` 有孩子；内层沿本层的 `next` 链横走，对每个节点做两次连线：同一父亲的两个孩子相连；如果右边有邻居，右孩子连到邻居的左孩子。

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

运行：`[1,2,3,4,5,6,7]` 连完后按层序列化 → `[1, '#', 2, 3, '#', 4, 5, 6, 7, '#']`；空树 → `None`；高度 `1..12` 的完美树，每层相邻节点都互连，最右节点的 `next` 为 `None`。

**复杂度。** 时间 `O(n)`；空间 `O(1)`。

**写法要点。** 外层条件 `leftmost and leftmost.left` 同时处理空树和到达叶子层；内层 `node = node.next` 沿着刚连好的上一层链走，这是常量空间的关键；`node.next` 在内层循环走到下一个节点前仍未被修改（修改的是下一层的 `next`）；`leftmost = leftmost.left` 下降一层；函数返回 `root` 本身，不创建任何新节点；注解里的 `'Node | None'` 用字符串，因为 `Node` 由判题环境提供。
