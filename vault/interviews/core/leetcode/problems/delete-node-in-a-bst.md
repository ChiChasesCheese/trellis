---
slug: delete-node-in-a-bst
---
## Q
**LC 450 删除二叉搜索树中的节点**｜Medium

删除 BST 中值为 `key` 的节点，保证结果仍是 BST，返回根节点。

## A
**一句话。** 按大小递归找到节点，用返回值接回子树；缺一个孩子就让另一个顶替，两个孩子就用右子树最小值（中序后继）覆盖再删后继。

```python
def delete_node(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        if not root.left:
            return root.right    # 含叶子
        if not root.right:
            return root.left
        succ = root.right        # 中序后继
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete_node(root.right, succ.val)
    return root
```

**复杂度。** 时间 `O(h)`，空间 `O(h)`。

**易错点。**
- 两个孩子时直接返回右孩子：丢掉左子树，`[5,3,6,2,4,null,7]` 删 `3` 丢了 `2`。
- 不用返回值接回：写成 `delete_node(root.left, key)` 不赋值，树不变。

**追问。**
- 用前驱（左子树最大值）行吗？：行，只是结果形状不同。
- 不想递归，`O(1)` 空间？：迭代找到节点和父节点，两个孩子时转成删后继，最后让孩子顶替。

**同模式。** LC 700 二叉搜索树中的搜索、LC 701 二叉搜索树中的插入操作、LC 669 修剪二叉搜索树、LC 98 验证二叉搜索树
