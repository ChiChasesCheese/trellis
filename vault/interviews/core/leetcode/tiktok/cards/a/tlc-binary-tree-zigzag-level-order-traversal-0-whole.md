---
id: tlc-binary-tree-zigzag-level-order-traversal-0-whole
node: a.binary-tree-zigzag-level-order-traversal
type: qa
---
## Q
**LC 103 二叉树的锯齿形层序遍历**｜Medium · TikTok·字节 高频

给二叉树的根节点 `root`，返回其节点值的**锯齿形层序遍历**：第一层从左往右，第二层从右往左，之后交替。树中节点数在 `[0, 2000]` 内，`-100 <= Node.val <= 100`。例：`root = [3,9,20,null,null,15,7]` → `[[3],[20,9],[15,7]]`；`root = [1]` → `[[1]]`；`root = []` → `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 照常做层序遍历（BFS），每层的节点始终按从左到右存放；只在把这一层的值写进答案的那一刻，按层号奇偶决定是否反转。`O(n)`。

**识别。** 「按层输出」就是广度优先（BFS，Breadth-First Search）：一层一层处理，每层先固定好节点。「之字形」只改变**输出顺序**，不改变**遍历顺序**，所以它是层序遍历加一个布尔开关，不是新算法。`n <= 2000`，`O(n)` 绰绰有余；用迭代而不用递归，因为单链树深度 2000 会超过 Python 默认递归上限 1000。

**推导。** 朴素想法：让队列两头进出，每层换一次方向 → 方向一换，左右孩子的入队次序也得跟着换，出队端、入队端、孩子顺序三件事要同时对，极易错。观察：遍历顺序和输出顺序可以分开 → 遍历一律从左到右，只对「写进答案的那份值列表」做反转 → 每个节点入队一次、反转一次，总共 `O(n)`。

```python
def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    if root is None:
        return []
    res: list[list[int]] = []
    level = [root]                      # 当前层的节点，始终按从左到右存放
    left_to_right = True
    while level:
        vals = [node.val for node in level]
        res.append(vals if left_to_right else vals[::-1])   # 只在输出时反转
        level = [child for node in level
                 for child in (node.left, node.right) if child]
        left_to_right = not left_to_right
    return res
```

运行：`[3,9,20,null,null,15,7]` → `[[3], [20, 9], [15, 7]]`，`[1]` → `[[1]]`，`[]` → `[]`，`[1,2,3,4,null,null,5]` → `[[1], [3, 2], [4, 5]]`，2000 个节点的单链树 → 2000 层。

**复杂度。** 时间 `O(n)`；额外空间 `O(w)`，`w` 是最宽一层的节点数（答案本身不算）。

**易错点。**
- 把反转作用在遍历用的 `level` 上：先反转 `level` 再展开孩子，下一层的左右顺序就乱了。节点值 `1..15` 的满二叉树会得到 `[[1],[3,2],[6,7,4,5],[11,10,9,8,15,14,13,12]]`，正确是 `[[1],[3,2],[4,5,6,7],[15,14,13,12,11,10,9,8]]`。
- 开关初值写反：第 0 层是正序。初值设成 `False`，示例一会变成 `[[3],[9,20],[7,15]]`。
- 空树返回 `[]`，不是 `[[]]`。

**追问。**
- 自底向上的层序（LC 107）：最后 `res.reverse()` 即可。
- 递归（DFS）写法：`dfs(node, depth)` 把值放进 `res[depth]`，最后反转奇数层；深链树会 `RecursionError`，要改成显式栈。
- 只要每层最右的节点：每层取 `level[-1]`（LC 199）。

**同模式。** LC 102 二叉树的层序遍历、LC 107 层序遍历 II、LC 199 二叉树的右视图、LC 637 二叉树的层平均值、LC 515 在每个树行中找最大值。
