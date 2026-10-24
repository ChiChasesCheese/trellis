---
id: tlc-minimum-moves-to-pick-k-ones-2-code
node: b.minimum-moves-to-pick-k-ones
type: qa
step: 2
---
## Q
**LC 3086 拾起 K 个 1 需要的最少行动次数**｜写出 Python 实现

二进制数组 `nums`（长度 `2..10^5`）、正整数 `k`（`1..10^5`）、`maxChanges`（`0..10^5`），保证 `maxChanges + sum(nums) >= k`。Alice 选定位置后，每步可以把一个 `0` 造成 `1`（最多 `maxChanges` 次），或交换相邻的 `1`、`0`；`1` 被换到 Alice 脚下就拾起。返回拾起恰好 `k` 个 `1` 的最少行动次数。要求 `O(n)`。

## A
**思路。** 先算 `c`：连续 `1` 的最大长度，封顶 `3` 和 `k`；它们的拾取代价是 `0, 1, 1`。若造 `1` 的次数够补满其余，答案 `max(c - 1, 0) + 2 * (k - c)`。否则造 `1` 全用，再从已有 `1` 的位置数组里取长度 `need = k - maxChanges` 的窗口，站在中位数，距离和用前缀和算，取最小再加 `2 * maxChanges`。

```python
from itertools import accumulate, groupby


def minimum_moves(nums: list[int], k: int, max_changes: int) -> int:
    # c：Alice 站在某个 1 上，不用"造 1"就能拿到的相邻 1 的个数（0、1、1 步），最多 3 个
    longest_run = max((len(list(g)) for v, g in groupby(nums) if v), default=0)
    c = min(longest_run, 3, k)
    if max_changes >= k - c:                   # 剩下的 k-c 个全靠"造 1 再换过来"，每个 2 步
        return max(c - 1, 0) + 2 * (k - c)

    # 否则造 1 的次数全部用完，还得把 need 个已有的 1 挪到 Alice 身边
    need = k - max_changes
    pos = [i for i, x in enumerate(nums) if x]
    pre = list(accumulate(pos, initial=0))     # pre[i] = pos[0] + ... + pos[i-1]

    def cost(l: int) -> int:                   # 窗口 pos[l : l+need] 全部挪向中位数的总步数
        r, m = l + need, l + need // 2
        left = pos[m] * (m - l) - (pre[m] - pre[l])
        right = (pre[r] - pre[m + 1]) - pos[m] * (r - m - 1)
        return left + right

    return 2 * max_changes + min(map(cost, range(len(pos) - need + 1)))
```

**运行。** `[1,1,0,0,0,1,1,0,0,1], 3, 1` → `3`；`[0,0,0,0], 2, 3` → `4`；`[1,0,1,0,1], 3, 0` → `4`；`[1,1,1], 3, 0` → `2`；`[0,0], 1, 1` → `2`；`[1,0,1], 2, 1` → `2`。

**复杂度。** 时间 `O(n)`：`groupby` 与建位置数组各一遍，窗口数 `m - need + 1` 个，每个 `O(1)`；空间 `O(m)`，`m = sum(nums)`。

**写法要点。** `groupby(nums)` 按相邻相等分组，`if v` 只留 `1` 的组，`len(list(g))` 是组长；`max(..., default=0)` 处理没有 `1` 的数组；`accumulate(pos, initial=0)` 得到长度 `m + 1` 的前缀和，区间和写成 `pre[r] - pre[l]` 不用特判边界；嵌套函数 `cost` 把窗口公式命名，`min(map(cost, range(...)))` 替代手写的 `best = inf` 擂台。
