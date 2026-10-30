---
id: tlc-tt-path-sum-n-ary-prefix-sum-2-code
node: p3.tt-path-sum-n-ary-prefix-sum
type: qa
step: 2
---
## Q
**N 叉树路径和（前缀和加哈希）**｜写出 Python 实现

节点 `Node` 有 `val: int` 和 `children: list[Node]`。写 `path_sum(root, target)`：统计自上而下（只往孩子方向走、起点终点任意）的路径条数，使节点值之和等于 `target`。`0 <= n <= 10^5`，`-10^9 <= val, target <= 10^9`，树可能退化成 `10^5` 层的链，要求 `O(n)`。

## A
**思路。** 栈里放 `(节点, 父亲的前缀和)`，节点为 `None` 的项是「退出标记」。进入节点：算出 `cur`，先用 `seen[cur - target]` 累加答案，再登记 `seen[cur]`，并压入退出标记和所有孩子；弹出退出标记时撤销登记。

```python
from collections import Counter


def path_sum(root: Node | None, target: int) -> int:
    """统计自上而下的路径条数（起点终点任意，只能往孩子方向走），路径和等于 target。"""
    if root is None:
        return 0
    seen = Counter({0: 1})                        # 前缀和 -> 当前根到当前节点这条链上出现的次数；空前缀 0 出现 1 次
    ans = 0
    stack: list[tuple[Node | None, int]] = [(root, 0)]    # (节点, 父亲的前缀和)；node 为 None 表示「退出」标记
    while stack:
        node, prefix = stack.pop()
        if node is None:
            seen[prefix] -= 1                     # 离开某个节点：撤销它的前缀和（回溯）
            continue
        cur = prefix + node.val                   # 根到 node 的前缀和
        ans += seen[cur - target]                 # 以 node 结尾、和为 target 的路径数
        seen[cur] += 1
        stack.append((None, cur))                 # 先压退出标记，它会在所有孩子处理完之后弹出
        stack.extend((child, cur) for child in node.children)
    return ans
```

运行：`10 -> [5 -> [3 -> [3, -2], 2 -> [1]], -3 -> [11]]`、`target = 8` → `3`；`Node(0, [Node(0), Node(0)])`、`target = 0` → `5`；`None` → `0`；`Node(5)`：`target = 5` → `1`，`target = 6` → `0`，`target = 0` → `0`；`10^5` 层的全 `1` 链、`target = 3` → `99998`。

**复杂度。** 时间 `O(n)`，空间 `O(h)`（最坏链状树 `O(n)`）。

**写法要点。**
- `Counter` 对不存在的键返回 `0` 且不插入，`seen[cur - target]` 可以直接读，不用 `.get(key, 0)`；`seen[prefix] -= 1` 让计数归零但保留键，不影响正确性。
- 「退出标记」：栈里 `(None, cur)` 在所有孩子之后才弹出（后进先出），恰好模拟递归函数返回时的撤销，迭代代码不再需要调用栈。
- `stack.extend(生成器)`：一次把所有孩子压栈，孩子顺序倒过来被处理，不影响计数结果。
- 先查询再登记：查询时 `seen` 里只有真正的祖先前缀（加上空前缀），不包含自己，所以不会把「空路径」当成答案。
