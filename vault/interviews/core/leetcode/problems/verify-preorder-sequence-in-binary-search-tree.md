---
slug: verify-preorder-sequence-in-binary-search-tree
---
## Q
**LC 255 验证前序遍历序列二叉搜索树**｜Medium

给无重复元素的数组 `preorder`，判断它是否是某棵二叉搜索树的前序遍历序列。

## A
**一句话。** 按「根、左、右」模拟建树：子树只接受落在 `(lo, hi)` 内的下一个数，最后看序列是否恰好用完。

```python
def verify_preorder(preorder):
    n, i = len(preorder), 0

    def build(lo, hi):
        nonlocal i
        if i == n or not lo < preorder[i] < hi:
            return
        root = preorder[i]
        i += 1
        build(lo, root)       # 左子树值域 (lo, root)
        build(root, hi)       # 右子树值域 (root, hi)

    build(-inf, inf)
    return i == n
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 忘了检查 `i == n`：`[5,2,6,1,3]` 消费到 `6` 就卡住，却返回 `True`，应为 `False`。
- 降序序列是 `10^4` 层的左链：超过 CPython 默认递归上限，要调高上限。

**追问。**
- 能 `O(1)` 空间吗？：用单调栈，弹出的最大值作为下界 `low`，之后任何 `<= low` 的数都非法；把序列本身当栈即可。
- 后序遍历怎么验证？：从右往左读，镜像地套用同一做法。

**同模式。** LC 449 序列化和反序列化二叉搜索树、LC 1008 前序遍历构造二叉搜索树、LC 98 验证二叉搜索树、LC 331 验证二叉树的前序序列化
