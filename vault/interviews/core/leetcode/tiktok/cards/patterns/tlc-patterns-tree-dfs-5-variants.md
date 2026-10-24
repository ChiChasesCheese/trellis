---
id: tlc-patterns-tree-dfs-5-variants
node: patterns.tree-dfs
type: qa
step: 5
---
## Q
**二叉树 DFS（Tree DFS）｜变形：向下传前缀和、向下传长度、返回距离列表、由遍历序列建树**

路径总和 III（LC 437）、最长连续序列（LC 298）、好叶子对（LC 1530）、由前序与中序建树（LC 105）的写法各自怎样？

## A
**LC 437 前缀和 + 回溯**：路径必须向下，不必从根开始。`cnt` 记录「根到当前节点这条路径上」每个前缀和出现的次数。

```python
from collections import Counter
def path_sum(root: TreeNode | None, target_sum: int) -> int:
    cnt: Counter[int] = Counter({0: 1})
    def dfs(node: TreeNode | None, pre: int) -> int:
        if node is None:
            return 0
        pre += node.val
        res = cnt[pre - target_sum]        # 以 node 结尾、和为 target 的向下路径数
        cnt[pre] += 1
        res += dfs(node.left, pre) + dfs(node.right, pre)
        cnt[pre] -= 1                      # 回溯：离开 node 的子树时撤销
        return res
    return dfs(root, 0)
```

`[10,5,-3,3,2,null,11,3,-2,null,1], 8` → `3`；`[5,4,8,11,null,13,4,7,2,null,null,5,1], 22` → `3`。漏掉 `cnt[pre] -= 1`：树 `[2,2,3]`、目标 `1` 得 `1`（左兄弟的前缀和泄漏过来），正确是 `0`。

**LC 298 把当前长度向下传**：`length = length + 1 if node.val == parent_val + 1 else 1`，再 `best = max(best, length)`；`[1,null,3,2,4,null,null,null,5]` → `3`。

**LC 1530 返回距离列表**：每个叶子返回 `[1]`；内部节点拿到左右列表，满足 `a + b <= distance` 的两两配对计数，再把所有距离加 1 且只保留 `< distance` 的向上传。`distance <= 10`，列表很短。

**LC 105 由前序 + 中序建树**：前序的第一个是根，在中序中的位置把序列分成左右子树；用字典 `值 -> 中序下标` 做到 `O(1)` 定位，总 `O(n)`。

```python
def build_tree(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    pos = {v: i for i, v in enumerate(inorder)}
    it = iter(preorder)                    # 前序依次给出各子树的根
    def build(lo: int, hi: int) -> TreeNode | None:
        if lo > hi:
            return None
        root = TreeNode(next(it))
        mid = pos[root.val]
        root.left = build(lo, mid - 1)     # 先建左子树：前序里左子树排在前面
        root.right = build(mid + 1, hi)
        return root
    return build(0, len(inorder) - 1)
```
