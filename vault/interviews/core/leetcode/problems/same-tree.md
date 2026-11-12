---
slug: same-tree
---
## Q
**LC 100 相同的树**｜Easy

给两棵二叉树的根 `p`、`q`，判断它们是否结构相同且对应节点值相同。

## A
**一句话。** 两树相同，当且仅当同为空，或根值相等且左子树相同、右子树相同。

```python
def is_same_tree(p, q):
    if not p or not q:
        return p is q              # 同为空才相同
    return (p.val == q.val
            and is_same_tree(p.left, q.left)
            and is_same_tree(p.right, q.right))
```

**复杂度。** 时间 `O(min(n,m))`，空间 `O(h)`。

**易错点。**
- 只比遍历出的值序列、不带空标记：`[1,2]` 与 `[1,null,2]` 前序都是 `[1,2]`，会误判相同。
- 只判 `p` 为空就访问 `q.val`：`p` 非空 `q` 为空时抛 `AttributeError`，两个空要一起处理。

**追问。**
- 怎么判断子树（LC 572）？：对 `root` 的每个节点调用 `is_same_tree`，`O(mn)`。
- 不用递归怎么写？：队列成对入队 `(p, q)`，出队时同样先比空再比值。

**同模式。** LC 101 对称二叉树、LC 572 另一棵树的子树、LC 617 合并二叉树、LC 951 翻转等价二叉树
