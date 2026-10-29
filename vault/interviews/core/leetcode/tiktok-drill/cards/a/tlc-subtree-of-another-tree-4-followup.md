---
id: tlc-subtree-of-another-tree-4-followup
node: a.subtree-of-another-tree
type: qa
step: 4
---
## Q
**LC 572 另一个树的子树**｜追问

面试官接着问：（1）不用字符串，纯比较怎么写，复杂度多少？（2）想要有保证的线性时间，还有什么办法？（3）如果 `root` 非常大、要对很多棵不同的 `subRoot` 做查询呢？

## A
1. **逐对比较**：遍历 `root`，在值与 `subRoot.val` 相同的节点上做「两树是否相同」。比较和遍历都用显式栈，避免递归深度问题。最坏 `O(m·n)`（例如 `root` 与 `subRoot` 都是全 `1` 的链），空间 `O(h)`。

```python
def is_subtree_pairs(root: TreeNode | None, sub_root: TreeNode | None) -> bool:
    def same(a: TreeNode | None, b: TreeNode | None) -> bool:
        stack = [(a, b)]
        while stack:
            x, y = stack.pop()
            if x is None and y is None:
                continue
            if x is None or y is None or x.val != y.val:
                return False
            stack.append((x.left, y.left))
            stack.append((x.right, y.right))
        return True

    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        if node.val == sub_root.val and same(node, sub_root):
            return True
        stack.append(node.left)
        stack.append(node.right)
    return False
```

示例 1 → `True`，示例 2 → `False`。
2. **保证线性**：对序列用 KMP（失败函数），时间严格 `O(m + n)`；或者给每个子树算结构哈希（子树的哈希由根值和两个孩子的哈希合并而来），`root` 里哪个节点的哈希等于 `subRoot` 的哈希就匹配，注意用高质量的哈希或者再验证一次相等，防碰撞。
3. **多次查询**：对 `root` 只序列化一次并缓存，每个 `subRoot` 单独序列化再做子串查找；数据量再大时，对 `root` 的所有子树做哈希并存进字典，每次查询 `O(|subRoot|)`。

**Python 提醒**：`a in b` 对字符串是子串查找，对列表是「是否含有某个元素」，`[1, 2] in [0, 1, 2, 3]` 得到 `False`。想在先序序列里找连续片段，要用字符串，或者自己写 KMP。
