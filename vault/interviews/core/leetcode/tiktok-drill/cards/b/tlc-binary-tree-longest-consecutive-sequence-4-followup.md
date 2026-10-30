---
id: tlc-binary-tree-longest-consecutive-sequence-4-followup
node: b.binary-tree-longest-consecutive-sequence
type: qa
step: 4
---
## Q
**LC 298 二叉树最长连续序列**｜追问

面试官接着问：（1）树退化成 `30000` 层的链，递归超限，怎么改成迭代？（2）路径可以递增也可以递减，还可以在某个节点拐弯（先上后下），怎么做（LC 549）？（3）树是 N 叉树？（4）要返回这条路径本身？

## A
1. **显式栈**：栈里放 `(节点, 以它结尾的连续长度)`，根的长度是 `1`。每弹出一个节点就更新答案；对每个孩子，值恰好比当前节点大 `1` 则长度加一，否则重置为 `1`，再压栈。`O(n)` 时间，深度不受递归上限限制。
```python
def longest_consecutive_iter(root: TreeNode | None) -> int:
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
`30000` 个节点的右斜链（值 `1..30000`）→ `30000`，默认递归上限下也不抛 `RecursionError`。
2. **递增 / 递减 / 可拐弯**：后序遍历，每个节点返回「从它向下的最长递增链、最长递减链」，在节点处合并两条链。
```python
def longest_consecutive_ii(root: TreeNode | None) -> int:
    best = 0

    def dfs(node: TreeNode | None) -> tuple[int, int]:
        nonlocal best
        if node is None:
            return 0, 0
        inc = dec = 1                              # 从 node 向下的最长递增 / 递减链
        for child in (node.left, node.right):
            if child is None:
                continue
            c_inc, c_dec = dfs(child)
            if child.val == node.val + 1:
                inc = max(inc, c_inc + 1)
            elif child.val == node.val - 1:
                dec = max(dec, c_dec + 1)
        best = max(best, inc + dec - 1)            # 路径可以经过 node 拐一下
        return inc, dec

    dfs(root)
    return best
```
`[1,2,3]` → `3`，`[2,1,3]` → `3`（`1-2-3`，在 `2` 处拐弯），`[2,null,3,2,null,1]` → `3`。这里用了递归，深度大时同样要换成显式后序遍历。
3. **N 叉树**：把 `(node.left, node.right)` 换成 `node.children`，其余不变。
4. **返回路径**：递归参数（或栈元素）里多带「这条链的起点节点」，更新 `best` 时记下 `(起点, 当前节点)`，最后沿 `parent` 或重新从起点向下走一遍还原；或者栈里直接带一个路径列表（空间 `O(n · h)`，只在必要时用）。

**Python 提醒**：嵌套函数里要修改外层变量 `best` 必须写 `nonlocal best`，否则赋值会创建局部变量，外层的 `best` 始终是 `0`。
