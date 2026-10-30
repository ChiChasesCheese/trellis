---
id: tlc-shu-de-zi-jie-gou-lcof-4-followup
node: p5.shu-de-zi-jie-gou-lcof
type: qa
step: 4
---
## Q
**剑指 Offer 26 树的子结构**｜追问

面试官接着问：（1）改成“另一棵树的子树”（LC 572，要求完全相同）怎么改？（2）两棵树都很大，`O(m * n)` 太慢，能做到 `O(m + n)` 吗？（3）用递归写要注意什么？

## A
1. **LC 572。** 比较函数要求两边同时为空，或同时有值且相等；候选根的遍历不变：
```python
def is_subtree(root: TreeNode | None, sub: TreeNode | None) -> bool:
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

    todo = [root] if root else []
    while todo:
        node = todo.pop()
        if same(node, sub):
            return True
        todo.extend(c for c in (node.left, node.right) if c)
    return sub is None
```
2. **`O(m + n)`（只对 LC 572 成立）。** 先序序列化，空节点用 `#`，每个值前加分隔符，避免 `12` 和 `2` 混淆；子树对应序列里的一段连续子串：
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
3. **递归写法。** 外层与 `match` 各一个递归函数，代码最短；链状树 `10000` 层超过默认递归上限，要 `sys.setrecursionlimit`，或者像上面这样改成显式栈。

**Python 提醒**：序列化时值与值之间一定要有分隔符：不加分隔符，节点 `12` 与节点 `1` 加节点 `2` 的序列都是 `"12"`，`in` 判断会产生假阳性。
