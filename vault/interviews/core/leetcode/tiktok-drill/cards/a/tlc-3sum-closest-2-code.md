---
id: tlc-3sum-closest-2-code
node: a.3sum-closest
type: qa
step: 2
---
## Q
**LC 16 最接近的三数之和**｜写出 Python 实现

整数数组 `nums`（长度 `3..1000`，元素 `-1000..1000`）和整数 `target`（`-10^4..10^4`）。选三个不同下标的数，返回与 `target` 最接近的和（保证解唯一）。要求 `O(n^2)`，且不要改动调用者传入的数组。

## A
**思路。** 先 `sorted` 得到新数组。外层枚举第一个数 `nums[i]`，内层 `lo = i + 1`、`hi = n - 1`。算出和 `s`，若比当前最优更接近 `target` 就更新；恰好等于就返回；`s < target` 右移 `lo`，否则左移 `hi`。

```python
def three_sum_closest(nums: list[int], target: int) -> int:
    nums = sorted(nums)                          # 排序后才能用双指针；用 sorted 不改动调用者的数组
    best = nums[0] + nums[1] + nums[2]
    for i in range(len(nums) - 2):
        if i and nums[i] == nums[i - 1]:         # 相同的第一个数结果相同，跳过
            continue
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if abs(s - target) < abs(best - target):
                best = s
            if s == target:                      # 不可能更近了
                return s
            if s < target:
                lo += 1                          # 和偏小：左指针右移，让和变大
            else:
                hi -= 1                          # 和偏大：右指针左移，让和变小
    return best
```

**运行。** `([-1,2,1,-4], 1)` → `2`；`([0,0,0], 1)` → `0`；`([1,1,1,0], -100)` → `2`；`([1,1,-1,-1,3], -1)` → `-1`；`([-1000,-1000,-1000], 10000)` → `-3000`。

**复杂度。** 时间 `O(n^2)`：外层 `n` 次，内层双指针最多 `n` 步；空间 `O(n)`（`sorted` 的拷贝）。

**写法要点。** `nums = sorted(nums)` 重新绑定到新列表，调用者的数组不变，比 `nums.sort()` 更安全；`best` 用前三个数之和初始化，保证是一个真实的三数之和；`if i and nums[i] == nums[i - 1]` 用 `i` 的真值同时跳过 `i = 0`，不会访问 `nums[-1]`；用 `abs(s - target)` 比较"距离"，不是比较和本身。
