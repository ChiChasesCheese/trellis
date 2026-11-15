---
slug: binary-tree-paths
---
## Q
**LC 257 二叉树的所有路径**｜Easy

按任意顺序返回所有从根到叶子的路径，格式如 `"1->2->5"`。

## A
**一句话。** DFS 带着当前路径往下走，到叶子时把路径拼成字符串收集起来。

```python
def binary_tree_paths(root):
    ans = []
    def dfs(node, path):
        path = path + [str(node.val)]  # 新列表，不用回溯
        if node.left is None and node.right is None:
            ans.append("->".join(path))  # 到叶子才收集
            return
        if node.left:
            dfs(node.left, path)
        if node.right:
            dfs(node.right, path)
    dfs(root, [])
    return ans
```

**复杂度。** 时间 `O(n·h)`（拼路径），空间 `O(n·h)`（输出）。

**易错点。**
- 在空结点处收集：一个孩子为空的结点会被当成叶子，路径重复或多出半截。
- 共用同一个列表却不回溯：`append` 后不 `pop`，路径会越来越长。

**追问。**
- 回溯写法？：共用一个 `path` 列表，进入时 `append`、返回前 `pop`，省去复制。
- 只要路径条数？：等于叶子个数，不必拼字符串。

**同模式。** LC 112 路径总和、LC 113 路径总和 II、LC 129 求根节点到叶节点数字之和
