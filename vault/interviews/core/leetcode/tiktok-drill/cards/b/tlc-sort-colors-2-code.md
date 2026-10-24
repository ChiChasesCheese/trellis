---
id: tlc-sort-colors-2-code
node: b.sort-colors
type: qa
step: 2
---
## Q
**LC 75 颜色分类**｜写出 Python 实现

数组 `nums`（长度 `1..300`，元素 `0`、`1`、`2`）。写 `sort_colors(nums)`，原地排成升序，不使用库自带的排序，一趟扫描、`O(1)` 额外空间。函数不返回值。

## A
**思路。** 三指针：`lo` 是 `0` 区的右边界，`hi` 是 `2` 区的左边界，`i` 扫描中间未检查部分；`0` 与 `lo` 换，`2` 与 `hi` 换，`1` 跳过。

```python
def sort_colors(nums: list[int]) -> None:
    # 不变量：nums[:lo] 全是 0，nums[lo:i] 全是 1，nums[hi+1:] 全是 2，nums[i:hi+1] 未检查
    lo, i, hi = 0, 0, len(nums) - 1
    while i <= hi:
        if nums[i] == 0:
            nums[lo], nums[i] = nums[i], nums[lo]   # 换来的一定是 1（区间 [lo, i) 全是 1），i 可以前进
            lo += 1
            i += 1
        elif nums[i] == 2:
            nums[i], nums[hi] = nums[hi], nums[i]   # 换来的是未检查的数，i 不能动
            hi -= 1
        else:
            i += 1
```

运行：`[2,0,2,1,1,0]` → `[0, 0, 1, 1, 2, 2]`，`[2,0,1]` → `[0, 1, 2]`，`[0]` → `[0]`，`[1,2,0]` → `[0, 1, 2]`，`[2,2,2]` → `[2, 2, 2]`。

**复杂度。** 时间 `O(n)`：`i` 每步前进，或者 `hi` 每步后退，总步数不超过 `n`；空间 `O(1)`。

**写法要点。** `nums[a], nums[b] = nums[b], nums[a]` 是 Python 的交换惯用法，右边先整体求值，不需要临时变量。循环条件是 `i <= hi`（含等号），因为 `hi` 指向的位置也还没检查。三个分支里只有「换 `2`」不动 `i`。函数原地修改并返回 `None`，类型标注为 `-> None`。
