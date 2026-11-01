---
slug: split-array-largest-sum
---
## Q
**LC 410 分割数组的最大值**｜Hard

给定非负整数数组 `nums` 和整数 `k`，把数组分成 `k` 个**非空的连续子数组**，使这 `k` 个子数组各自和的最大值**最小**，返回这个最小值。`1 <= nums.length <= 1000`，`0 <= nums[i] <= 10^6`，`1 <= k <= min(50, nums.length)`。例：`nums = [7,2,5,10,8]`, `k = 2` → `18`（分成 `[7,2,5]` 和 `[10,8]`）；`nums = [1,2,3,4,5]`, `k = 2` → `9`；`nums = [1,4,4]`, `k = 3` → `4`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 二分答案（binary search on the answer）+ 贪心判定："最大值最小"。

**一句话。** 二分"每段和的上限 `cap`"，贪心地从左到右尽量往一段里装，算出最少要分几段，段数 `<= k` 就说明 `cap` 够用。

**识别。** 「最大值的最小化」「连续子数组分段」= 二分答案：`cap` 越大，需要的段数越少（单调）；答案范围 `[max(nums), sum(nums)]`，`sum` 最大约 `10^9`，二分约 `30` 轮，每轮 `O(n)`。`n <= 1000`、`k <= 50` 也允许 `O(k n^2)` 的 DP，见拓展。

**推导。** 暴力：枚举所有切法，`C(n-1, k-1)` 种，指数级。换个问法：给定上限 `cap`，最少需要几段？贪心——当前段装得下就装，装不下才另起一段——这就是最少段数（每段尽量长不会更差）。"段数随 `cap` 增大单调不增"，所以能让段数 `<= k` 的最小 `cap` 可以二分。`cap` 至少是 `max(nums)`，否则最大的元素无处安放。

```python
def split_array(nums: list[int], k: int) -> int:
    def groups_needed(cap: int) -> int:
        # 每段和不超过 cap 时，贪心最少要几段：装不下才另起一段
        cnt, cur = 1, 0
        for x in nums:
            if cur + x > cap:
                cnt += 1
                cur = 0
            cur += x
        return cnt

    lo, hi = max(nums), sum(nums)  # 上限至少是最大元素；hi = sum 时只需一段
    while lo < hi:
        mid = (lo + hi) // 2
        if groups_needed(mid) <= k:  # mid 够用（段数不超过 k；少于 k 段时可以再拆，最大值不会变大）
            hi = mid
        else:
            lo = mid + 1
    return lo
```

运行：`([7,2,5,10,8], 2)` → `18`；`([1,2,3,4,5], 2)` → `9`；`([1,4,4], 3)` → `4`；`([0,0,0], 2)` → `0`；`([5], 1)` → `5`。

**复杂度。** 时间 `O(n log(sum(nums)))`，空间 `O(1)`。

**拓展优化。**
- 面试官可能追问不用二分的做法：区间 DP 的前缀和版本，`dp[j][i]` 表示前 `i` 个数分成 `j` 段的最小"最大段和"，时间 `O(k n^2)`，`n = 1000`、`k = 50` 时偏慢，是二分的退路而非首选：

```python
from itertools import accumulate
from math import inf


def split_array_dp(nums: list[int], k: int) -> int:
    n = len(nums)
    pre = [0] + list(accumulate(nums))  # pre[i]：前 i 个数的和
    dp = [[inf] * (n + 1) for _ in range(k + 1)]  # dp[j][i]：前 i 个数分成 j 段的最小"最大段和"
    dp[0][0] = 0
    for j in range(1, k + 1):
        for i in range(j, n + 1):
            for p in range(j - 1, i):  # 最后一段是 nums[p:i]
                dp[j][i] = min(dp[j][i], max(dp[j - 1][p], pre[i] - pre[p]))
    return dp[k][n]
```

**易错点。**
- 下界取 `0` 或 `1`：贪心里一个比 `cap` 还大的元素会被当作"自己一段"，段数被低估。`[1,4,4]`, `k = 3` 会返回 `1`，正确是 `4`。
- 判定写成 `groups_needed(mid) == k`：`[1,4,4]`, `k = 3` 返回 `9`，正确是 `4`；段数少于 `k` 总能继续拆、最大值不变大，所以条件是 `<= k`。
- 边界混写：`while lo <= hi` 配 `hi = mid - 1` 却返回 `hi`，示例 1 得到 `17`，正确是 `18`；本卡用 `lo < hi`、`hi = mid`、`lo = mid + 1`，返回 `lo`。

**同模式。** LC 1011 在 D 天内送达包裹的能力、LC 875 爱吃香蕉的珂珂、LC 1482 制作 m 束花所需的最少天数、LC 774 最小化去加油站的最大距离。
