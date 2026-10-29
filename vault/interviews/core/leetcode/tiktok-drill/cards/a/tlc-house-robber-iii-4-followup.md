---
id: tlc-house-robber-iii-4-followup
node: a.house-robber-iii
type: qa
step: 4
---
## Q
**LC 337 打家劫舍 III**｜追问

面试官接着问：（1）要返回具体偷了哪些房子，而不只是金额？（2）树换成多叉树？（3）能不能用递归写，写出来最短的版本？（4）房子围成环（LC 213）怎么办？

## A
1. **还原方案**：求出 `take`、`skip` 后自顶向下走一遍。根的决策是 `take[root] > skip[root]` 就偷；偷了某节点，它的孩子都走「不偷」分支；不偷某节点，每个孩子各自比较 `take` 与 `skip`，更大的那个决定它偷不偷。用一个栈带着 `(节点, 父亲是否被偷)` 迭代即可。
2. **多叉树**：状态不变，`take[v] = v.val + Σ skip[c]`，`skip[v] = Σ max(take[c], skip[c])`，对 `children` 求和；顺序仍是先序入列、倒序处理。
3. **递归版**：返回 `(偷, 不偷)` 二元组，五行以内：

```python
def rob_rec(root: TreeNode | None) -> int:
    def go(v: TreeNode | None) -> tuple[int, int]:
        if v is None:
            return 0, 0
        lt, ls = go(v.left)
        rt, rs = go(v.right)
        return v.val + ls + rs, max(lt, ls) + max(rt, rs)

    return max(go(root))
```

   和迭代版结果一致，但在 `10^4` 的斜链上默认递归上限（`1000`）会抛 `RecursionError`，面试里要说明这一点，必要时改迭代或调大 `sys.setrecursionlimit`。
4. **环形（LC 213）**：断开首尾，分别对「去掉首」「去掉尾」两条链做线性打家劫舍，取较大值。

**Python 提醒**：返回元组再 `max(go(root))` 是在「两个状态里取较大」，别写成 `max(go(root)[0], ...)` 漏掉另一个状态；`sys.setrecursionlimit` 调大只改解释器的计数，栈太深仍可能让进程崩溃，不如迭代稳。
