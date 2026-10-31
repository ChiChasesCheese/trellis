---
id: tlc-minimum-size-subarray-sum-2-code
node: p2.minimum-size-subarray-sum
type: qa
step: 2
---
## Q
**LC 209 长度最小的子数组**｜写出 Python 实现

正整数数组 `nums`（长度 `1` 到 `10^5`，每个元素 `1` 到 `10^4`）和正整数 `target`（至多 `10^9`），返回和大于等于 `target` 的最短连续子数组的长度，没有则返回 `0`。要求 `O(n)`。

## A
**思路。** 右端依次吃进元素并累加。每当窗口和 `>= target`，就用当前长度更新答案，并缩左端，直到和重新小于 `target`。哨兵 `len(nums) + 1` 表示“还没找到”。

```python
def min_sub_array_len(target: int, nums: list[int]) -> int:
    best = len(nums) + 1                    # 哨兵：比任何合法长度都大
    left = total = 0
    for right, x in enumerate(nums):
        total += x                          # 右端吃进 x
        while total >= target:              # 窗口和够了：尽量缩左端，每缩一步都是一个候选答案
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return best if best <= len(nums) else 0
```

运行：`(7, [2,3,1,2,4,3])` → `2`，`(4, [1,4,4])` → `1`，`(11, [1,1,1,1,1,1,1,1])` → `0`，`(1, [1])` → `1`。

**复杂度。** 时间 `O(n)`：`left` 与 `right` 都只前进，各自最多 `n` 步；空间 `O(1)`。

**写法要点。**
- `for right, x in enumerate(nums)` 同时拿到下标和值；`left` 手动维护，因为它会在内层 `while` 里前进。
- 哨兵代替 `inf`：保持 `best` 一直是 `int`，最后用 `best <= len(nums)` 判断有没有找到；写成 `float("inf")` 也行，但返回类型会混入浮点。
- `total` 是 `int`，`while total >= target` 里先用 `right - left + 1` 记录，再减 `nums[left]` 并 `left += 1`，顺序反了会少记一格。
- 进阶 `O(n log n)`：`pre = list(accumulate(nums, initial=0))`，对每个 `i` 做 `bisect_left(pre, pre[i] + target)`，`initial=0` 让 `pre` 带上空前缀的 `0`。
