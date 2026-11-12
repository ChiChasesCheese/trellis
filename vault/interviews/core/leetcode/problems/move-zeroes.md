---
slug: move-zeroes
---
## Q
**LC 283 移动零**｜Easy

原地把数组中所有 `0` 移到末尾，保持非零元素的相对顺序。

## A
**一句话。** 快慢双指针：`read` 扫描，遇到非零就与 `write` 处交换，`write` 前进。

```python
def move_zeroes(nums):
    write = 0   # nums[:write] 是已放好的非零元素
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = (nums[read],
                                       nums[write])
            write += 1
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只覆盖不补零：`[0,1,0,3,12]` 停在 `[1,3,12,3,12]`。
- 边遍历边 `remove`：会跳过相邻元素，且是 `O(n^2)`。

**追问。**
- 为什么交换而不是覆盖？：交换保证 `nums[write:read]` 全是 `0`，一趟结束，不用补零。
- 要把写入次数降到最少？：加 `write != read` 判断，只在前面有零时才交换。

**同模式。** LC 27 移除元素、LC 26 删除有序数组中的重复项、LC 75 颜色分类
