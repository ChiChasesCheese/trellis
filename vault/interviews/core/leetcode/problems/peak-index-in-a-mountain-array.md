---
slug: peak-index-in-a-mountain-array
---
## Q
**LC 852 山脉数组的峰顶索引**｜Medium

给定一个长度为 `n` 的整数山脉数组 `arr`，其中的值递增到一个峰值元素然后递减，返回峰值元素的下标。必须设计并实现时间复杂度为 `O(log n)` 的解决方案。`3 <= arr.length <= 10^5`，`0 <= arr[i] <= 10^6`，题目数据保证 `arr` 是一个山脉数组。例：`arr = [0,1,0]` → `1`；`arr = [0,2,1,0]` → `1`；`arr = [0,10,5,2]` → `1`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 二分查找（binary search）：在「先升后降」上按斜率二分，找第一个下降点。

**一句话。** 比较 `arr[mid]` 与 `arr[mid + 1]`：在上坡就丢掉左半（含 `mid`），在下坡就保留 `mid` 并丢掉右半，区间收缩到一个点就是峰。

**识别。** 「要求 `O(log n)`」且数组只有一个峰：把它改写成「下标 `i` 满足 `arr[i] > arr[i+1]`」这个布尔条件，它在峰之前全为假、峰及之后全为真，即对下标单调，可以二分。

**推导。** 线性扫描找最大值是 `O(n)`，题目禁止。观察 `arr[mid]` 和右邻居：`arr[mid] < arr[mid+1]` 说明 `mid` 还在上坡，峰在 `mid + 1` 及右边；否则 `mid` 在峰或下坡，峰在 `mid` 及左边（`mid` 本身可能就是峰，不能丢）。

```python
def peak_index_in_mountain_array(arr: list[int]) -> int:
    lo, hi = 0, len(arr) - 1              # 峰一定在 [lo, hi] 内
    while lo < hi:
        mid = (lo + hi) // 2              # 向下取整：mid < hi，所以 arr[mid + 1] 不会越界
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1                  # 上坡：峰在右边，mid 不可能是峰
        else:
            hi = mid                      # 下坡（或 mid 就是峰）：峰在 mid 或左边，保留 mid
    return lo
```

运行：`[0,1,0]` → `1`，`[0,2,1,0]` → `1`，`[0,10,5,2]` → `1`，`[0,1,2,3,2]` → `3`，`[1,3,5,4,2]` → `2`。

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**拓展优化。**
- 标准库写法（Python 3.10+）：对「是否已下降」这个单调布尔值二分，不用手写循环：

```python
def peak_index_bisect(arr: list[int]) -> int:
    # key 在下标 i 上给出 arr[i] > arr[i+1]：峰之前为 False，峰及之后为 True
    return bisect_left(range(len(arr) - 1), True, key=lambda i: arr[i] > arr[i + 1])
```

- 数组里允许平台（相邻相等）时 `arr[mid]` 与 `arr[mid + 1]` 相等就无法判断方向，最坏退化成 `O(n)`。

**易错点。**
- 下坡分支写成 `hi = mid - 1` 会丢掉峰本身：`[0,10,5,2]` 第一次 `mid = 1` 就是峰，`hi = 0` 之后返回 `0`（正确 `1`）。
- 用 `while lo <= hi` 配合 `arr[mid + 1]`，当 `mid` 到达最后一个下标会 `IndexError`；用 `lo < hi` 配合 `hi = mid` 的闭区间收缩写法更稳。

**同模式。** LC 162 寻找峰值、LC 153 寻找旋转排序数组中的最小值、LC 1095 山脉数组中查找目标值、LC 658 找到 K 个最接近的元素。
