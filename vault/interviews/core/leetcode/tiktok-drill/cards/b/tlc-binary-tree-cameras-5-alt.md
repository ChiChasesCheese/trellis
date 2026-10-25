---
id: tlc-binary-tree-cameras-5-alt
node: b.binary-tree-cameras
type: qa
step: 5
---
## Q
**LC 968 监控二叉树**｜另一种解法

不依赖「推迟装摄像头」的贪心，还有什么写法能解 LC 968（节点数 `<= 1000`，摄像头监视父节点、自己、直接子节点）？它的复杂度是多少，什么时候该选它而不是贪心？

## A
**三状态树形 DP。** 对每个节点 `v` 求三个值，都表示「`v` 子树内所有节点（除 `v` 本身在 `c` 状态外）都被监控」时的最少摄像头数：
- `a`：`v` 上装摄像头。孩子处于任意状态都被覆盖：`a = 1 + Σ min(孩子的 a, b, c)`。
- `b`：`v` 不装，但被某个孩子的摄像头覆盖。每个孩子要自己负责（`min(a, b)`），并且至少一个孩子取 `a`。
- `c`：`v` 不装，也不被孩子覆盖，等父亲来覆盖：孩子必须都被它们自己的孩子覆盖，`c = Σ 孩子的 b`。

空节点的三元组是 `(inf, 0, 0)`：不能在空节点装摄像头，其余两种状态代价为零。答案是 `min(a, b)` 取根（根没有父亲，不能用 `c`）。

```python
from math import inf


def min_camera_dp(root: TreeNode | None) -> int:
    order: list[TreeNode] = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    # f[v] = (a, b, c)：a 在 v 装摄像头；b 不装，但 v 被某个孩子的摄像头覆盖；c 不装，v 等父亲覆盖
    f: dict[TreeNode | None, tuple[float, float, float]] = {None: (inf, 0, 0)}
    for node in reversed(order):
        kids = [f[node.left], f[node.right]]
        a = 1 + sum(min(k) for k in kids)                    # 摄像头覆盖孩子：孩子任意状态都行
        best = [min(k[0], k[1]) for k in kids]               # 孩子自己负责（装摄像头或被其孩子覆盖）
        b = min((k[0] + sum(best) - best[i] for i, k in enumerate(kids) if k[0] < inf), default=inf)
        c = sum(k[1] for k in kids)                          # 孩子都得靠自己的孩子被覆盖
        f[node] = (a, b, c)
    a, b, _ = f[root]
    return int(min(a, b))
```

运行：`[0,0,null,0,0]` → `1`；`[0,0,null,0,null,0,null,null,0]` → `2`；`[0]` → `1`；`1000` 节点的左斜链 → `334`，与贪心一致。

**复杂度。** 时间 `O(n)`；空间 `O(n)`。

**怎么选。**
- 每个摄像头代价相同、只要答案：贪心，代码更短、状态更少。
- 摄像头成本不同、覆盖规则变化、或者要在面试里讲清为什么最优：三状态 DP，每个状态的含义可以逐条解释；成本不同只需把 `a` 里的 `1` 换成该节点成本。
- 两者都是线性的，面试里可以先写贪心，再用 DP 验证一两个小例子。
