---
id: tlc-shu-de-zi-jie-gou-lcof-2-code
node: p5.shu-de-zi-jie-gou-lcof
type: qa
step: 2
---
## Q
**剑指 Offer 26 树的子结构**｜写出 Python 实现

给定两棵二叉树 `tree1`、`tree2`（节点数 `0` 到 `10000`），判断 `tree2` 是否是 `tree1` 的子结构：`tree1` 中存在某个节点，以它为根向下，`tree2` 的结构和节点值都能对上，`tree1` 在对应位置多出来的孩子不影响。空树不是任何树的子结构。链状树 `10000` 层也不能报错。

## A
**思路。** 外层用栈遍历 `tree1` 的每个节点，值等于 `tree2` 根的才进入 `match`。`match` 也用栈同步下降：`b` 的节点为空就跳过这一支，`a` 缺节点或值不同就失败，否则把左右孩子对压栈。

```python
def is_sub_structure(tree1: TreeNode | None, tree2: TreeNode | None) -> bool:
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

运行：`([1,7,5], [6,1])` → `False`，`([3,6,7,1,8], [6,1])` → `True`，`(空, [1])` → `False`，`([1], 空)` → `False`，`([1,2,3], [1,2,3,4])` → `False`；`10000` 层左链配 `[0]`（全 `0`）→ `True`，配 `[1]` → `False`。

**复杂度。** 时间 `O(m * n)`（`m`、`n` 是两棵树的节点数）；空间 `O(m + n)`，两个栈的最坏规模。

**写法要点。**
- `match` 先判断 `y is None`，再判断 `x is None or x.val != y.val`：顺序保证 `x.val` 访问时 `x` 非空，也让“`b` 已到头”优先于“`a` 缺节点”。
- 把递归改成栈：外层与内层都不递归，链状树 `10000` 层也不会 `RecursionError`；元组 `(x, y)` 入栈、`x, y = stack.pop()` 解包。
- `todo.extend(c for c in (node.left, node.right) if c)`：生成器表达式过滤空孩子，一行完成两个孩子入栈。
- 先比较根的值再调用 `match`，省掉绝大多数无谓的函数调用。
