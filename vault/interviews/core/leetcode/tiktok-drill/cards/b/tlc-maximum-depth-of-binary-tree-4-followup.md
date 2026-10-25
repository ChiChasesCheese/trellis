---
id: tlc-maximum-depth-of-binary-tree-4-followup
node: b.maximum-depth-of-binary-tree
type: qa
step: 4
---
## Q
**LC 104 二叉树的最大深度**｜追问

面试官接着问：（1）递归写法什么时候会出问题，怎么办？（2）改求**最小深度**（LC 111）要改哪里？（3）N 叉树的最大深度（LC 559）怎么写？

## A
1. **递归的风险**：递归深度等于树高。平衡树 `O(log n)` 没问题；`10^4` 个节点的单链需要 `10^4` 层调用，超过 CPython 默认上限 `1000`，抛 `RecursionError`。办法：像卡片里那样改成逐层迭代，或者用显式栈 `(node, depth)` 做深度优先。`sys.setrecursionlimit` 只改解释器的计数，真正的 C 栈用完仍会崩溃，不是正解。

```python
def max_depth_stack(root: TreeNode | None) -> int:
    best = 0
    stack = [(root, 1)]
    while stack:
        node, d = stack.pop()
        if node:
            best = max(best, d)
            stack.append((node.left, d + 1))
            stack.append((node.right, d + 1))
    return best
```

`[3,9,20,null,null,15,7]` → `3`。
2. **最小深度**：叶子的定义是「没有孩子」。BFS 里遇到的**第一个叶子**所在的层就是答案，可以提前返回；递归版要在只有一个孩子时取非空那一侧，不能直接 `1 + min(左, 右)`。
3. **N 叉树**：下一层是所有节点的 `children` 拼起来：`level = [c for node in level for c in node.children]`，其余不变。

**Python 提醒**：`max()` 对空序列抛 `ValueError`；N 叉树的递归写法 `1 + max((f(c) for c in node.children), default=0)` 必须带 `default=0`，叶子没有孩子。
