---
id: tlc-minimum-moves-to-pick-k-ones-0-whole
node: b.minimum-moves-to-pick-k-ones
type: qa
---
## Q
**LC 3086 拾起 K 个 1 需要的最少行动次数**｜Hard · LC TikTok 热度 62/100

给下标从 0 开始的二进制数组 `nums`（长度 `n`）、正整数 `k` 和非负整数 `maxChanges`。Alice 先任选一个站立下标 `aliceIndex`；若该位是 `1`，她立即拾起它（该位变 `0`，不算行动）。之后每次行动恰好做下面之一：（1）选一个 `j != aliceIndex` 且 `nums[j] == 0`，把它置为 `1`，这个动作最多做 `maxChanges` 次；（2）选相邻下标 `x, y`，`nums[x] == 1, nums[y] == 0`，交换二者；若 `y == aliceIndex`，Alice 拾起这个 `1`（该位变 `0`）。返回恰好拾起 `k` 个 `1` 的最少行动次数。

约束：`2 <= n <= 10^5`，`0 <= nums[i] <= 1`，`1 <= k <= 10^5`，`0 <= maxChanges <= 10^5`，`maxChanges + sum(nums) >= k`。例：`nums = [1,1,0,0,0,1,1,0,0,1], k = 3, maxChanges = 1` → `3`；`nums = [0,0,0,0], k = 2, maxChanges = 3` → `4`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** Alice 站定后，拾起一个 `1` 的代价只有几档：脚下 `0` 步、紧挨着的 `1` 需要 `1` 步、「造一个 `1` 再换过来」需要 `2` 步、距离为 `d` 的已有 `1` 需要 `d` 步。先吃掉最便宜的相邻 `1`（至多 3 个），再用 `maxChanges` 次造 `1`；若造 `1` 的次数不够，剩下的 `need = k - maxChanges` 个必须真的从已有的 `1` 里挪过来，取 `1` 的位置数组上长度为 `need` 的窗口、站在中位数，用前缀和 `O(1)` 求总距离，取最小。`O(n)`。

**识别。** 「相邻交换，代价按步数」把问题变成「`k` 个点聚到同一位置，总距离最小」，最优聚集点是中位数（median），这是 LC 462、LC 1703 的同一套路。「`maxChanges` 次免费造 `1`」给出一档固定代价 `2`，要和「移动已有的 `1`」按代价比较，便宜的先用。`n = 10^5` 要求窗口 + 前缀和，每个窗口 `O(1)`。

**推导。** 暴力：枚举 Alice 的位置 `i`，已有的每个 `1` 代价是 `|j - i|`，每次造 `1` 代价是 `2`，取最便宜的 `k` 个，`O(n · (m + maxChanges) · log k)`（`m` 是 `1` 的个数）。浪费：代价档位很少。距离 `>= 2` 的已有 `1` 至少和造 `1` 一样贵，只有脚下和紧邻的 `1`（最多 3 个，即连续 `1` 的长度封顶 3）比造 `1` 便宜。于是分两支：（1）`maxChanges >= k - c`（`c` 是能便宜拿到的个数）：答案 `max(c - 1, 0) + 2 * (k - c)`；（2）否则造 `1` 全部用掉，再从已有的 `1` 里选 `need` 个距离和最小的。后者在位置数组里必然连续（漏掉中间的 `1` 换进来不会更差），站中位数最省。

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

**运行。** 例 1 → `3`；例 2 → `4`；`[1,0,1,0,1], k=3, maxChanges=0` → `4`；`[1,1,1], k=3, maxChanges=0` → `2`；`[0,0], k=1, maxChanges=1` → `2`；`[1,0,1], k=2, maxChanges=1` → `2`。

**复杂度。** 时间 `O(n)`：`groupby` 一遍、建位置数组一遍、窗口每个 `O(1)`；空间 `O(m)`（位置数组和前缀和）。

**易错点。**
- `c` 必须是**连续** `1` 的长度（封顶 3），不是「三格内有几个 `1`」：`[1,0,1], k=2, maxChanges=1` 若把 `c` 当成 `2`，会得到 `1` 步，正确是 `2`。
- 忽略 `maxChanges`、一律用窗口：例 1 会得到 `4`，正确是 `3`。造 `1` 不够时才走窗口，且造 `1` 要用满。
- `c` 要对 `k` 取最小，`c - 1` 要对 `0` 取最大：`k = 1` 时答案是 `0`，没有 `1` 且全靠造时是 `2k`。

**追问。**
- 同时要站立位置：记录最优窗口的中位数下标 `pos[m]`。
- 造 `1` 的代价改成别的数 `w`：每档比较随之变化，直接用「枚举站立位置，把已有 `1` 的距离和各次造 `1` 的新代价放在一起取最便宜的 `k` 个」的写法最稳，只是时间变成平方级。
- 同一数组查询很多个 `k`：`pos`、`pre` 只建一次，每次查询只重跑窗口。

**同模式。** LC 462 最少移动次数使数组元素相等 II、LC 1703 得到连续 K 个 1 的最少相邻交换次数、LC 296 最佳的碰头地点、LC 2448 使数组相等的最小开销。
