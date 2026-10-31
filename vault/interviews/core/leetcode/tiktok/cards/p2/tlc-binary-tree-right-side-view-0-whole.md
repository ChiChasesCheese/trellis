---
id: tlc-binary-tree-right-side-view-0-whole
node: p2.binary-tree-right-side-view
type: qa
---
## Q
**LC 199 二叉树的右视图**｜Medium · LC TikTok 近 6 个月热度 53/100（全时段 62） · 近一年被问：美国 2 次、国内 4 次 · CodeTop 国内累计 90 次 · 最近 2026-10（美国面试记录）

给二叉树的根节点 `root`，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值。节点个数范围 `[0, 100]`，`-100 <= Node.val <= 100`。例：`root = [1,2,3,null,5,null,4]` → `[1,3,4]`；`root = [1,2,3,4,null,null,null,5]` → `[1,3,4,5]`（第 4 层只有左子树的节点 `5`，右边没有遮挡，也能看到）；`root = [1,null,3]` → `[1,3]`；`root = []` → `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 层序遍历（BFS），每一层取**最后一个**节点的值。`O(n)`。

**识别。** 「从右侧看」= 每一深度上最靠右的那个节点，按深度从上到下输出：这是「按层处理」的信号。节点数至多 `100`，规模很小，重点是想清楚「看到」的定义。

**推导。** 暴力：只沿着右孩子一路往下走 → 浪费/错误：当右子树比左子树浅时，更深的层只有左子树的节点，它们同样会被看到 → 正确定义：每层最右边的节点 → 一层一层展开，每层取最后一个。

**简单解法。** 前序 DFS 带着深度，把每层所有节点值从左到右收进 `levels[depth]`，最后取每层最后一个。

```python
def right_side_view(root: TreeNode | None) -> list[int]:
    levels: list[list[int]] = []                    # levels[d]：深度 d 的节点值，从左到右

    def dfs(node: TreeNode | None, depth: int) -> None:
        if node is None:
            return
        if depth == len(levels):
            levels.append([])
        levels[depth].append(node.val)
        dfs(node.left, depth + 1)                   # 先左后右：每层最后收进去的就是最右的
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return [level[-1] for level in levels]
```

时间 `O(n)`，空间 `O(n)`；节点数 `<= 100` 没有问题，只是白存了每层除最右以外的值。

最优解：

```python
def right_side_view(root: TreeNode | None) -> list[int]:
    ans: list[int] = []
    level = [root] if root else []
    while level:
        ans.append(level[-1].val)                  # 这一层最右的节点
        level = [kid for node in level for kid in (node.left, node.right) if kid]
    return ans
```

运行：`[1,2,3,null,5,null,4]` → `[1, 3, 4]`，`[1,2,3,4,null,null,null,5]` → `[1, 3, 4, 5]`，`[1,null,3]` → `[1, 3]`，`[]` → `[]`。

**复杂度。** 时间 `O(n)`：每个节点进入 `level` 一次；空间 `O(w)`，`w` 是最宽一层的节点数，最坏 `O(n)`。

**拓展优化。**
- 先右后左的 DFS，每个深度只记第一次到达的节点，额外空间 `O(h)`（`h` 为树高），比 BFS 的 `O(w)` 队列省：
```python
def right_side_view_dfs(root: TreeNode | None) -> list[int]:
    ans: list[int] = []

    def dfs(node: TreeNode | None, depth: int) -> None:
        if node is None:
            return
        if depth == len(ans):                       # 该深度第一次到达，先右后左所以一定是最右的
            ans.append(node.val)
        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)

    dfs(root, 0)
    return ans
```

**易错点。**
- 只走右孩子链是错的：`[1,2,3,4,null,null,null,5]` 会得到 `[1, 3]`，正确是 `[1, 3, 4, 5]`。
- 空树要返回 `[]`：`level = [root] if root else []` 一行处理，否则 `root.val` 会对 `None` 报 `AttributeError`。
- 不要把「最右」理解成右孩子：某层的最右节点可能是某个左孩子。

**追问。**
- 左视图：把 `level[-1]` 换成 `level[0]`（拓展优化里的 DFS 则改成先左后右）。
- 底视图/顶视图需要水平位置：给每个节点标 `(深度, 水平偏移)`，是另一类问题（LC 314）。

**同模式。** LC 102 二叉树的层序遍历、LC 515 在每个树行中找最大值、LC 637 二叉树的层平均值、LC 116 填充每个节点的下一个右侧节点指针。
