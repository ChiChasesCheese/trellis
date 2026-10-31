---
id: tlc-path-sum-iii-4-followup
node: p2.path-sum-iii
type: qa
step: 4
---
## Q
**LC 437 路径总和 III**｜追问

面试官接着问：（1）不只要条数，要把所有路径列出来？（2）如果树有一百万个结点、可能退化成链，怎么办？（3）路径允许在任意两点之间（可以先上后下）呢？

## A
1. **列出路径**：哈希表改成 `前缀和 → 该前缀对应的深度下标列表`，同时维护当前链 `chain: list[int]`；命中时对每个下标 `i` 输出 `chain[i + 1 :]`（加上当前结点）。路径数本身可以是 `O(n^2)`，输出就是下界。
2. **百万结点 / 链**：递归会爆栈，改成显式栈（或把递归限制调高并说明风险）；栈深 `O(h)`，链上是 `O(n)`，无法再降，因为必须记住整条链的前缀和。显式栈里同一个结点压两次，第二次是「离开」标记，用来撤销前缀和：

```python
def path_sum_stack(root: TreeNode | None, target_sum: int) -> int:
    count = 0
    prefix: Counter[int] = Counter({0: 1})   # 当前根到结点链上：前缀和 -> 出现次数
    stack: list[tuple[TreeNode | None, int, bool]] = [(root, 0, False)]
    while stack:                             # 迭代 DFS：进入时加入前缀和，离开时撤销
        node, total, leaving = stack.pop()
        if node is None:
            continue
        if leaving:
            prefix[total] -= 1               # 回溯：别的分支看不到这条链
            continue
        total += node.val                    # 根到 node 的和
        count += prefix[total - target_sum]  # 有多少个祖先前缀和恰好差 target_sum
        prefix[total] += 1
        stack.append((node, total, True))
        stack.append((node.right, total, False))
        stack.append((node.left, total, False))
    return count
```

3. **任意两点间路径**：不再是链上的片段，前缀和失效。要用后序 DFS，在每个结点合并左、右子树「向下的单链和」。数「和等于 `target` 的任意路径条数」没有 `O(n)` 的好办法，常见做法是对每个结点做小到大合并（启发式合并）的哈希表。

**Python 提醒**：`Counter` 的 `c[k] -= 1` 减到 `0` 后键**仍留在**字典里；这里只做查询所以无妨，但若用 `len(prefix)` 或遍历，要自己 `del`。另外 `defaultdict(int)` 读缺失键会**插入**键，`Counter` 不会——读多写少时更省内存。
