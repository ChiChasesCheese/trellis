---
id: tlc-binary-tree-zigzag-level-order-traversal-4-followup
node: b.binary-tree-zigzag-level-order-traversal
type: qa
step: 4
---
## Q
**LC 103 二叉树的锯齿形层序遍历**｜追问

面试官接着问：（1）要**自底向上**的层序结果（最后一层在最前）？（2）想用 DFS（递归）写，怎么按层收集？（3）只想要每层的最后一个节点值（右视图）？分别怎么改。

## A
1. **自底向上**：遍历不变，最后 `res.reverse()`（LC 107）。想在每层追加时就放到最前，可以用 `collections.deque` 的 `appendleft`，每步 `O(1)`；对列表做 `insert(0, x)` 是 `O(n)`，层数多时会拖慢。
2. **DFS 写法**：`dfs(node, depth)`，`depth == len(res)` 时新建一层，再 `res[depth].append(node.val)`；先左后右，这样每层内部就是从左到右，最后反转奇数层。代价是递归深度等于树高，单链树 2000 层会超过 Python 默认递归上限 1000，需要显式栈。
3. **右视图**：每层只取 `level[-1].val`（LC 199），代码就是在 BFS 里把「收集整层」换成「取最后一个」。

```python
def right_side(root: TreeNode | None) -> list[int]:
    out: list[int] = []
    level = [root] if root else []
    while level:
        out.append(level[-1].val)
        level = [c for n in level for c in (n.left, n.right) if c]
    return out
```

**Python 提醒**：`vals[::-1]` 会新建一个列表；只想遍历反向顺序时用 `reversed(vals)`，它是迭代器，不拷贝。`[[]] * k` 得到的是 `k` 个指向同一个列表的引用，要建 `k` 个独立列表必须写 `[[] for _ in range(k)]`。
