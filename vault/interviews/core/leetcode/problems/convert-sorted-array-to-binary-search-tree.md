---
slug: convert-sorted-array-to-binary-search-tree
---
## Q
**LC 108 将有序数组转换为二叉搜索树**｜Easy

把升序数组转换成一棵高度平衡的二叉搜索树。

## A
**一句话。** 取区间中点作根，左半递归建左子树、右半递归建右子树，两边个数至多差 `1`。

```python
def sorted_array_to_bst(nums):
    def build(lo, hi):          # 左闭右开
        if lo >= hi:
            return None
        mid = (lo + hi) // 2
        node = TreeNode(nums[mid])
        node.left = build(lo, mid)
        node.right = build(mid + 1, hi)
        return node
    return build(0, len(nums))
```

**复杂度。** 时间 `O(n)`，空间 `O(log n)`。

**易错点。**
- 用切片 `nums[:mid]` 递归：每层复制数组，时间 `O(n log n)`；应传下标。
- 偶数个元素时中点偏左偏右都对：输出不唯一，判题看「是 BST 且平衡」。

**追问。**
- 输入是有序链表（LC 109）？：快慢指针找中点，或中序遍历同时建树。
- 能保证结果唯一吗？：不能，取偏左或偏右中点会得到不同的合法树。

**同模式。** LC 109 有序链表转换二叉搜索树、LC 105 从前序与中序遍历序列构造二叉树、LC 1382 将二叉搜索树变平衡
