---
id: tlc-count-complete-subarrays-in-an-array-4-followup
node: b.count-complete-subarrays-in-an-array
type: qa
step: 4
---
## Q
**LC 2799 统计完全子数组的数目**｜追问

面试官接着问：（1）改成「恰好有 `k` 种不同元素」的子数组数？（2）如果 `n` 到 `10^5`，`O(n^2)` 的写法不行，现有写法还成立吗？（3）怎样只求最短的完全子数组？

## A
1. **恰好 `k` 种（LC 992）。** 恰好 = 至多 `k` 种 − 至多 `k - 1` 种。「至多 `k` 种」的子数组数用滑动窗口一遍得到：右端每进一步，窗口种类数超过 `k` 就缩左，贡献 `right - left + 1`。

```python
from collections import Counter


def at_most_k_distinct(nums: list[int], k: int) -> int:
    cnt: Counter[int] = Counter()
    left = ans = 0
    for right, x in enumerate(nums):
        cnt[x] += 1
        while len(cnt) > k:                # 种类超限：缩左直到合法
            cnt[nums[left]] -= 1
            if cnt[nums[left]] == 0:
                del cnt[nums[left]]
            left += 1
        ans += right - left + 1            # 以 right 结尾、起点在 [left, right] 的子数组都合法
    return ans
```

2. **`n = 10^5`。** 现有解法本来就是 `O(n)`，不依赖 `n <= 1000`；那个约束只是让 `O(n^2)` 暴力也能过。
3. **最短完全子数组。** 同一个循环，每次凑齐时用 `right - left` 更新最小长度，不再累加个数。

**Python 提醒**：`Counter` 的值减到 `0` 键不会消失，`len(cnt)` 仍然把它算进去；需要「当前种类数」时必须手动 `del`，或者改用 `+cnt`（去掉非正数项）这类会新建对象的写法，窗口里每步都这样做会变成 `O(n·k)`。
