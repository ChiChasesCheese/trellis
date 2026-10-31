---
id: tlc-find-k-closest-elements-0-whole
node: c.find-k-closest-elements
type: qa
---
## Q
**LC 658 找到 K 个最接近的元素**｜Medium · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 5 次 · 最近 2025-09-22（国内 CodeTop）

给定一个排好序（升序）的数组 `arr`，以及整数 `k` 和 `x`，从数组中找到最靠近 `x` 的 `k` 个数，结果按升序返回。整数 `a` 比整数 `b` 更接近 `x` 指：`|a - x| < |b - x|`，或者 `|a - x| == |b - x|` 且 `a < b`。`1 <= k <= arr.length <= 10^4`，`arr` 升序，`-10^4 <= arr[i], x <= 10^4`。例：`arr = [1,2,3,4,5], k = 4, x = 3` → `[1,2,3,4]`；`arr = [1,1,2,3,4,5], k = 4, x = -1` → `[1,1,2,3]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 答案是原数组里长度为 `k` 的连续窗口，二分窗口左端点：比较 `arr[mid]` 和窗口外的 `arr[mid + k]` 谁离 `x` 更近，窗口往更近的一侧挪，`O(log(n - k) + k)`。

**识别。** 「有序数组 + 取离某值最近的 k 个」：最近的元素在有序数组里必然挨着，答案是连续段；有序加「找位置」就想二分，只是二分对象是窗口起点而不是元素。

**推导。** 暴力：按 `(|a - x|, a)` 排序取前 `k` 个再排回升序，`O(n log n)`，浪费在数组本来有序。洞察：相邻窗口 `[mid, mid + k - 1]` 与 `[mid + 1, mid + k]` 只差 `arr[mid]` 和 `arr[mid + k]`；`x - arr[mid] > arr[mid + k] - x` 随 `mid` 增大从真变假，单调，可以二分左端点 `[0, n - k]`。

**简单解法。** 按（距离，值）排序取前 `k` 个，再按值排回升序。

```python
def find_closest_elements_sort(arr: list[int], k: int, x: int) -> list[int]:
    return sorted(sorted(arr, key=lambda a: (abs(a - x), a))[:k])   # 平局按值小的优先
```

`O(n log n)`，`n <= 10^4` 够用，但没用上「已排序」，面试官会追问 `O(log n)`。

最优解：

```python
def find_closest_elements(arr: list[int], k: int, x: int) -> list[int]:
    lo, hi = 0, len(arr) - k                 # 窗口左端点的候选范围 [0, n - k]
    while lo < hi:
        mid = (lo + hi) // 2
        # 比较窗口 [mid, mid+k-1] 与 [mid+1, mid+k]：只差 arr[mid] 和 arr[mid+k]
        if x - arr[mid] > arr[mid + k] - x:  # 右侧新元素更近：左端点一定在 mid 右边
            lo = mid + 1
        else:                                # 左侧不比右侧远（相等时取小的）：左端点不会超过 mid
            hi = mid
    return arr[lo:lo + k]
```

运行：`([1,2,3,4,5], 4, 3)` → `[1,2,3,4]`；`([1,1,2,3,4,5], 4, -1)` → `[1,1,2,3]`；`([1,2,3,4,5], 4, 10)` → `[2,3,4,5]`；`([5], 1, 3)` → `[5]`；`([1,3], 1, 2)` → `[1]`。

**复杂度。** 时间 `O(log(n - k) + k)`，空间 `O(1)`（不计输出）。

**拓展优化。**
- 双指针从两端收缩，`O(n - k)`，没有下标范围的坑。

```python
def find_closest_elements_shrink(arr: list[int], k: int, x: int) -> list[int]:
    left, right = 0, len(arr) - 1
    while right - left + 1 > k:              # 每轮丢掉离 x 更远的一端，直到只剩 k 个
        if x - arr[left] <= arr[right] - x:  # 左端不比右端远：丢右端（相等时保留小的）
            right -= 1
        else:
            left += 1
    return arr[left:right + 1]
```

- 先 `bisect_left(arr, x)` 定位，再向两边各扩展、每步取更近的一个，共 `k` 步，`O(log n + k)`。

**易错点。**
- 平局方向写反：`arr = [1,3], k = 1, x = 2` 应返回 `[1]`，把 `>` 写成 `>=` 会返回 `[3]`。
- 上界写成 `len(arr) - 1`：`mid + k` 越界，左端点最大只能是 `n - k`。
- 二分元素值后只取一侧：会漏掉左右各取一部分的情形。

**追问。**
- 数组没排序：大小为 `k` 的堆，`heapq.nsmallest(k, arr, key=lambda a: (abs(a - x), a))`，`O(n log k)`。
- 只要最近的 1 个：二分找插入位置后比较左右邻居。

**同模式。** LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 35 搜索插入位置、LC 33 搜索旋转排序数组、LC 719 找出第 K 小的数对距离、LC 215 数组中的第K个最大元素。
