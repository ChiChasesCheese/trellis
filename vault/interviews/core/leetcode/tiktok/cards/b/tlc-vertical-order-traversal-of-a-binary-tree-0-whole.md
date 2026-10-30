---
id: tlc-vertical-order-traversal-of-a-binary-tree-0-whole
node: b.vertical-order-traversal-of-a-binary-tree
type: qa
---
## Q
**LC 987 二叉树的垂序遍历**｜Hard · CodeTop 国内累计 3 次 · 最近 2024-09-25（CodeTop）

给二叉树的根结点 `root`，计算它的**垂序遍历**。位置 `(row, col)`：根在 `(0, 0)`，一个节点在 `(row, col)`，则左孩子在 `(row + 1, col - 1)`，右孩子在 `(row + 1, col + 1)`。垂序遍历从最左边的列到最右边的列，每一列上的节点按位置**从上到下**（`row` 从小到大）排列；如果同一行同一列有多个节点，按**节点值从小到大**排。返回垂序遍历的结果（每一列一个列表）。节点数在 `[1, 1000]`，`0 <= Node.val <= 1000`。例：`[3,9,20,null,null,15,7]` → `[[9],[3,15],[20],[7]]`；`[1,2,3,4,5,6,7]` → `[[4],[2],[1,5,6],[3],[7]]`（`5` 和 `6` 都在 `(2, 0)`，按值 `5` 在前）；`[1,2,3,4,6,5,7]` 的结果与上一个相同。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 递归遍历一遍收集每个节点的 `(col, row, val)`，按元组整体排序——字典序正好是「列 → 行 → 值」三级顺序，再用 `itertools.groupby` 按列切段。`O(n log n)`。

**识别。** 「按多级条件排序后分组输出」：每个节点都有坐标，输出顺序由坐标和值共同决定。它不是普通的层序遍历：同一行同一列的节点要按**值**排，层序遍历里的出现顺序（从左到右）不满足这一点（示例 3）。

**推导。** 暴力：先遍历得到所有 `(row, col, val)`，再对每一列扫描一遍全部节点并排序，`O(n * 列数)` → 观察要求的顺序恰好是 `(col, row, val)` 的字典序，一次整体排序就全部满足 → 排序后同一列的节点连续，`groupby(key=col)` 切成一段一段。遍历用最直观的递归 `dfs(node, row, col)`，把坐标往下传；遍历顺序无所谓，因为随后会整体排序。

```python
from itertools import groupby
from operator import itemgetter


def vertical_traversal(root: TreeNode | None) -> list[list[int]]:
    nodes: list[tuple[int, int, int]] = []

    def dfs(node: TreeNode | None, row: int, col: int) -> None:
        if node is None:
            return
        nodes.append((col, row, node.val))           # 记下坐标和值；遍历顺序无所谓，排序会重排
        dfs(node.left, row + 1, col - 1)
        dfs(node.right, row + 1, col + 1)

    dfs(root, 0, 0)
    nodes.sort()                                     # 先按列、再按行、最后按值：正好是题目要的三级顺序
    return [[v for _, _, v in grp] for _, grp in groupby(nodes, key=itemgetter(0))]
```

运行：`[3,9,20,null,null,15,7]` → `[[9], [3, 15], [20], [7]]`；`[1,2,3,4,5,6,7]` → `[[4], [2], [1, 5, 6], [3], [7]]`；`[1,2,3,4,6,5,7]` → `[[4], [2], [1, 5, 6], [3], [7]]`；`1000` 个节点的左斜链 → `1000` 列，调高递归上限后正常返回；默认上限下抛 `RecursionError`。

**复杂度。** 时间 `O(n log n)`（排序主导）；空间 `O(n)`（列表，加上递归栈深度 `O(h)`）。

**易错点。**
- 只用层序遍历、不排序：`[1,2,3,4,6,5,7]` 得到 `[[4], [2], [1, 6, 5], [3], [7]]`，同行同列的 `6` 排在了 `5` 前面。
- 同一列按值全局排序、忽略行：`[5,1,3,null,null,2,null]` 得到 `[[1], [2, 5], [3]]`，正确是 `[[1], [5, 2], [3]]`（`5` 在第 `0` 行，`2` 在第 `2` 行，行靠上的在前）。
- 递归深度：`1000` 个节点的斜链连同最后一次对空节点的调用就是 `1001` 层，超过 CPython 默认递归上限约 `1000`，会抛 `RecursionError`；要么 `sys.setrecursionlimit` 调高，要么改成显式栈（见追问）。
- 元组顺序写成 `(row, col, val)`：排序后先按行分组，不再按列连续，`groupby` 切出来是错的。

**追问。**
- 树很深、递归会超限：用显式栈遍历，栈里放 `(节点, 行, 列)`；遍历顺序无所谓，其余部分（排序、`groupby`）不变。

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

- LC 314（二叉树的垂直遍历）：同列内按「从上到下、同行从左到右」，不按值排序。层序遍历加 `defaultdict(list)` 一趟 `O(n)`，不需要排序。
- 列的范围一定是连续的（相邻节点列差为 `1`），所以也可以记录最小列和最大列，用桶数组代替对列排序；每个桶内部仍要排序。
- 节点值可以重复：排序键已含值，不影响；`groupby` 只按列切段。

**同模式。** LC 314 二叉树的垂直遍历、LC 102 二叉树的层序遍历、LC 199 二叉树的右视图、LC 103 二叉树的锯齿形层序遍历、LC 429 N 叉树的层序遍历。
