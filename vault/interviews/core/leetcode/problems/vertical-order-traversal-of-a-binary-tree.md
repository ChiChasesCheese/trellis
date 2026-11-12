---
slug: vertical-order-traversal-of-a-binary-tree
---
## Q
**LC 987 二叉树的垂序遍历**｜Hard

根在 `(0,0)`，左孩子 `(row+1,col-1)`，右孩子 `(row+1,col+1)`。按列从左到右输出，列内按行从上到下，同行同列按值从小到大。

## A
**一句话。** 递归收集 `(col, row, val)`，整体排序后按列 `groupby` 切段。

```python
def vertical_traversal(root):
    nodes = []

    def dfs(node, row, col):
        if not node:
            return
        nodes.append((col, row, node.val))
        dfs(node.left, row + 1, col - 1)
        dfs(node.right, row + 1, col + 1)

    dfs(root, 0, 0)
    nodes.sort()                  # 列 → 行 → 值
    return [[v for _, _, v in g]
            for _, g in groupby(nodes, key=itemgetter(0))]
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 只层序遍历不排序：`[1,2,3,4,6,5,7]` 同行同列的 `6` 排在 `5` 前。
- 元组写成 `(row, col, val)`：先按行排，同列节点不再连续，`groupby` 切错。
- 同列只按值排、忽略行：`[5,1,3,null,null,2,null]` 应为 `[[1],[5,2],[3]]`。

**追问。**
- LC 314 垂直遍历呢？：同列按从上到下、从左到右，不比较值，层序加 `defaultdict(list)` 一趟 `O(n)`。
- 树很深递归超限？：改成显式栈存 `(节点, 行, 列)`，后面的排序不变。

**同模式。** LC 314 二叉树的垂直遍历、LC 102 二叉树的层序遍历、LC 199 二叉树的右视图、LC 103 二叉树的锯齿形层序遍历
