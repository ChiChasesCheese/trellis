---
slug: largest-bst-subtree
---
## Q
**LC 333 最大二叉搜索子树**｜Medium

给二叉树，找出其中结点数最多的二叉搜索子树（左 < 根 < 右，且整棵子树都满足），返回它的结点数。

## A
**一句话。** 后序给每棵子树返回「是不是 BST、大小、最小值、最大值」；左最大 < 根 < 右最小才合并成更大的 BST。

```python
def largest_bst_subtree(root):
    best = 0
    def dfs(node):    # 返回 (是BST, 大小, 最小, 最大)
        nonlocal best
        if not node:
            return True, 0, inf, -inf
        lok, ls, lmin, lmax = dfs(node.left)
        rok, rs, rmin, rmax = dfs(node.right)
        if lok and rok and lmax < node.val < rmin:
            size = ls + rs + 1
            best = max(best, size)
            return True, size, min(lmin, node.val), \
                max(rmax, node.val)
        return False, 0, -inf, inf   # 不是 BST，祖先也不是
    dfs(root)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 只比较根与左右孩子：BST 要求整棵左子树都小于根，必须用子树的最大、最小值。
- 非 BST 返回的最值不设成 `(-inf, inf)`：会让祖先误判为合法。
- 空树的最小、最大值设成 `inf, -inf`：这样叶子自然满足比较。

**追问。**
- 为什么不能自顶向下逐个验证？：每个结点都做一次 LC 98 验证，最坏 `O(n^2)`；后序一次汇总才是线性。
- 要返回这棵子树的根呢？：在更新 `best` 时同时记下 `node`。

**同模式。** LC 98 验证二叉搜索树、LC 1373 二叉搜索子树的最大键值和、LC 543 二叉树的直径、LC 124 二叉树中的最大路径和
