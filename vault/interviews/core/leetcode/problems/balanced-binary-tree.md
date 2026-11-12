---
slug: balanced-binary-tree
---
## Q
**LC 110 平衡二叉树**｜Easy

判断二叉树是否高度平衡：每个节点左右子树高度差的绝对值不超过 `1`。

## A
**一句话。** 后序遍历自底向上算高度，发现某节点高度差大于 `1` 就返回哨兵 `-1` 一路上传。

```python
def is_balanced(root):
    def height(node):
        if node is None:
            return 0
        l = height(node.left)
        if l == -1:
            return -1
        r = height(node.right)
        if r == -1 or abs(l - r) > 1:
            return -1
        return max(l, r) + 1

    return height(root) != -1
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 只比较根的左右高度：`[1,2,2,3,null,null,3,4,null,null,4]` 根两边高度相同，但内部节点 `2` 不平衡，应为 `False`，每个节点都要查。
- 见到 `-1` 还继续算差：`-1` 会被当成高度参与比较，要立刻返回。

**追问。**
- 为什么不能每个节点单独求高度再比较？：每层重复求高度，最坏 `O(n²)`。
- 把普通 BST 变平衡呢？：LC 1382，中序得有序数组，再取中点递归建树。

**同模式。** LC 104 二叉树的最大深度、LC 543 二叉树的直径、LC 124 二叉树中的最大路径和、LC 1382 将二叉搜索树变平衡
