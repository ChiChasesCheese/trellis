---
id: tlc-tt-max-path-sum-with-path-5-alt
node: p3.tt-max-path-sum-with-path
type: qa
step: 5
---
## Q
**二叉树最大路径和（并输出路径）**｜另一种解法

主解是后序递归。树可能退化成 `3 * 10^4` 层的链，递归会超过 CPython 默认上限，面试官追问「树很深怎么办」时，同样求最大路径和并还原路径，显式栈怎么写？什么时候选它？

## A
**显式栈。** 先序（根、右、左）把节点记进 `order`，倒着处理就是孩子先于父亲，用同样的 `gain` / `down` 逻辑算完，再沿 `down` 展开两条臂。

```python
def max_path_sum_stack(root: TreeNode) -> tuple[int, list[TreeNode]]:
    order: list[TreeNode] = []
    stack = [root]
    while stack:                                   # 先序（根、右、左）入表，倒过来就是「孩子先于父亲」
        node = stack.pop()
        order.append(node)
        stack.extend(child for child in (node.left, node.right) if child)
    gain: dict[TreeNode, int] = {}                 # gain[v]：从 v 向下的单链最大和
    down: dict[TreeNode, TreeNode | None] = {}     # down[v]：最优单链在 v 之后走向哪个孩子
    best, peak = root.val, root
    for node in reversed(order):                   # 孩子先于父亲
        left = gain[node.left] if node.left and gain[node.left] > 0 else 0    # 负贡献的分支直接不要
        right = gain[node.right] if node.right and gain[node.right] > 0 else 0
        down[node] = node.left if left and left >= right else node.right if right else None
        gain[node] = node.val + max(left, right)
        if node.val + left + right > best:
            best, peak = node.val + left + right, node

    def arm(child: TreeNode | None) -> list[TreeNode]:
        chain = []
        while child:
            chain.append(child)
            child = down[child]
        return chain

    left_arm = arm(peak.left) if peak.left and gain[peak.left] > 0 else []
    right_arm = arm(peak.right) if peak.right and gain[peak.right] > 0 else []
    return best, left_arm[::-1] + [peak] + right_arm
```

`-10 -> (9, 20 -> (15, 7))` → `(42, [15, 20, 7])`，与递归版的结果一致；`3 * 10^4` 层的左链在默认递归上限下也能得到 `(30000, 路径长度 30000)`。时间 `O(n)`，空间 `O(n)`。

**限制。** 比递归版长，要自己维护处理顺序；逻辑相同，只是把调用栈换成了列表。

**怎么选。**
- 树大致平衡（高度 `O(log n)`）：递归版最短最易读，面试里先写它。
- 可能退化成链，或者面试官追问「树很深怎么办」：换成显式栈，或者 `sys.setrecursionlimit` 调高后继续用递归。
- 只要数值、不要路径：递归版去掉 `down` 和 `arm`，十行以内。
