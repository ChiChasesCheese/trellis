---
slug: binary-subarrays-with-sum
---
## Q
**LC 930 和相同的二元子数组**｜Medium

`nums` 只含 `0` 和 `1`，统计和恰为 `goal` 的非空子数组个数。

## A
**一句话。** 前缀和加哈希表计数：以当前位置结尾、和为 `goal` 的子数组个数就是 `pre - goal` 出现过的次数。

```python
def num_subarrays_with_sum(nums, goal):
    seen = Counter({0: 1})   # 空前缀
    pre = ans = 0
    for x in nums:
        pre += x
        ans += seen[pre - goal]   # 先查后存
        seen[pre] += 1
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 漏了 `{0: 1}`：从下标 0 开头的子数组漏掉，`([1], 1)` 得 `0`，应为 `1`。
- 先存后查：`goal = 0` 时把空子数组算进去，`[0,0,0,0,0]` 得 `20`，应为 `15`。

**追问。**
- 元素全非负怎么省空间？：滑动窗口，`at_most(goal) - at_most(goal - 1)`，`goal = 0` 时 `at_most(-1)` 要返回 `0`。
- 元素可为负呢？：滑动窗口失效，只能用前缀和哈希表。

**同模式。** LC 560 和为 K 的子数组、LC 713 乘积小于 K 的子数组、LC 974 和可被 K 整除的子数组、LC 992 K 个不同整数的子数组
