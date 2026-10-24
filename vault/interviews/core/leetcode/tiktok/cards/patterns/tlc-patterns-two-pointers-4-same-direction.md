---
id: tlc-patterns-two-pointers-4-same-direction
node: patterns.two-pointers
type: qa
step: 4
---
## Q
**双指针（Two Pointers）｜同向快慢指针与三路分区**

「原地把非零元素移到前面」「原地去重」「0/1/2 排序」这三件事的指针各自维护什么区间？

## A
同向快慢指针：`fast` 负责读，`slow` 负责写，`slow` 左侧始终是「已处理好的结果」。

```python
def move_zeroes(nums: list[int]) -> None:
    slow = 0                               # nums[:slow] 全是非零元素
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
a = [0, 1, 0, 3, 12]
move_zeroes(a)
print(a)    # [1, 3, 12, 0, 0]

def remove_duplicates(nums: list[int]) -> int:
    slow = 0                               # nums[:slow] 是去重后的有序结果
    for x in nums:
        if slow == 0 or x != nums[slow - 1]:
            nums[slow] = x
            slow += 1
    return slow
b = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
k = remove_duplicates(b)
print(k, b[:k])    # 5 [0, 1, 2, 3, 4]
```

**三路分区（荷兰国旗，LC 75）**：三个区间 `[0, lo)` 全是 0、`[lo, i)` 全是 1、`(hi, n)` 全是 2，`[i, hi]` 是未处理区。

```python
def sort_colors(nums: list[int]) -> None:
    lo, i, hi = 0, 0, len(nums) - 1
    while i <= hi:
        if nums[i] == 0:
            nums[lo], nums[i] = nums[i], nums[lo]; lo += 1; i += 1
        elif nums[i] == 2:
            nums[i], nums[hi] = nums[hi], nums[i]; hi -= 1   # 换来的数还没检查，i 不动
        else:
            i += 1
a = [2, 0, 2, 1, 1, 0]; sort_colors(a); print(a)   # [0, 0, 1, 1, 2, 2]
```

交换 `2` 时 `i` 不前进，因为从 `hi` 换来的数未检查；交换 `0` 时 `i` 前进，因为从 `lo` 换来的一定是 `1`（已处理）。一次扫描 `O(n)`，空间 `O(1)`。
