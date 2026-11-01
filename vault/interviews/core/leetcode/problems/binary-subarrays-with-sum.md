---
slug: binary-subarrays-with-sum
---
## Q
**LC 930 和相同的二元子数组**｜Medium

给你一个二元数组 `nums`（每个元素不是 `0` 就是 `1`）和一个整数 `goal`，统计并返回有多少个和为 `goal` 的非空子数组。`1 <= nums.length <= 3 * 10^4`，`0 <= goal <= nums.length`。例：`nums = [1,0,1,0,1], goal = 2` → `4`（`[1,0,1]`、`[1,0,1,0]`、`[0,1,0,1]`、`[1,0,1]`）；`nums = [0,0,0,0,0], goal = 0` → `15`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 前缀和（prefix sum）+ 哈希计数。

**一句话。** 子数组和等于两个前缀和之差，扫描时用哈希表记每个前缀和出现的次数，当前前缀为 `pre` 时，以当前位置结尾且和为 `goal` 的子数组个数就是 `pre - goal` 出现过的次数。

**识别。** 「统计和为 k 的子数组个数」就是 LC 560 的形状，`n = 3 * 10^4` 排除 `O(n^2)` 的枚举（约 `4.5 * 10^8` 次）。元素非负时滑动窗口也可以，但 `goal = 0` 的边界更容易出错。

**推导。** 暴力枚举两端 `O(n^2)`；固定右端点 `i`，要找左端点 `j` 使 `pre[i] - pre[j] = goal`，即 `pre[j] = pre[i] - goal`。浪费在于对每个 `i` 重新数满足条件的 `j`；一边扫一边把已见前缀和的出现次数放进哈希表，每个右端点 `O(1)` 查到答案。

```python
def num_subarrays_with_sum(nums: list[int], goal: int) -> int:
    seen = Counter({0: 1})        # 前缀和 -> 出现次数；空前缀的和为 0，出现 1 次
    pre = ans = 0
    for x in nums:
        pre += x
        ans += seen[pre - goal]   # 以当前位置结尾、和恰为 goal 的子数组个数
        seen[pre] += 1            # 先查后存：左端点必须在当前位置之前
    return ans
```

运行：`([1,0,1,0,1], 2)` → `4`，`([0,0,0,0,0], 0)` → `15`，`([1], 1)` → `1`，`([1], 0)` → `0`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`（前缀和只会取 `0..n`）。

**拓展优化。**
- 元素非负，所以「和恰好为 goal」等于「和至多 goal」减去「和至多 goal - 1」，每个都是滑动窗口，空间 `O(1)`：

```python
def num_subarrays_with_sum_window(nums: list[int], goal: int) -> int:
    def at_most(k: int) -> int:           # 和 <= k 的子数组个数
        if k < 0:
            return 0                      # goal = 0 时 at_most(-1) 必须是 0
        left = total = count = 0
        for right, x in enumerate(nums):
            total += x
            while total > k:              # 窗口和超标：左端点右移
                total -= nums[left]
                left += 1
            count += right - left + 1     # 以 right 结尾、左端点在 [left, right] 的子数组都合法
        return count

    return at_most(goal) - at_most(goal - 1)
```

**易错点。**
- 忘了预置 `{0: 1}`：以下标 0 开头的子数组会漏掉，`([1], 1)` 会返回 `0`（正确 `1`）。
- 先存后查会把空子数组算进去：`goal = 0` 时 `([0,0,0,0,0], 0)` 会多算 5 个，得到 `20`（正确 `15`）。
- `at_most(goal - 1)` 在 `goal = 0` 时参数为 `-1`，不特判会在 `while total > k` 里一直左移到越界。

**同模式。** LC 560 和为 K 的子数组、LC 713 乘积小于 K 的子数组、LC 974 和可被 K 整除的子数组、LC 992 K 个不同整数的子数组。
