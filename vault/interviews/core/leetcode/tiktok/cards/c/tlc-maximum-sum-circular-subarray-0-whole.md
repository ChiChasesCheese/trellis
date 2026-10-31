---
id: tlc-maximum-sum-circular-subarray-0-whole
node: c.maximum-sum-circular-subarray
type: qa
---
## Q
**LC 918 环形子数组的最大和**｜Medium · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 3 次 · 最近 2025-04-02（国内 CodeTop）

给定长度为 `n` 的环形整数数组 `nums`（末尾与开头相连，`nums[i]` 的下一个是 `nums[(i + 1) % n]`），返回 `nums` 的非空子数组的最大和。子数组最多包含每个元素一次。`1 <= n <= 3 * 10^4`，`-3 * 10^4 <= nums[i] <= 3 * 10^4`。例：`[1,-2,3,-2]` → `3`；`[5,-3,5]` → `10`（子数组 `[5,5]` 跨越首尾）；`[3,-2,2,-3]` → `3`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 环形最大子数组要么不跨首尾（普通 Kadane），要么跨首尾，跨首尾时等于「总和减去中间一段最小子数组」。

**识别。** 「环形 + 最大连续和」：把环拆成两种情形——最大段在中间，或最大段由首尾两头拼成（此时剩下的中间一段是最小子数组）。两种情形各是一遍 Kadane。

**推导。** 拷贝数组成两倍长再枚举起点，`O(n²)` 或需要单调队列。更简单：跨首尾的段 = 总和 - 不被选中的那段连续区间，要让选中的最大就让不选的最小，所以答案是 `max(最大子数组和, 总和 - 最小子数组和)`。唯一陷阱：数组全是负数时最小子数组就是整个数组，`总和 - 最小 = 0` 对应空子数组，题目要求非空，此时直接返回最大子数组和（最大的那个负数）。

```python
from math import inf


def max_subarray_sum_circular(nums: list[int]) -> int:
    total = 0
    cur_max = cur_min = 0                        # 以当前元素结尾的最大 / 最小子数组和
    best_max, best_min = -inf, inf
    for x in nums:
        total += x
        cur_max = max(cur_max + x, x)            # Kadane：接上前面或从 x 重新开始
        cur_min = min(cur_min + x, x)
        best_max = max(best_max, cur_max)
        best_min = min(best_min, cur_min)
    if best_max < 0:                             # 全是负数：total - best_min 会得到空子数组的 0，不合法
        return best_max
    return max(best_max, total - best_min)       # 不跨首尾 vs 跨首尾（去掉中间最小的一段）
```

运行：`[1,-2,3,-2]` → `3`，`[5,-3,5]` → `10`，`[3,-2,2,-3]` → `3`；`[-3,-2,-3]` → `-2`，`[5]` → `5`，`[0,-1]` → `0`。

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**拓展优化。**
- 不拆情形的统一做法：对前缀和的两倍长数组，用单调队列维护长度不超过 `n` 的窗口内最小前缀和，`O(n)`。

```python
from collections import deque


def max_subarray_sum_circular_deque(nums: list[int]) -> int:
    n = len(nums)
    prefix = [0]
    for i in range(2 * n):
        prefix.append(prefix[-1] + nums[i % n])  # 两倍长的前缀和，覆盖所有跨首尾的段
    best = nums[0]
    window: deque[int] = deque([0])              # 下标队列，对应的前缀和严格递增
    for j in range(1, 2 * n + 1):
        if window[0] < j - n:                    # 子数组长度不能超过 n
            window.popleft()
        best = max(best, prefix[j] - prefix[window[0]])
        while window and prefix[j] <= prefix[window[-1]]:
            window.pop()
        window.append(j)
    return best
```

**易错点。**
- 忘了处理全负数：`[-3,-2,-3]` 会返回 `0`，正确答案是 `-2`。
- 只做普通 Kadane：`[5,-3,5]` 得到 `5`，漏掉跨首尾的 `[5,5]`，正确是 `10`。

**追问。**
- 返回具体区间：Kadane 里记录起点，跨首尾时区间是「最小段之外」的两头。
- 数据是流式的：两个 Kadane 与总和都可以增量更新，每来一个数 `O(1)`。

**同模式。** LC 53 最大子数组和、LC 152 乘积最大子数组、LC 213 打家劫舍 II、LC 862 和至少为 K 的最短子数组、LC 1749 任意子数组和的绝对值的最大值。
