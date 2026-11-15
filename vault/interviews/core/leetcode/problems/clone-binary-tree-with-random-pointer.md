---
slug: clone-binary-tree-with-random-pointer
---
## Q
**LC 1485 克隆含随机指针的二叉树**｜Medium

二叉树每个结点除 `left`、`right` 外还有一个 `random` 指针，指向树中任意结点或为空。深拷贝这棵树，返回新树的根。

## A
**一句话。** 用哈希表记录「原结点 → 新结点」，递归克隆左右孩子和 `random`，已克隆过的直接复用，这样随机指针也能指对。

```python
def copy_random_binary_tree(root):
    mp = {None: None}                 # 原结点 -> 新结点
    def clone(node):
        if node not in mp:
            mp[node] = NodeCopy(node.val)   # 先登记再递归：防止循环
            mp[node].left = clone(node.left)
            mp[node].right = clone(node.right)
            mp[node].random = clone(node.random)
        return mp[node]
    return clone(root)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 递归之后才登记映射：`random` 指针可能指回祖先，形成环，导致无限递归。
- 把 `random` 指向原树结点：必须指向新树里对应的结点，要通过映射取。
- 忘了空指针：`mp[None] = None`，让空孩子自然返回空。

**追问。**
- 链表版本（LC 138）怎么做？：同样的哈希表，或把新结点穿插在原结点后面，省去哈希。
- 图的克隆（LC 133）有什么共同点？：都靠「原对象到新对象」的映射处理共享与环。

**同模式。** LC 138 随机链表的复制、LC 133 克隆图、LC 297 二叉树的序列化与反序列化
