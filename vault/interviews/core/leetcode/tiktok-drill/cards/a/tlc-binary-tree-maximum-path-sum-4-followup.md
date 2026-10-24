---
id: tlc-binary-tree-maximum-path-sum-4-followup
node: a.binary-tree-maximum-path-sum
type: qa
step: 4
---
## Q
**LC 124 二叉树中的最大路径和**｜追问

面试官接着问：（1）要返回路径本身，而不只是和？（2）路径必须从根出发（或必须在叶子结束）？（3）改成 N 叉树？

## A
1. **返回路径**：在每个节点多存一份「最优一侧是哪个孩子」（`nxt[node]`）。刷新全局最大值时，同时记下最高点 `top`。最后从 `top` 出发，沿左侧链和右侧链各走到头（只走增益为正的一侧），拼起来。额外空间 `O(n)`，时间仍是 `O(n)`。
2. **路径必须从根出发**：就不存在「拐弯」，答案是 `gain(root)`，即 `root.val + max(gain(左), gain(右), 0)`。去掉「左右合并」那一步，只剩一个自底向上的 `gain`；若还要求必须在叶子结束，就去掉 `0` 的下限，并且只在存在孩子时才选孩子。
3. **N 叉树**：最高点处从所有孩子的增益里取**最大的两个**（与 `0` 比较后），`val + 第一大 + 第二大` 刷新答案；向上返回 `val + 第一大`。用 `heapq.nlargest(2, gains)` 取两个，`gains` 为孩子增益的列表。

```python
import heapq

def top_two_gain(val: int, gains: list[int]) -> tuple[int, int]:
    """N 叉树的一个节点：返回 (以它为最高点的路径和, 向上返回的增益)。"""
    best_two = heapq.nlargest(2, [g for g in gains if g > 0])
    return val + sum(best_two), val + (best_two[0] if best_two else 0)
```
   `val = 5`，孩子增益 `[3, -2, 4]` → `(12, 9)`。

**Python 提醒**：`dict` 以节点为键时，默认比较是对象身份，两个值相同的不同节点不会混淆；但如果给 `TreeNode` 自己定义了 `__eq__` 却没有 `__hash__`，实例就变成不可哈希，字典用法会直接报 `TypeError`。
