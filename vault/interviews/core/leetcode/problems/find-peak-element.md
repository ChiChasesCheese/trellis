---
slug: find-peak-element
---
## Q
**LC 162 寻找峰值**｜Medium

数组相邻元素不相等，两端之外视为负无穷，返回任意一个峰值（严格大于左右邻居）的下标，要求 `O(log n)`。

## A
**一句话。** 对坡度二分：`nums[mid] < nums[mid+1]` 是上坡，右边必有峰；否则 `mid` 或左边有峰。

```python
def find_peak_element(nums):
    lo, hi = 0, len(nums) - 1    # [lo, hi] 内一定有峰
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:   # 上坡，往右
            lo = mid + 1
        else:                           # 下坡，mid 可能就是峰
            hi = mid
    return lo
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 下坡写 `hi = mid - 1`：排除了可能是峰的 `mid`，`[1,2,1]` 返回下标 `0`，不是峰。
- 用 `lo <= hi` 模板：`mid+1` 可能越界；这里 `lo < hi` 且 `hi = mid`，收缩到一点即答案。

**追问。**
- 相邻元素可以相等呢？：平台处无法判断方向，二分失效，最坏退化成 `O(n)`。
- 二维矩阵的峰值（LC 1901）？：取中间列的最大值，与左右比较，往更大一侧收缩，`O(m log n)`。

**同模式。** LC 852 山脉数组的峰顶索引、LC 1095 山脉数组中查找目标值、LC 153 寻找旋转排序数组中的最小值、LC 1901 寻找峰值 II
