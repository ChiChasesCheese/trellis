---
slug: sort-an-array
---
## Q
**LC 912 排序数组**｜Medium

不使用内置排序函数，把整数数组升序排列，时间 `O(n log n)`，空间尽量小。

## A
**一句话。** 堆排序：原地建大根堆，再反复把堆顶换到末尾并下沉修复。

```python
def sort_array(nums):
    n = len(nums)
    def sift(root, size):      # nums[root] 下沉进 nums[:size]
        val = nums[root]
        while (c := 2 * root + 1) < size:
            if c + 1 < size and nums[c + 1] > nums[c]:
                c += 1          # 选较大的孩子
            if nums[c] <= val:
                break
            nums[root] = nums[c]
            root = c
        nums[root] = val
    for i in range(n // 2 - 1, -1, -1):   # 自底向上建堆
        sift(i, n)
    for end in range(n - 1, 0, -1):
        nums[0], nums[end] = nums[end], nums[0]
        sift(0, end)
    return nums
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`。

**易错点。**
- 建堆从 `0` 往后下沉：必须从最后一个非叶子 `n // 2 - 1` 倒着下沉，`[1,2,3,4]` 会错成 `[1,2,4,3]`。
- `sift(0, end)` 写成 `sift(0, n)`：已排好的后缀被拉回堆里，结果被破坏。
- 选孩子前不判断 `c + 1 < size`：最后一层越界。

**追问。**
- 为什么常有人写快排？：平均更快，但固定首元素当基准遇到有序数组退化成 `O(n^2)`，要用随机基准加三路划分。
- 需要稳定排序？：用归并排序，额外空间 `O(n)`。

**同模式。** LC 215 数组中的第 K 个最大元素、LC 75 颜色分类、LC 148 排序链表、LC 315 计算右侧小于当前元素的个数
