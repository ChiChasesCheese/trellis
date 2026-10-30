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
**思路。** 递归 DFS，`dfs(node, prefix)` 返回以子树内节点结尾的路径条数。进入节点：算出 `cur`，先用 `seen[cur - target]` 得到以它结尾的路径数，再登记 `seen[cur]`，递归所有孩子，返回前撤销登记。

```python
from collections import Counter


def path_sum(root: Node | None, target: int) -> int:
    """统计自上而下的路径条数（起点终点任意，只能往孩子方向走），路径和等于 target。"""
    seen = Counter({0: 1})                        # 前缀和 -> 当前根到当前节点这条链上出现的次数；空前缀 0 出现 1 次

    def dfs(node: Node | None, prefix: int) -> int:   # prefix：根到 node 的父亲的前缀和
        if node is None:
            return 0
        cur = prefix + node.val                   # 根到 node 的前缀和
        ans = seen[cur - target]                  # 以 node 结尾、和为 target 的路径数（先查询）
        seen[cur] += 1                            # 进入：再登记 cur，供子孙节点配对
        for child in node.children:
            ans += dfs(child, cur)
        seen[cur] -= 1                            # 离开：撤销（回溯），兄弟分支看不到它
        return ans

    return dfs(root, 0)
```

运行：`10 -> [5 -> [3 -> [3, -2], 2 -> [1]], -3 -> [11]]`、`target = 8` → `3`；`Node(0, [Node(0), Node(0)])`、`target = 0` → `5`；`None` → `0`；`Node(5)`：`target = 5` → `1`，`target = 6` → `0`，`target = 0` → `0`；`10^5` 层的全 `1` 链、`target = 3` 在默认递归上限下抛 `RecursionError`，调高上限后 → `99998`。

**复杂度。** 时间 `O(n)`，空间 `O(h)`（递归栈与哈希表，最坏链状树 `O(n)`；`10^5` 层会触到默认递归上限）。

**写法要点。**
- `Counter` 对不存在的键返回 `0` 且不插入，`seen[cur - target]` 可以直接读，不用 `.get(key, 0)`；`seen[prefix] -= 1` 让计数归零但保留键，不影响正确性。
- 回溯就是一对语句：`seen[cur] += 1` 在递归孩子之前，`seen[cur] -= 1` 在返回之前，函数返回处天然是「所有孩子都处理完」的时刻。
- `prefix` 作为参数向下传，每层自己算 `cur`，不需要在返回时再减回去。
- 先查询再登记：查询时 `seen` 里只有真正的祖先前缀（加上空前缀），不包含自己，所以不会把「空路径」当成答案。
