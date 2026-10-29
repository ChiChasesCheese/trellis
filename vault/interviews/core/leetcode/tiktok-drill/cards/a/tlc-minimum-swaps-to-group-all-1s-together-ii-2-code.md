---
id: tlc-minimum-swaps-to-group-all-1s-together-ii-2-code
node: a.minimum-swaps-to-group-all-1s-together-ii
type: qa
step: 2
---
## Q
**LC 2134 最少交换次数来组合所有的 1 II**｜写出 Python 实现

二进制环形数组 `nums`（`1 <= nums.length <= 10^5`，第一个和最后一个元素相邻）。每次交换两个不同位置的值，返回把所有 `1` 聚集在一起（环形意义下连续）的最少交换次数。

## A
**思路。** 设 `k` 为 `1` 的总数，窗口长度就是 `k`。先算起点 `0` 的窗口里 `1` 的个数，之后窗口每右移一格，加入下标 `i % n`、移除下标 `(i - k) % n`，一共再看 `n - 1` 个起点，记录最大值。答案是 `k - 最大值`。

```python
def min_swaps(nums: list[int]) -> int:
    n, ones = len(nums), sum(nums)         # 最终 1 要聚成长度 ones 的一段
    window = sum(nums[:ones])              # 起点 0 的窗口里已有的 1 的个数
    best = window
    for i in range(ones, ones + n - 1):    # 窗口右端继续推进，下标对 n 取模当作环
        window += nums[i % n] - nums[(i - ones) % n]
        best = max(best, window)
    return ones - best                     # 窗口里的 0 的个数 = 需要换进来的 1 的个数
```

运行：`[0,1,0,1,1,0,0]` → `1`，`[0,1,1,1,0,0,1,1,0]` → `2`，`[1,1,0,0,1]` → `0`，`[0]` → `0`，`[1]` → `0`，`[0,0,0]` → `0`，`[1,1,1]` → `0`，`[1,0,0,0,1]` → `0`；长度 `10^5` 的随机数组约 `4 ms`。

**复杂度。** 时间 `O(n)`：初始窗口 `O(k)`，再 `n - 1` 次 `O(1)` 更新；空间 `O(1)`。

**写法要点。** `ones == 0` 或 `ones == n` 不需要特判：窗口长度为 `0` 时每次增量都是 `0`，`best = 0`，答案 `0`；窗口长度为 `n` 时 `best = n`，答案 `0`。`% n` 同时处理“右端越界”和“左端回绕”。想要少写下标运算，可以用前缀和：`pref = list(accumulate(nums + nums, initial=0))`，答案 `ones - max(pref[i + ones] - pref[i] for i in range(n))`，用 `O(n)` 空间换更直白的表达。
