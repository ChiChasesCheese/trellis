---
id: tlc-first-missing-positive-2-code
node: b.first-missing-positive
type: qa
step: 2
---
## Q
**LC 41 缺失的第一个正数**｜写出 Python 实现

未排序整数数组 `nums`（`1 <= nums.length <= 10^5`，值在 `[-2^31, 2^31 - 1]`）。返回没有出现的最小正整数，要求 `O(n)` 时间、`O(1)` 额外空间（允许修改输入）。

## A
**思路。** 第一遍：对每个下标 `i`，只要 `nums[i]` 在 `[1, n]` 内并且它的目标位置还没有放好同一个值，就把它交换过去。第二遍：从左往右找第一个 `nums[i] != i + 1`，返回 `i + 1`；都对就返回 `n + 1`。

```python
def first_missing_positive(nums: list[int]) -> int:
    n = len(nums)
    for i in range(n):
        # 把每个落在 [1, n] 的数 x 送到下标 x - 1；目标位置已是 x 就停（重复值）
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1             # 先把目标下标存下来，下面交换会改 nums[i]
            nums[i], nums[j] = nums[j], nums[i]
    for i, x in enumerate(nums):        # 第一个"站错位"的下标就是答案
        if x != i + 1:
            return i + 1
    return n + 1                        # 1..n 全在，答案只能是 n + 1
```

运行：`[1,2,0]` → `3`，`[3,4,-1,1]` → `2`，`[7,8,9,11,12]` → `1`，`[1]` → `2`，`[2]` → `1`，`[1,1]` → `2`，`10^5` 个打乱的 `1..n` → `100001`。

**复杂度。** 时间 `O(n)`：每次交换让一个数永久回到自己的位置，总共至多 `n` 次，外层 `for` 和第二遍扫描各 `n` 步；空间 `O(1)`。

**写法要点。** 链式比较 `1 <= nums[i] <= n` 一次判断两端；`nums[nums[i] - 1] != nums[i]` 同时挡住重复值和已归位的情况，保证每次交换都有进展；`j = nums[i] - 1` 先存下目标下标，再做 `nums[i], nums[j] = nums[j], nums[i]`，避开元组赋值里左边下标被先赋的值改变的陷阱；`for i, x in enumerate(nums)` 同时拿下标和值，不用 `nums[i]` 再取一次。
