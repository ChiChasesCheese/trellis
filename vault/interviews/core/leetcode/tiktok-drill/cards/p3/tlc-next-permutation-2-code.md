---
id: tlc-next-permutation-2-code
node: p3.next-permutation
type: qa
step: 2
---
## Q
**LC 31 下一个排列**｜写出 Python 实现

整数数组 `nums`（`1 <= nums.length <= 100`，`0 <= nums[i] <= 100`，可能有重复），原地改成字典序的下一个排列；已是最大排列时改成升序。只能用常数额外空间。

## A
**思路。** 三步：从右往左找第一个升位 `i`；如果存在，在右边的降序段里从右往左找第一个比 `nums[i]` 大的 `j`，交换；最后把 `i` 右边整段用双指针翻转。`i = -1` 时翻转整个数组，正好得到最小排列。

```python
def next_permutation(nums: list[int]) -> None:
    n = len(nums)
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:    # 从右找第一个"升"的位置：nums[i] < nums[i+1]
        i -= 1
    if i >= 0:
        j = n - 1
        while nums[j] <= nums[i]:               # 右边降序段里，从右数第一个比 nums[i] 大的
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    lo, hi = i + 1, n - 1                       # i = -1 时整个数组翻转，正好是最小排列
    while lo < hi:                              # 右边是降序段，翻转成升序 = 最小
        nums[lo], nums[hi] = nums[hi], nums[lo]
        lo, hi = lo + 1, hi - 1
```

运行：`[1,2,3]` → `[1, 3, 2]`，`[3,2,1]` → `[1, 2, 3]`，`[1,1,5]` → `[1, 5, 1]`，`[1,3,2,2]` → `[2, 1, 2, 3]`，`[2,3,1]` → `[3, 1, 2]`。

**复杂度。** 时间 `O(n)`：三个循环各最多扫一遍；空间 `O(1)`：只有几个下标。

**写法要点。** 函数没有返回值（返回类型 `None`），因为题目要求原地修改；`nums[i], nums[j] = nums[j], nums[i]` 是 Python 的元组交换，右边先全部求值再赋值，不需要临时变量；`while nums[j] <= nums[i]` 不用检查 `j` 越界，因为 `i` 位置的后面一定有一个更大的数（`nums[i+1] > nums[i]`），循环必在 `j = i + 1` 前停下；翻转用双指针而不用切片，保证严格 `O(1)` 额外空间。
