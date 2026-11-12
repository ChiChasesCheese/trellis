---
slug: maximum-width-of-binary-tree
---
## Q
**LC 662 二叉树最大宽度**｜Medium

一层的宽度是该层最左与最右非空节点之间的长度（中间的 `null` 也计入）。求所有层的最大宽度。

## A
**一句话。** 按堆的方式给节点编号（左 `2i`、右 `2i+1`）做层序遍历，宽度为最右减最左编号加一，每层归零防止膨胀。

```python
def width_of_binary_tree(root):
    best = 0
    level = [(root, 0)]          # (节点, 层内编号)
    while level:
        base = level[0][1]       # 本层最左编号，用来归零
        best = max(best, level[-1][1] - base + 1)
        nxt = []
        for node, idx in level:
            idx -= base
            if node.left:
                nxt.append((node.left, 2 * idx))
            if node.right:
                nxt.append((node.right, 2 * idx + 1))
        level = nxt
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只数每层节点个数：`[1,3,2,5,3,null,9]` 得 `3`，应为 `4`，中间空位没计入。
- 宽度漏掉 `+ 1`：少算 1。
- 不归零：编号长成大整数，运算变慢，在 Java / C++ 里还会溢出。

**追问。**
- 用 DFS 怎么做？：先序遍历，字典 `first[depth]` 记每层第一次见到的编号，宽度为 `idx - first[depth] + 1`。

**同模式。** LC 102 二叉树的层序遍历、LC 515 在每个树行中找最大值、LC 919 完全二叉树插入器、LC 958 二叉树的完全性检验
