---
slug: count-complete-tree-nodes
---
## Q
**LC 222 完全二叉树的节点个数**｜Medium

求一棵完全二叉树的节点数，要求比 `O(n)` 遍历更快。

## A
**一句话。** 数最左链和最右链的层数，相等就是满二叉树，返回 `2^h - 1`，否则递归左右子树。

```python
def count_nodes(root):
    lh, node = 0, root
    while node:             # 最左链层数
        lh += 1
        node = node.left
    rh, node = 0, root
    while node:             # 最右链层数
        rh += 1
        node = node.right
    if lh == rh:            # 满二叉树
        return (1 << lh) - 1
    return (1 + count_nodes(root.left)
            + count_nodes(root.right))
```

**复杂度。** 时间 `O(log² n)`，空间 `O(log n)`。

**易错点。**
- 公式漏掉 `- 1`：只有根时 `lh = rh = 1`，`1 << 1` 得 `2`，应为 `1`。
- 满子树不直接返回：会退化成 `O(n)`。

**追问。**
- 为什么是 `log² n`？：每层递归里有一棵子树是满的会立刻返回，只剩一条路径，深 `log n` 层，每层数链 `O(log n)`。
- 该方法用在非完全二叉树上呢？：`[1,2,3,null,4,5]` 两条链等长却不满，得 `3`，实际 `5`，所以依赖「完全」。

**同模式。** LC 104 二叉树的最大深度、LC 110 平衡二叉树、LC 958 二叉树的完全性检验、LC 100 相同的树
