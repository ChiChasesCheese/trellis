---
id: tlc-count-number-of-nice-subarrays-4-followup
node: p3.count-number-of-nice-subarrays
type: qa
step: 4
---
## Q
**LC 1248 统计「优美子数组」**｜追问

面试官接着问：（1）要求 `O(1)` 额外空间？（2）有没有只扫描奇数位置的写法？（3）推广到「恰好 `k` 个满足某个条件的元素」？

## A
1. **`O(1)` 空间：至多 `k` 减至多 `k - 1`。** 滑动窗口数“奇数个数不超过 `m`”的子数组，每个右端点贡献 `right - left + 1`：
```python
def at_most(nums: list[int], m: int) -> int:
    left = odd = ans = 0
    for right, x in enumerate(nums):
        odd += x & 1
        while odd > m:                      # 奇数太多：缩左端
            odd -= nums[left] & 1
            left += 1
        ans += right - left + 1             # 以 right 结尾、奇数个数 <= m 的子数组个数
    return ans
```
答案是 `at_most(nums, k) - at_most(nums, k - 1)`。`[1,1,2,1,1]`，`k = 3` 得到 `2`。两趟扫描，`O(1)` 空间。
2. **奇数位置相乘。** 把所有奇数的下标取出来，两端各补一个哨兵 `-1` 和 `n`；窗口以第 `i` 个奇数开头、含 `k` 个奇数时，起点可以在上一个奇数之后到这个奇数之间任选，终点在第 `i + k - 1` 个奇数到下一个奇数之间任选：
```python
def number_of_subarrays_gaps(nums: list[int], k: int) -> int:
    odds = [-1] + [i for i, x in enumerate(nums) if x & 1] + [len(nums)]
    return sum((odds[i] - odds[i - 1]) * (odds[i + k] - odds[i + k - 1])
               for i in range(1, len(odds) - k))
```
`[2,2,2,1,2,2,1,2,2,2]`，`k = 2` 得到 `16`。只扫一遍奇数位置，`O(n)`。
3. **推广。** 先把元素映射成 `0/1`（满足条件为 `1`），再套用前缀计数；条件可以是“是否为质数”“是否大于阈值”等任意谓词。

**Python 提醒**：列表负下标不报错，`seen[odd - k]` 在 `odd < k` 时会静默读到数组尾部的元素；写前缀计数时要么加 `if odd >= k` 的保护，要么用 `Counter` / `dict`，那样缺失的键返回 `0`。
