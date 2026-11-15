---
slug: sum-of-root-to-leaf-binary-numbers
---
## Q
**LC 1022 从根到叶的二进制数之和**｜Easy

二叉树每个结点值是 `0` 或 `1`，每条从根到叶的路径表示一个二进制数（根为最高位）。求所有路径表示的数之和。

## A
**一句话。** 自顶向下 DFS，带着当前值：每向下一层 `cur = cur * 2 + val`，到叶子返回，两边求和。

```python
def sum_root_to_leaf(root):
    def dfs(node, cur):
        if not node:
            return 0
        cur = cur * 2 + node.val         # 追加一位
        if not node.left and not node.right:
            return cur                   # 叶子：一条路径结束
        return dfs(node.left, cur) + dfs(node.right, cur)
    return dfs(root, 0)
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 在空结点处返回 `cur`：只有一个孩子的结点会把同一条路径算两次，应在叶子处返回，空结点返回 `0`。
- 把 `cur` 写成全局变量累加：多条路径共用一个变量，回溯时要还原，传参更干净。

**追问。**
- 为什么不需要回溯还原？：`cur` 是参数，递归调用各自持有，不会互相污染。
- 路径是十进制数字（LC 129）怎么改？：把 `* 2` 换成 `* 10`。

**同模式。** LC 129 求根节点到叶节点数字之和、LC 988 从叶结点开始的最小字符串、LC 257 二叉树的所有路径
