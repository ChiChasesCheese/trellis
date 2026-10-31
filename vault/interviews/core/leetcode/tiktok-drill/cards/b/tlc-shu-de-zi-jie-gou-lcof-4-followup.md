---
id: tlc-shu-de-zi-jie-gou-lcof-4-followup
node: b.shu-de-zi-jie-gou-lcof
type: qa
step: 4
---
## Q
**剑指 Offer 26 树的子结构**｜追问

面试官接着问：（1）`tree1` 是 `10000` 层的链，递归会怎样，怎么改？（2）改成“另一棵树的子树”（LC 572，要求完全相同）怎么改？（3）两棵树都很大，`O(m * n)` 太慢，能做到 `O(m + n)` 吗？

## A
1. **深链与显式栈。** 递归深度等于树高，`10000` 层的链会超过 CPython 默认递归上限（约 `1000`）而抛 `RecursionError`；可以 `sys.setrecursionlimit` 调高，或改成显式栈：`match` 用栈同步下降，外层用栈遍历 `tree1` 的每个节点：
```python
def is_sub_structure_stack(tree1: TreeNode | None, tree2: TreeNode | None) -> bool:
    if tree1 is None or tree2 is None:
        return False                            # 空树不算子结构

    def match(a: TreeNode | None, b: TreeNode | None) -> bool:
        stack = [(a, b)]                        # 同步下降：a 的结构必须“包住”b
        while stack:
            x, y = stack.pop()
            if y is None:
                continue                        # b 这一支到头了，a 那边多出来的不管
            if x is None or x.val != y.val:
                return False
            stack.append((x.left, y.left))
            stack.append((x.right, y.right))
        return True

    todo = [tree1]                              # 用显式栈遍历 tree1 的每个结点当候选根
    while todo:
        node = todo.pop()
        if node.val == tree2.val and match(node, tree2):
            return True
        todo.extend(c for c in (node.left, node.right) if c)
    return False
```
2. **LC 572。** 比较函数要求两边同时为空，或同时有值且相等；候选根的遍历不变：
```python
def is_subtree(root: TreeNode | None, sub: TreeNode | None) -> bool:
    def same(a: TreeNode | None, b: TreeNode | None) -> bool:
        if a is None or b is None:
            return a is b                       # 两边必须同时为空
        return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)

    if root is None:
        return sub is None
    return same(root, sub) or is_subtree(root.left, sub) or is_subtree(root.right, sub)
```
3. **`O(m + n)`（只对 LC 572 成立）。** 先序序列化，空节点用 `#`，每个值前加分隔符，避免 `12` 和 `2` 混淆；子树对应序列里的一段连续子串：
```python
def serialize(root: TreeNode | None) -> str:
    out: list[str] = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            out.append(",#")
        else:
            out.append(f",{node.val}")
            stack.append(node.right)
            stack.append(node.left)
    return "".join(out)
```
`serialize(sub) in serialize(root)` 即答案，CPython 的子串查找在新版本中是线性时间。子结构因为允许 `tree1` 多出孩子，序列不再是连续子串，这个做法不适用，需要树哈希之类的更复杂手段。

**Python 提醒**：序列化时值与值之间一定要有分隔符：不加分隔符，节点 `12` 与节点 `1` 加节点 `2` 的序列都是 `"12"`，`in` 判断会产生假阳性。
