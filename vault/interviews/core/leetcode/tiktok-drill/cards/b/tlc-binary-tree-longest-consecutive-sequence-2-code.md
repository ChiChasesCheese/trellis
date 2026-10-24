---
id: tlc-binary-tree-longest-consecutive-sequence-2-code
node: b.binary-tree-longest-consecutive-sequence
type: qa
step: 2
---
## Q
**LC 298 二叉树最长连续序列**｜写出 Python 实现

二叉树节点数 `1` 到 `3 * 10^4`，值在 `[-3 * 10^4, 3 * 10^4]`。求最长的、每步恰好加一且只能向下走的路径包含的节点数，路径起点任意。

## A
**思路。** 栈里放 `(节点, 以它结尾的连续长度)`，根的长度是 `1`。每弹出一个节点就更新答案；对每个孩子，若它的值恰好比当前节点大 `1`，长度加一，否则重置为 `1`，再压栈。

```python
def longest_consecutive(root: TreeNode | None) -> int:
    best = 0
    stack = [(root, 1)] if root else []          # (节点, 以它结尾的连续递增路径长度)
    while stack:
        node, length = stack.pop()
        best = max(best, length)
        for child in (node.left, node.right):
            if child:
                stack.append((child, length + 1 if child.val == node.val + 1 else 1))
    return best
```

运行：`[1,null,3,2,4,null,null,null,5]` → `3`，`[2,null,3,2,null,1]` → `2`，`[7]` → `1`；`30000` 个节点的右斜链（值 `1..30000`）→ `30000`。

**复杂度。** 时间 `O(n)`：每个节点压栈弹栈一次；空间 `O(h)`：栈里同时存在的节点数不超过树高加一层的宽度，链状树是 `O(n)`。

**写法要点。** 递归版更短，但 `30000` 层会触发 `RecursionError`，显式栈把深度搬到堆上；元组 `(节点, 长度)` 让每个节点自带上下文，不需要全局变量；`length + 1 if cond else 1` 是条件表达式，一次决定「延续或重置」；先弹后更新答案，叶子也会被统计到。
