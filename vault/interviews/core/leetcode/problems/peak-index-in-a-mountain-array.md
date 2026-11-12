---
slug: peak-index-in-a-mountain-array
---
## Q
**LC 852 山脉数组的峰顶索引**｜Medium

山脉数组先严格递增后严格递减，返回峰值下标，要求 `O(log n)`。

## A
**一句话。** 二分比较 `arr[mid]` 与 `arr[mid + 1]`：上坡丢掉左半，下坡保留 `mid` 丢掉右半。

```python
def peak_index_in_mountain_array(arr):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1     # 上坡：峰在右边
        else:
            hi = mid         # 下坡：mid 可能就是峰，保留
    return lo
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 下坡写成 `hi = mid - 1`：丢掉峰本身，`[0,10,5,2]` 返回 `0`，应为 `1`。
- 用 `while lo <= hi` 配合 `arr[mid + 1]`：`mid` 到最后一个下标时 `IndexError`。

**追问。**
- 为什么能二分？：`arr[mid] < arr[mid+1]` 把数组分成「上坡 / 下坡」两段，具有单调性，找第一个下坡点。
- 在山脉数组里找目标值（LC 1095）？：先找峰，再在升序段和降序段各二分一次。

**同模式。** LC 162 寻找峰值、LC 153 寻找旋转排序数组中的最小值、LC 1095 山脉数组中查找目标值、LC 658 找到 K 个最接近的元素
