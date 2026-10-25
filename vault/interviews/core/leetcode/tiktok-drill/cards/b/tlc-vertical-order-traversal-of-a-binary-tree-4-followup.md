---
id: tlc-vertical-order-traversal-of-a-binary-tree-4-followup
node: b.vertical-order-traversal-of-a-binary-tree
type: qa
step: 4
---
## Q
**LC 987 二叉树的垂序遍历**｜追问

面试官接着问：（1）同一行同一列的节点不按值排序，而是按从左到右的出现顺序（LC 314）？（2）能不能避开对列号的排序？（3）改成 N 叉树？分别怎么改。

## A
1. **LC 314**：不需要排序。层序遍历（`deque`），每个节点把值追加到 `cols[col]`，同一列自然按「从上到下、同行从左到右」出现；最后按列号输出：

```python
from collections import defaultdict, deque


def vertical_order(root: TreeNode | None) -> list[list[int]]:
    if root is None:
        return []
    cols: defaultdict[int, list[int]] = defaultdict(list)
    queue = deque([(root, 0)])
    while queue:
        node, col = queue.popleft()
        cols[col].append(node.val)
        if node.left:
            queue.append((node.left, col - 1))
        if node.right:
            queue.append((node.right, col + 1))
    return [cols[c] for c in sorted(cols)]
```

   `[3,9,20,null,null,15,7]` → `[[9], [3, 15], [20], [7]]`，整体 `O(n)` 加列号排序。
2. **避免对列号排序**：树上相邻节点的列号相差 `1`，所以出现的列号是连续的一段。遍历时记下最小列和最大列，用桶数组 `buckets[col - min_col]`，输出时顺序读取即可；每个桶内部仍然要按「行、值」排序。
3. **N 叉树**：位置规则要先约定（比如孩子列号依次为 `col - k, ..., col + k`），其余完全一样：收集 `(col, row, val)`，整体排序，`groupby`。

**Python 提醒**：`deque.popleft()` 是 `O(1)`，`list.pop(0)` 是 `O(n)`，层序遍历一定用 `deque`；`defaultdict` 的 `cols[c]` 对不存在的列会创建空列表，输出时只遍历 `sorted(cols)` 里已有的列就不会多出空列。
