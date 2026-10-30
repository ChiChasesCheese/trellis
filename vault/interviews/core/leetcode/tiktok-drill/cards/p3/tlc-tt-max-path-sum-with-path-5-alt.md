---
id: tlc-tt-max-path-sum-with-path-5-alt
node: p3.tt-max-path-sum-with-path
type: qa
step: 5
---
## Q
**二叉树最大路径和（并输出路径）**｜另一种解法

面试里最常见的写法是递归的后序遍历。同样求最大路径和并还原路径，递归写法怎么写？它有什么限制，什么时候选它？

## A
**递归 DFS。** 递归函数返回「从该节点向下的单链最大和」，在函数里更新全局最优和拐点，同时记录每个节点的最优单链走向。

```python
def max_path_sum_recursive(root: TreeNode) -> tuple[int, list[TreeNode]]:
    gains: dict[TreeNode, int] = {}                # gains[v]：从 v 向下的单链最大和
    down: dict[TreeNode, TreeNode | None] = {}     # down[v]：最优单链在 v 之后走向哪个孩子
    best, peak = root.val, root

    def dfs(node: TreeNode | None) -> int:
        nonlocal best, peak
        if node is None:
            return 0
        left, right = max(dfs(node.left), 0), max(dfs(node.right), 0)    # 负贡献的分支不要
        down[node] = node.left if left and left >= right else node.right if right else None
        gains[node] = node.val + max(left, right)
        if node.val + left + right > best:
            best, peak = node.val + left + right, node
        return gains[node]

    dfs(root)

    def arm(child: TreeNode | None) -> list[TreeNode]:
        chain = []
        while child:
            chain.append(child)
            child = down[child]
        return chain

    left_arm = arm(peak.left) if peak.left and gains[peak.left] > 0 else []
    right_arm = arm(peak.right) if peak.right and gains[peak.right] > 0 else []
    return best, left_arm[::-1] + [peak] + right_arm
```

`-10 -> (9, 20 -> (15, 7))` → `(42, [15, 20, 7])`，与显式栈的版本对所有随机小树结果一致。时间 `O(n)`，空间 `O(n)`。

**限制。** 递归深度等于树高：`3 * 10^4` 层的链会 `RecursionError`（默认上限 `1000`）。要么 `sys.setrecursionlimit` 加大并且在一个栈更大的线程里运行（`threading.stack_size`），要么改用显式栈。

**怎么选。**
- 树大致平衡（高度 `O(log n)`）：递归版最短最易读，面试里先写它。
- 可能退化成链，或者面试官追问「树很深怎么办」：换成显式栈的版本，逻辑相同。
- 只要数值、不要路径：递归版去掉 `down` 和 `arm`，十行以内。
