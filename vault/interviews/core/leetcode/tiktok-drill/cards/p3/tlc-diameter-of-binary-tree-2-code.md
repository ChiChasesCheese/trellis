---
id: tlc-diameter-of-binary-tree-2-code
node: p3.diameter-of-binary-tree
type: qa
step: 2
---
## Q
**LC 543 二叉树的直径**｜写出 Python 实现

二叉树根节点 `root`（节点数 `1..10^4`，值 `-100..100`）。返回直径：树中任意两节点之间最长路径的边数，路径可以不经过根。注意树可能是 `10^4` 层的链。

## A
**思路。** 递归后序。`height(node)` 返回子树高度（按节点数），空节点返回 `0`；两个孩子的高度算完后，用 `左高 + 右高` 更新答案，再返回 `1 + max(左高, 右高)`。

```python
def diameter_of_binary_tree(root: TreeNode | None) -> int:
    best = 0

    def height(node: TreeNode | None) -> int:    # 子树高度（按结点数），空树为 0
        nonlocal best
        if node is None:
            return 0
        lh, rh = height(node.left), height(node.right)
        best = max(best, lh + rh)                # 经过 node 的最长路径的边数 = 左高 + 右高
        return 1 + max(lh, rh)

    height(root)
    return best
```

**运行。** `[1,2,3,4,5]` → `3`；`[1,2]` → `1`；`[1]` → `0`；`None` → `0`；`10^4` 层的左斜链在默认递归上限下抛 `RecursionError`，调高上限后 → `9999`。

**复杂度。** 时间 `O(n)`：每个节点访问一次；空间 `O(h)`：递归栈，`h` 是树高，链状树时 `O(n)`（`10^4` 层会触到默认递归上限）。

**写法要点。** 嵌套函数里要修改外层的整数变量，必须声明 `nonlocal best`，否则 `best = …` 会新建局部变量；`lh, rh = height(node.left), height(node.right)` 一行取两个孩子的高度；空节点在递归入口返回 `0`，省去对孩子判空；一次递归同时返回高度、顺手更新全局答案，是树形 DP 的通用写法。
