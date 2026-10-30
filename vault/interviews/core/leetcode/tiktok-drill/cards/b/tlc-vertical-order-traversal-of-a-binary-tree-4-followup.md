---
id: tlc-vertical-order-traversal-of-a-binary-tree-4-followup
node: b.vertical-order-traversal-of-a-binary-tree
type: qa
step: 4
---
## Q
**LC 987 二叉树的垂序遍历**｜追问

面试官接着问：（1）树是 `1000` 层的斜链，递归超限，怎么改成迭代？（2）同一行同一列的节点不按值排序，而是按从左到右的出现顺序（LC 314）？（3）能不能避开对列号的排序？（4）改成 N 叉树？分别怎么改。

## A
1. **显式栈**：栈里放 `(节点, 行, 列)`，弹出时记录 `(col, row, val)`，再压左右孩子；遍历顺序无所谓，后面的排序和 `groupby` 不变，不受递归上限限制。
```python
from itertools import groupby
from operator import itemgetter


def vertical_traversal_stack(root: TreeNode | None) -> list[list[int]]:
    nodes: list[tuple[int, int, int]] = []
    stack = [(root, 0, 0)]                           # (节点, 行, 列)
    while stack:
        node, row, col = stack.pop()
        nodes.append((col, row, node.val))
        if node.left:
            stack.append((node.left, row + 1, col - 1))
        if node.right:
            stack.append((node.right, row + 1, col + 1))
    nodes.sort()                                     # 先按列、再按行、最后按值：正好是题目要的三级顺序
    return [[v for _, _, v in grp] for _, grp in groupby(nodes, key=itemgetter(0))]
```
`1000` 个节点的左斜链在默认递归上限下也能返回 `1000` 列；示例 `[1,2,3,4,5,6,7]` → `[[4], [2], [1, 5, 6], [3], [7]]`。
2. **LC 314**：不需要排序。层序遍历（`deque`），每个节点把值追加到 `cols[col]`，同一列自然按「从上到下、同行从左到右」出现；最后按列号输出：

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
3. **避免对列号排序**：树上相邻节点的列号相差 `1`，所以出现的列号是连续的一段。遍历时记下最小列和最大列，用桶数组 `buckets[col - min_col]`，输出时顺序读取即可；每个桶内部仍然要按「行、值」排序。
4. **N 叉树**：位置规则要先约定（比如孩子列号依次为 `col - k, ..., col + k`），其余完全一样：收集 `(col, row, val)`，整体排序，`groupby`。

**Python 提醒**：`deque.popleft()` 是 `O(1)`，`list.pop(0)` 是 `O(n)`，层序遍历一定用 `deque`；`defaultdict` 的 `cols[c]` 对不存在的列会创建空列表，输出时只遍历 `sorted(cols)` 里已有的列就不会多出空列。
