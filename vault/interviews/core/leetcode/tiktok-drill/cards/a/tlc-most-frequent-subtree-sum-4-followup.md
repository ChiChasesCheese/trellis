---
id: tlc-most-frequent-subtree-sum-4-followup
node: a.most-frequent-subtree-sum
type: qa
step: 4
---
## Q
**LC 508 出现次数最多的子树元素和**｜追问

面试官接着问：（1）只要一个众数，且要最小的那个？（2）树换成多叉树？（3）节点太多，`total` 字典占内存太大怎么办？

## A
1. **最小的众数**：`top = max(freq.values())` 后，`min(s for s, c in freq.items() if c == top)`；若同时要返回次数，用 `max(freq.items(), key=lambda kv: (kv[1], -kv[0]))`，先比次数、次数相同取和更小的。
2. **多叉树**：先序栈里把 `children` 全部压栈；倒序处理时 `s = node.val + sum(total[c] for c in node.children)`。其余计数逻辑完全不变。
3. **省内存**：孩子的和只被父亲读一次，父亲算完就可以 `del total[child]`，字典里同时只保留「已算完、父亲还没处理」的节点；对链状树 `total` 的大小接近 `O(1)`，对满二叉树仍是 `O(n)` 量级。要彻底 `O(h)`，用递归版（返回子树和），代价是递归深度。

递归版只有几行，适合树深有保证的场合：

```python
def frequent_tree_sum_rec(root: TreeNode | None) -> list[int]:
    freq: Counter[int] = Counter()

    def go(v: TreeNode | None) -> int:
        if v is None:
            return 0
        s = v.val + go(v.left) + go(v.right)
        freq[s] += 1
        return s

    go(root)
    top = max(freq.values(), default=0)
    return [s for s, c in freq.items() if c == top]
```

**Python 提醒**：`max(freq.values())` 在空 `Counter` 上抛 `ValueError`；节点数至少为 `1` 时不会触发，但处理空树时要写 `default=0`，并且先判断 `root is None`。
