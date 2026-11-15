---
slug: smallest-string-starting-from-leaf
---
## Q
**LC 988 从叶结点开始的最小字符串**｜Medium

二叉树每个结点的值是 `0..25`，对应字母 `a..z`。求从任一叶结点出发、沿父指针走到根形成的所有字符串中，字典序最小的一个。

## A
**一句话。** 自顶向下 DFS，路径字符串每走一步把新字符放在前面（叶子端在左），到叶子时与当前最小值比较。

```python
def smallest_from_leaf(root):
    best = "~"                       # '~' 比所有小写字母大
    def dfs(node, suffix):
        nonlocal best
        if not node:
            return
        suffix = chr(97 + node.val) + suffix   # 新结点放最前
        if not node.left and not node.right:
            best = min(best, suffix)           # 到叶子：候选答案
        dfs(node.left, suffix)
        dfs(node.right, suffix)
    dfs(root, "")
    return best
```

**复杂度。** 时间 `O(nh)`（字符串拼接），空间 `O(h)`。

**易错点。**
- 把字符追加到路径末尾：字符串要从叶子读到根，叶子端应在最左，所以新字符放前面。
- 在非叶结点上也更新答案：路径必须到叶子，`"ab"` 比 `"b"` 小，但只走半程不合法。
- 单孩子结点当叶子：只有两边都为空才是叶子。

**追问。**
- 为什么不能边走边剪枝？：自顶向下时较大的前缀可能因为后面的字符变小，字符串在左端补长，不单调。
- 与 LC 129 求根到叶子节点数字之和相比？：同样的 DFS 骨架，只是路径累计方式不同。

**同模式。** LC 129 求根节点到叶节点数字之和、LC 257 二叉树的所有路径、LC 1022 从根到叶的二进制数之和
