---
slug: sum-root-to-leaf-numbers
---
## Q
**LC 129 求根节点到叶节点数字之和**｜Medium

二叉树每个节点存一个 `0` 到 `9` 的数字，根到叶的路径表示一个数（`1->2->3` 即 `123`）。返回所有根到叶路径所表示的数之和。

## A
**一句话。** DFS 把「根到当前节点形成的数」向下传，`acc = acc*10 + val`，到叶子返回它。

```python
def sum_numbers(root):
    def dfs(node, acc):
        if not node:
            return 0
        acc = acc * 10 + node.val
        if not node.left and not node.right:
            return acc                 # 叶子：一条路径的数
        return dfs(node.left, acc) + dfs(node.right, acc)
    return dfs(root, 0)
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 到空节点才返回 `acc`：`[1,2]` 得 `25`，应为 `12`，根的空右孩子被多算一次。
- 用 `or` 判叶子：`[1,2]` 得 `1`，应为 `12`；只有一个孩子的节点不是叶子。

**追问。**
- 不想递归？：显式栈存 `(node, acc)`，叶子处累加。
- 要返回所有路径本身（LC 257）？：多维护 `path`，进入 `append`、离开 `pop`，收集时复制。

**同模式。** LC 112 路径总和、LC 257 二叉树的所有路径、LC 1022 从根到叶的二进制数之和、LC 988 从叶结点开始的最小字符串
