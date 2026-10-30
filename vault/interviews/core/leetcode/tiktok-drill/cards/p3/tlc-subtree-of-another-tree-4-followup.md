---
id: tlc-subtree-of-another-tree-4-followup
node: p3.subtree-of-another-tree
type: qa
step: 4
---
## Q
**LC 572 另一个树的子树**｜追问

面试官接着问：（1）想要有保证的线性时间怎么做？（2）树很深、递归会超限，怎么改成不用递归？（3）如果 `root` 非常大、要对很多棵不同的 `subRoot` 做查询呢？

## A
1. **线性时间（序列化）**：两棵树各自先序序列化，空孩子记 `#`，每个值前加逗号；`subRoot` 的序列是 `root` 序列的子串，当且仅当存在匹配子树。`in` 在 CPython 3.10 起最坏线性，总时间 `O(m + n)`。下面用显式栈做先序，深链也不会 `RecursionError`；递归写法只有一行：`"#" if t is None else f",{t.val}{ser(t.left)}{ser(t.right)}"`。

```python
def is_subtree_serialize(root: TreeNode | None, sub_root: TreeNode | None) -> bool:
    def serialize(tree: TreeNode | None) -> str:
        parts: list[str] = []
        stack = [tree]
        while stack:
            node = stack.pop()
            if node is None:
                parts.append("#")                  # 空位也要记，才能区分形状
            else:
                parts.append(f",{node.val}")       # 值前加逗号，防止 "12" 里匹配出 "2"
                stack.append(node.right)
                stack.append(node.left)            # 后进先出：左子树先出栈
        return "".join(parts)

    return serialize(sub_root) in serialize(root)
```

示例 1 → `True`，示例 2 → `False`。不加分隔符时 `root = [12]`、`subRoot = [2]` 的序列是 `"12##"` 与 `"2##"`，子串成立，输出 `True`，正确是 `False`；不记空位时 `[1,2]`（`2` 是左孩子）与 `[1,null,2]` 的序列都是 `",1,2"`，同样会错判。

2. **显式栈**：主解的递归在深链上会超过默认上限，把两个遍历都改成显式栈，最坏 `O(m·n)`，空间 `O(h)`。

```python
def is_subtree_stack(root: TreeNode | None, sub_root: TreeNode | None) -> bool:
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
3. **多次查询**：对 `root` 只序列化一次并缓存，每个 `subRoot` 单独序列化再做子串查找；数据量再大时，对 `root` 的所有子树做结构哈希并存进字典，每次查询 `O(|subRoot|)`；要有保证的线性可以对序列用 KMP，哈希则要防碰撞。

**Python 提醒**：`a in b` 对字符串是子串查找，对列表是「是否含有某个元素」，`[1, 2] in [0, 1, 2, 3]` 得到 `False`。想在先序序列里找连续片段，要用字符串，或者自己写 KMP。
