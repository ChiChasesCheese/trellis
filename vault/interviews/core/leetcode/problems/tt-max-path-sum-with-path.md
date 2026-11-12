---
slug: tt-max-path-sum-with-path
---
## Q
**二叉树最大路径和（并输出路径）**｜Hard

二叉树节点值可为负，路径是相连的节点序列，不要求过根或叶。求最大路径和，并返回取得最大和的那条路径（节点序列）。例：`-10 -> (9, 20 -> (15, 7))` → `42`，路径 `[15, 20, 7]`。

## A
**一句话。** 后序 DFS 算每个节点向下单链的最大收益 `gain`（负分支当 `0`），经过节点的路径和 `val + 左 + 右` 更新全局最优并记下拐点，再沿 `down` 展开左右两臂。

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def max_path_sum(root):
    gain = {}      # gain[v]：从 v 向下单链最大和
    down = {}      # down[v]：最优单链在 v 之后走向的孩子
    best, peak = root.val, root    # peak：最优路径的拐点

    def dfs(node):
        nonlocal best, peak
        if node is None:
            return 0
        left = max(dfs(node.left), 0)     # 负分支不要
        right = max(dfs(node.right), 0)
        down[node] = (node.left if left and left >= right
                      else node.right if right else None)
        gain[node] = node.val + max(left, right)
        if node.val + left + right > best:
            best, peak = node.val + left + right, node
        return gain[node]

    dfs(root)

    def arm(child):
        chain = []
        while child:
            chain.append(child)
            child = down[child]
        return chain

    lt, rt = peak.left, peak.right
    L = arm(lt) if lt and gain[lt] > 0 else []
    R = arm(rt) if rt and gain[rt] > 0 else []
    return best, L[::-1] + [peak] + R
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 不放弃负分支：`1 -> (-5, 3)` 应为 `4`，不带 `max(0, …)` 得 `3`。
- 向父亲返回两条臂：`gain` 只能带一条链，否则 `1 -> (2 -> (3, 3))` 会得到非法的 `9`，应为 `8`。
- 答案初值取 `0`：全负的树 `-3` 得 `0`，应为 `-3`，初值取根的值。
- 还原路径时左臂忘了反转：路径不是从一端走到另一端。

**追问。**
- 链状树递归超限怎么办？：调大 `setrecursionlimit`，或先序入表后倒序处理（孩子先于父亲）改成循环。
- 多条路径并列最大？：返回任意一条；要全部就收集所有等于 `best` 的拐点分别展开。

**同模式。** LC 124 二叉树中的最大路径和、LC 543 二叉树的直径、LC 687 最长同值路径、LC 1372 二叉树中的最长交错路径
