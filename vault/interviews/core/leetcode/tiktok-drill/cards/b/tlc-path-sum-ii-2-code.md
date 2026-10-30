---
id: tlc-path-sum-ii-2-code
node: b.path-sum-ii
type: qa
step: 2
---
## Q
**LC 113 路径总和 II**｜写出 Python 实现

二叉树根节点 `root`（节点数 `0..5000`，值 `-1000..1000`）与整数 `targetSum`。返回所有根到叶子、节点值之和等于 `targetSum` 的路径，每条路径是节点值列表。树可能是 5000 层的链。

## A
**思路。** 递归 DFS `dfs(node, rest)`，`rest` 是进入前还差多少。进入节点把值 `append` 到共享的 `path` 并更新 `rest`；若是叶子且 `rest == 0`，拷贝路径入答案；递归左右孩子；返回前把 `path` 的最后一个值 `pop`，路径回到进入该节点之前的状态。

```python
def path_sum(root: TreeNode | None, target_sum: int) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []                          # 当前根到 node 的路径，所有层共享同一个列表

    def dfs(node: TreeNode | None, rest: int) -> None:
        if node is None:
            return
        path.append(node.val)                     # 进入节点
        rest -= node.val
        if node.left is None and node.right is None and rest == 0:
            res.append(path[:])                   # 只有叶子且恰好用完才收：拷贝一份，path 之后还会变
        dfs(node.left, rest)
        dfs(node.right, rest)
        path.pop()                                # 离开节点：回溯

    dfs(root, target_sum)
    return res
```

**运行。** 例 1 → `[[5, 4, 11, 2], [5, 8, 4, 5]]`；`[1,2,3], 5` → `[]`；`[1,2], 0` → `[]`；`None, 0` → `[]`；`[1], 1` → `[[1]]`；`[-2,null,-3], -5` → `[[-2, -3]]`；5000 层的链调高递归上限后正常返回，默认上限下抛 `RecursionError`。

**复杂度。** 时间 `O(n + k·h)`（遍历 `n` 个节点，`k` 条命中路径各拷贝 `O(h)`）；空间 `O(h)`，是递归栈和 `path`，不含输出。

**写法要点。** `path` 在闭包里共享，`append` 在函数头、`pop` 在函数尾，进出成对，回溯不需要额外标记；`rest` 作参数随递归传下去，每层各有一份，不会在回溯时出错；`path[:]` 是浅拷贝，元素是整数，足够；先递归左再递归右，结果顺序是从左到右；遇到 `None` 直接返回，所以不必在调用前判断孩子是否存在。深度超过约 `1000` 要 `sys.setrecursionlimit`，或用「追问」卡的显式栈版本。
