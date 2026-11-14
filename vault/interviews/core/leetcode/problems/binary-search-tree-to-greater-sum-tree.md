---
slug: binary-search-tree-to-greater-sum-tree
---
## Q
**LC 1038 从二叉搜索树到更大和树**｜Medium

把二叉搜索树每个节点的值改成树中所有大于等于它的值之和，返回根。

## A
**一句话。** 反向中序遍历（右、根、左）按降序访问，边走边累加，当前累加和就是新值。

```python
def bst_to_gst(root):
    total = 0

    def dfs(node):             # 右 -> 根 -> 左，降序
        nonlocal total
        if node is None:
            return
        dfs(node.right)
        total += node.val       # 先加自己（大于等于）
        node.val = total
        dfs(node.left)

    dfs(root)
    return root
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 先赋值再累加：得到的是「严格大于」之和，少了自己。
- 用普通中序（左根右）：那是升序，得到的是小于等于之和。

**追问。**
- 不用递归、`O(1)` 空间？：反向 Morris 遍历，借左右指针做线索。
- 和 LC 538 的区别？：同一道题，只是题号不同。

**同模式。** LC 230 二叉搜索树中第 K 小的元素、LC 538 把二叉搜索树转换为累加树、LC 98 验证二叉搜索树
