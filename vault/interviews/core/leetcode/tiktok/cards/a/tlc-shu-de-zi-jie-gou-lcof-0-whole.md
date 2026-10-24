---
id: tlc-shu-de-zi-jie-gou-lcof-0-whole
node: a.shu-de-zi-jie-gou-lcof
type: qa
---
## Q
**剑指 Offer 26 树的子结构**｜Medium · 字节 高频

给两棵二叉树 `tree1` 和 `tree2`，判断 `tree2` 是否是 `tree1` 的**子结构**：存在 `tree1` 的某个节点，以它为根向下，`tree2` 的每个节点都能在相同位置找到值相同的节点（`tree2` 的结构是 `tree1` 中那一块的一部分，不要求走到 `tree1` 的叶子）。空树不是任何树的子结构。节点个数 `0 <= n <= 10000`。例：`tree1 = [1,7,5]`，`tree2 = [6,1]` → `false`；`tree1 = [3,6,7,1,8]`，`tree2 = [6,1]` → `true`（`tree1` 中的节点 `6` 有左孩子 `1`，另有右孩子 `8` 不影响）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 两层判断：外层遍历 `tree1` 的每个节点，把它当作候选根；内层 `match(a, b)` 同步向下比较，`b` 走到空就算这一支匹配成功，`a` 走到空或值不同就失败。外层 `O(m)` 个候选，每个内层最多 `O(n)`，总 `O(m * n)`，其中 `m`、`n` 分别是 `tree1`、`tree2` 的节点数。

**识别。** 「树里是否包含某个形状」是**树匹配**问题：先找起点（遍历每个节点），再验证从起点向下是否吻合。空间上，`n` 可达 `10000`，一条链就有 `10000` 层，递归会超过 Python 的默认递归上限，用显式栈更稳妥。要特别看清“子结构”和“子树”的区别：子结构只要求 `tree2` 被包含，`tree1` 的对应节点可以有更多孩子。

**推导。** 暴力：枚举 `tree1` 的每个节点作为根，逐个与 `tree2` 比较。这就是最优思路的骨架，复杂度 `O(m * n)`；更快的 `O(m + n)` 需要序列化再字符串匹配，且只适用于“子树”（完全相同的子树）这个更严格的版本，子结构不能直接这么做。比较函数的关键在判断顺序：先看 `b` 是否到头（到头则这一支成功，不管 `a` 还有没有），再看 `a` 是否缺少对应节点或值不同（失败），然后同时检查左右两支。

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

运行：`[1,7,5]` 与 `[6,1]` → `False`，`[3,6,7,1,8]` 与 `[6,1]` → `True`，`tree1` 为空 → `False`，`tree2` 为空 → `False`，`[1,2,3]` 与 `[1,2,3,4]` → `False`；`tree1` 是 10000 层的左链、`tree2 = [0]`（全部节点值为 `0`）→ `True`，`tree2 = [1]` → `False`。

**复杂度。** 时间 `O(m * n)`：`m` 个候选根，每个最多比较 `tree2` 的 `n` 个节点；空间 `O(m + n)`：两个显式栈在最坏情况下的大小。

**易错点。**
- 把“子结构”当成“子树”（LC 572）：要求 `a` 的这一块与 `b` 完全相同，包括 `a` 多出来的孩子。`[3,6,7,1,8]` 与 `[6,1]` 会得到 `False`，正确是 `True`。
- `match` 里先判断 `a` 为空再判断 `b` 为空：`b` 为空时不管 `a` 如何都应成功。顺序写反，`b` 提前结束的分支会被判失败。
- 空树：任何一棵为空都返回 `False`；不要沿用“空树是任何树的子树”的数学约定。

**追问。**
- LC 572（另一棵树的子树）：`match` 改成两边必须同时为空或同时有值且相等，其他不变。
- 想要 `O(m + n)`：把两棵树按先序序列化（空节点用 `#` 占位，值前加分隔符），再判断 `serialize(sub) in serialize(root)`；这只对 LC 572 成立。
- 用递归写：`match` 和外层遍历各一个递归函数，代码最短，但链状树 `10000` 层需要 `sys.setrecursionlimit`。

**同模式。** LC 572 另一棵树的子树、LC 100 相同的树、LC 101 对称二叉树、LC 226 翻转二叉树。
