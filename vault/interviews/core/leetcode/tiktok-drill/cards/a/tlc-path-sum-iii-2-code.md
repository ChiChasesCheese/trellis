---
id: tlc-path-sum-iii-2-code
node: a.path-sum-iii
type: qa
step: 2
---
## Q
**LC 437 路径总和 III**｜写出 Python 实现

二叉树（结点数 `0..1000`，值在 `[-10^9, 10^9]`，可为负）和整数 `targetSum`（`-1000..1000`）。数出结点值之和为 `targetSum` 的向下路径条数，路径可从任意结点开始、在任意结点结束。要求 `O(n)`。

## A
**思路。** DFS 时维护一张「根到当前结点这条链上的前缀和 → 次数」的表。到结点 `b` 时，答案加上表里 `前缀(b) - targetSum` 的次数，再把 `前缀(b)` 记入表；离开 `b` 时撤销。表一开始放 `{0: 1}`，代表空前缀。用显式栈，并用「是否离开」标记实现回溯。

```python
def path_sum(root: TreeNode | None, target_sum: int) -> int:
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

运行：`root=[10,5,-3,3,2,null,11,3,-2,null,1], targetSum=8` → `3`，`root=[5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum=22` → `3`，`root=[], targetSum=0` → `0`，`root=[1,-1,1,-1,1], targetSum=0` → `2`，`1000 个结点的单链，值全 0，targetSum=0` → `500500`。

**复杂度。** 时间 `O(n)`：每个结点进栈、出栈各一次，字典操作 `O(1)`；空间 `O(n)`：栈深 `O(h)`，`Counter` 里撤销后键仍保留，最坏有 `n` 个不同的前缀和。

**写法要点。** `Counter` 对不存在的键返回 `0` 且**不插入**，所以 `prefix[total - target_sum]` 可以直接读；`Counter({0: 1})` 一步完成播种；栈里放 `(结点, 前缀和, 是否离开)` 三元组，同一个结点压两次（进入 / 离开），这是把递归的「进入 + 回溯」改成迭代的通用手法；先压右再压左，使左子树先处理。
