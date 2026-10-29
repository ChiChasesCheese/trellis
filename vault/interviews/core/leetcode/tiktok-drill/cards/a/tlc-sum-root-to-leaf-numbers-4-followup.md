---
id: tlc-sum-root-to-leaf-numbers-4-followup
node: a.sum-root-to-leaf-numbers
type: qa
step: 4
---
## Q
**LC 129 求根到叶子节点数字之和**｜追问

面试官接着问：（1）树很深，递归会爆栈，怎么改成迭代？（2）要返回每条路径本身而不是求和（LC 257）？（3）节点值是 `0` 到 `9`，但数字可能很长，结果要对 `10^9 + 7` 取模，什么时候取？

## A
1. **迭代。** 显式栈存 `(节点, 前缀数)`，弹出时接长一位，叶子累加：
```python
def sum_numbers_iter(root: TreeNode | None) -> int:
    total = 0
    stack: list[tuple[TreeNode, int]] = [(root, 0)] if root else []
    while stack:
        node, acc = stack.pop()
        acc = acc * 10 + node.val
        if node.left is None and node.right is None:
            total += acc
            continue
        if node.right:
            stack.append((node.right, acc))
        if node.left:
            stack.append((node.left, acc))
    return total
```
时间 `O(n)`，栈里最多存 `O(h)` 到 `O(n)` 个元素。
2. **返回路径。** 递归时维护 `path` 列表：进入节点 `append(node.val)`，离开 `pop()`；到叶子把 `path` 的**拷贝**（`path[:]` 或 `"->".join(...)`）放进结果。忘记拷贝，所有结果会指向同一个被反复修改的列表。
3. **取模。** 每一步 `acc = (acc * 10 + val) % MOD`，叶子处累加后也取模；不要等整数拼完再取模（Python 虽不溢出，但其他语言会）。

**Python 提醒**：用 `int("".join(path))` 把长路径转成整数时，Python 3.11 之后超过 4300 位的十进制字符串会抛 `ValueError`；`acc * 10 + val` 的整数运算没有这个限制，面试里优先用它。
