---
id: tlc-recover-binary-search-tree-4-followup
node: p4.recover-binary-search-tree
type: qa
step: 4
---
## Q
**LC 99 恢复二叉搜索树**｜追问

面试官接着问：（1）只允许 `O(1)` 额外空间，怎么改？（2）不想碰递归上限，怎么用显式栈写？（3）如果不是恰好两个，而是任意个结点的值错位，还能一遍扫描吗？

## A
1. **`O(1)` 空间：Morris 遍历。** 栈（或递归）的作用只是「走完左子树后回到祖先」。Morris 把左子树最右结点（中序前驱）的空闲右指针临时指向当前结点作线索，走完再断开，因此不需要栈，且遍历后树结构还原。逆序检测逻辑与递归版完全一致。时间仍是 `O(n)`（每条边至多走两遍），空间 `O(1)`。

```python
def recover_tree_morris(root: TreeNode | None) -> None:
    first = second = prev = None
    cur = root
    while cur:
        if cur.left:
            pre = cur.left                         # 找中序前驱：左子树的最右结点
            while pre.right and pre.right is not cur:
                pre = pre.right
            if pre.right is None:                  # 第一次到达：建线索，进左子树
                pre.right = cur
                cur = cur.left
                continue
            pre.right = None                       # 第二次到达：左子树已走完，拆线索
        if prev and prev.val > cur.val:            # 访问 cur（中序位置）
            if first is None:
                first = prev
            second = cur
        prev = cur
        cur = cur.right
    if first and second:
        first.val, second.val = second.val, first.val
```

2. **显式栈（迭代中序）：** 单链树高 1000，递归超过默认的 1000 层上限会抛 `RecursionError`；可以 `sys.setrecursionlimit` 调大，或写迭代版：
```python
def recover_tree(root: TreeNode | None) -> None:
    stack: list[TreeNode] = []
    prev: TreeNode | None = None
    first = second = None
    node = root
    while stack or node:
        while node:                    # 一路向左压栈
            stack.append(node)
            node = node.left
        node = stack.pop()             # 弹出的顺序就是中序（升序）顺序
        if prev and prev.val > node.val:
            if first is None:
                first = prev
            second = node
        prev = node
        node = node.right
    if first and second:
        first.val, second.val = second.val, first.val
```
3. **任意个结点错位：** 不再是「1 或 2 处逆序」，位置不能只靠逆序对确定。通用办法：中序收集成数组，与排序后的数组逐位比较，不同位置即错位结点，`O(n log n)`。

**Python 提醒**：`a = b = None` 对不可变的 `None` 安全，但 `a = b = []` 会让两个名字指向同一个列表；Morris 遍历中途异常退出会留下线索，树结构被破坏；因此只在确定无异常的纯遍历里使用。
