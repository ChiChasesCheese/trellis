---
id: tlc-vertical-order-traversal-of-a-binary-tree-5-alt
node: b.vertical-order-traversal-of-a-binary-tree
type: qa
step: 5
---
## Q
**LC 987 二叉树的垂序遍历**｜另一种解法

不把所有 `(col, row, val)` 放在一起整体排序，还有什么写法能解 LC 987（节点数 `<= 1000`，同行同列按值升序）？它的复杂度是多少，什么时候该选它而不是整体排序？

## A
**层序遍历，逐层处理。** 行号就是层号，所以按层遍历时，行的顺序自然满足；每一层里用一个临时字典把同一列的值收集起来，**只在这一层内部**对每列的值排序，再追加到全局的 `cols[col]`：

```python
from collections import defaultdict


def vertical_traversal_bfs(root: TreeNode | None) -> list[list[int]]:
    cols: defaultdict[int, list[int]] = defaultdict(list)
    level = [(root, 0)]
    while level:
        buckets: defaultdict[int, list[int]] = defaultdict(list)
        nxt: list[tuple[TreeNode, int]] = []
        for node, col in level:
            buckets[col].append(node.val)
            if node.left:
                nxt.append((node.left, col - 1))
            if node.right:
                nxt.append((node.right, col + 1))
        for col, vals in buckets.items():
            cols[col].extend(sorted(vals))           # 同一行同一列：只在这一层内按值排序
        level = nxt
    return [cols[c] for c in sorted(cols)]
```

三个示例与整体排序的版本输出一致：`[[9], [3, 15], [20], [7]]`、`[[4], [2], [1, 5, 6], [3], [7]]`、同样的 `[[4], [2], [1, 5, 6], [3], [7]]`。

**复杂度。** 时间：遍历 `O(n)`；每层内的排序总和不超过 `O(n log w)`（`w` 是同一层内同一列的节点数，实际很小），再加列号排序 `O(c log c)`；空间 `O(n)`。

**怎么选。**
- 想要最短、最不容易错：整体排序加 `groupby`，三级顺序一次性由元组保证。
- 同行同列的冲突很少、希望排序的规模更小：逐层排序，每次只排冲突的少数几个值。
- 题目是 LC 314（不按值排序）：根本不需要排序，直接层序加字典。
- 注意：逐层版本只能用层序遍历（BFS）；如果用 DFS，同一列的节点出现顺序不是按行的，必须带上行号再排序。
