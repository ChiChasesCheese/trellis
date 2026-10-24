---
id: tlc-minimum-moves-to-pick-k-ones-5-alt
node: b.minimum-moves-to-pick-k-ones
type: qa
step: 5
---
## Q
**LC 3086 拾起 K 个 1 需要的最少行动次数**｜另一种解法

不做 `c` 的分支和中位数窗口，直接按定义怎么写？它的复杂度是多少，什么时候用它而不用 `O(n)` 的解法？

## A
**思路。** 枚举 Alice 的站立位置 `i`。已有的每个 `1` 代价是它到 `i` 的距离，每次造 `1` 的代价是 `2`（最多 `maxChanges` 个）。把这些代价放在一起，取最便宜的 `k` 个求和；对所有 `i` 取最小。

```python
from heapq import nsmallest


def minimum_moves_quadratic(nums: list[int], k: int, max_changes: int) -> int:
    ones = [j for j, x in enumerate(nums) if x]

    def cost_at(i: int) -> int:                  # Alice 站在 i 时，拿满 k 个的最小步数
        # 每个已有的 1 的代价 = 到 i 的距离；每次"造 1"的代价 = 2；从中挑最便宜的 k 个
        return sum(nsmallest(k, [abs(j - i) for j in ones] + [2] * max_changes))

    return min(map(cost_at, range(len(nums))))
```

`[1,1,0,0,0,1,1,0,0,1], 3, 1` → `3`；`[0,0,0,0], 2, 3` → `4`。

**复杂度与取舍。** 时间 `O(n · (m + maxChanges) · log k)`，`n = 10^5` 时超时。优点是几乎不用推导，正确性一眼可见，代价模型改了（比如造 `1` 变成 `w + 1` 步）只改一个常数。**什么时候用哪个：** 需要先给出一个肯定正确的版本、或 `n` 在两千以内，用这个；`n = 10^5` 的正式解答用 `O(n)` 的分支加窗口。写完 `O(n)` 解法后，用它在小数据上对照，是最快的自检方法。
