---
slug: subtree-of-another-tree
---
## Q
**LC 572 另一个树的子树**｜Easy

判断 `root` 中是否存在一棵子树，结构和节点值都与 `subRoot` 完全相同。

## A
**一句话。** 对 `root` 的每个节点做一次「两树是否完全相同」的递归比较。

```python
def is_same(a, b):
    if a is None or b is None:
        return a is b       # 同时为空才相同
    return (a.val == b.val and is_same(a.left, b.left)
            and is_same(a.right, b.right))

def is_subtree(root, sub_root):
    if root is None:
        return False
    return (is_same(root, sub_root)
            or is_subtree(root.left, sub_root)
            or is_subtree(root.right, sub_root))
```

**复杂度。** 时间 `O(mn)`，空间 `O(m)`。

**易错点。**
- 比较要到叶子为止：`4` 的后代多了一个 `0`，只比值会误判为 `true`。
- 值相等就返回：`root=[1,1]`、`subRoot=[1]` 根处不同，必须继续往孩子里找。

**追问。**
- 怎么做到线性？：两棵树先序序列化（空孩子记 `#`，值前加逗号），判子串；或用 KMP。
- 为什么序列化要加逗号和 `#`？：避免 `12` 里匹配出 `2`，并保留形状。

**同模式。** LC 100 相同的树、LC 652 寻找重复的子树、LC 1367 链表中的二叉树路径、LC 297 二叉树的序列化与反序列化
