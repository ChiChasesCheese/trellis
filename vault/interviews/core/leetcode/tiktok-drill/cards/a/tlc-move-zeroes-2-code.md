---
id: tlc-move-zeroes-2-code
node: a.move-zeroes
type: qa
step: 2
---
## Q
**LC 283 移动零**｜写出 Python 实现

`nums`（长度 `1` 到 `10^4`，值在 `[-2^31, 2^31 - 1]`）里，原地把所有 `0` 移到末尾，非零元素保持原来的相对顺序；不返回值，也不能复制数组；尽量少做写入。

## A
**思路。** `write` 指向下一个非零元素该去的位置。`read` 从头扫到尾，遇到非零元素就和 `write` 处交换（把零换到 `read`），然后 `write` 加一。若 `write == read`，说明这个元素前面没有零，已经在位，不必写。

```python
def move_zeroes(nums: list[int]) -> None:
    write = 0                                  # nums[:write] 是已经排好的非零元素
    for read in range(len(nums)):
        if nums[read] != 0:
            if write != read:                  # write == read 说明前面还没有零，不用动
                nums[write], nums[read] = nums[read], 0
            write += 1
```

运行：`[0,1,0,3,12]` → `[1,3,12,0,0]`，`[0]` → `[0]`，`[1,2,3]` → `[1,2,3]`，`[0,0,1]` → `[1,0,0]`，`[3,0]` → `[3,0]`；长 `10^4`、奇数位全为 `0` 的数组 → 前部是 `[1, 3, 5, ...]`、末尾全 `0`。

**复杂度。** 时间 `O(n)`：每个下标看一次；空间 `O(1)`。

**写法要点。** `nums[write], nums[read] = nums[read], 0` 先算右边的元组，再同时赋值，等价于「把非零值放到 `write`、把 `read` 清零」，比交换少一次读；用 `range(len(nums))` 而不是 `for x in nums`，因为循环里要写数组；不要写 `nums = ...`，那只是改了局部变量，调用方看不到。
