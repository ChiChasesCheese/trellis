---
id: tlc-subtree-of-another-tree-2-code
node: a.subtree-of-another-tree
type: qa
step: 2
---
## Q
**LC 572 另一个树的子树**｜写出 Python 实现

`root` 有 `1` 到 `2000` 个节点，`subRoot` 有 `1` 到 `1000` 个节点，值在 `[-10^4, 10^4]`。判断 `root` 中是否有一棵子树与 `subRoot` 结构和值完全相同（`root` 自己也算）。树可能退化成链，不要依赖递归。

## A
**思路。** 把每棵树迭代先序序列化：节点写成 `,值`，空孩子写成 `#`；`subRoot` 的序列是 `root` 序列的子串，当且仅当 `root` 里有匹配的子树。值前面的逗号保证数字边界对齐，`#` 保证匹配到叶子为止。

```python
def is_subtree(root: TreeNode | None, sub_root: TreeNode | None) -> bool:
    def serialize(tree: TreeNode | None) -> str:
        parts: list[str] = []
        stack = [tree]                             # 迭代先序，避免深链表式的树爆递归栈
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

运行：`[3,4,5,1,2]` 里找 `[4,1,2]` → `True`；`[3,4,5,1,2,null,null,null,null,0]` 里找 `[4,1,2]` → `False`；深度 2000 的右链里找深度 1000 的右链 → `True`，深度 2000 的左链里找右链 → `False`。

**复杂度。** 时间 `O(m + n)`：两次序列化各线性，`in` 在 CPython 3.10 起对长模式用双向算法，最坏线性；空间 `O(m + n)`。

**写法要点。** 内层函数 `serialize` 共用一个实现，两棵树都用；`parts` 列表加 `"".join` 比反复 `+=` 字符串高效；`f",{node.val}"` 里负数写成 `,-5`，仍能和别的数字区分；先压右孩子再压左孩子，出栈顺序才是「根、左、右」。
