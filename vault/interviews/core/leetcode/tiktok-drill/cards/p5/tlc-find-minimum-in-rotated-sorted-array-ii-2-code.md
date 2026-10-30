---
id: tlc-find-minimum-in-rotated-sorted-array-ii-2-code
node: p5.find-minimum-in-rotated-sorted-array-ii
type: qa
step: 2
---
## Q
**LC 154 寻找旋转排序数组中的最小值 II**｜写出 Python 实现

升序数组旋转 `1` 到 `n` 次得到 `nums`（`1 <= n <= 5000`，`-5000 <= nums[i] <= 5000`，可能有重复）。返回其中的最小元素，步骤尽量少。

## A
**思路。** 区间 `[lo, hi]` 内始终含有最小值。比较 `nums[mid]` 与 `nums[hi]`：大于，最小值只能在 `mid` 右边，`lo = mid + 1`；小于，最小值在 `mid` 或其左边，`hi = mid`；相等，丢掉 `hi`（`mid` 处有相同的值），`hi -= 1`。`lo == hi` 时就是答案。

```python
def find_min(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:        # 最小值一定在 mid 右边（mid 本身不是）
            lo = mid + 1
        elif nums[mid] < nums[hi]:      # 最小值在 mid 或它左边
            hi = mid
        else:                           # 相等：看不出在哪一侧，但 nums[hi] 有 nums[mid] 这个“替身”，可以安全丢掉
            hi -= 1
    return nums[lo]
```

运行：`[1,3,5]` → `1`；`[2,2,2,0,1]` → `0`；`[3,3,1,3]` → `1`；`[1]` → `1`；`[2,1]` → `1`；`[1,1]` → `1`；`[10,1,10,10,10]` → `1`；`[4,5,6,7,0,1,4]` → `0`；`[1] * 5000` → `1`。

**复杂度。** 平均 `O(log n)`，最坏 `O(n)`；空间 `O(1)`。

**写法要点。** 循环条件 `lo < hi`，区间收缩到一个元素时结束，不需要额外判断；`mid = (lo + hi) // 2` 向下取整，所以 `mid < hi`，`lo = mid + 1` 和 `hi = mid` 都保证区间严格变小，不会死循环；与 `nums[hi]` 比较而不是 `nums[lo]`，是因为右端点能区分 `mid` 落在哪一段；相等分支 `hi -= 1` 只在重复值上触发，每次只缩一格；Python 的整数不会溢出，`(lo + hi) // 2` 不需要写成 `lo + (hi - lo) // 2`。
