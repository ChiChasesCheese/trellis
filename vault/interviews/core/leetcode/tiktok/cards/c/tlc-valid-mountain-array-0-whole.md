---
id: tlc-valid-mountain-array-0-whole
node: c.valid-mountain-array
type: qa
---
## Q
**LC 941 有效的山脉数组**｜Easy · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 1 次 · 最近 2021-06-09（国内 CodeTop）

给定整数数组 `arr`，如果它是有效的山脉数组返回 `true`，否则返回 `false`。山脉数组满足：`arr.length >= 3`，并且存在下标 `i`（`0 < i < arr.length - 1`），使得 `arr[0] < arr[1] < ... < arr[i - 1] < arr[i]` 且 `arr[i] > arr[i + 1] > ... > arr[arr.length - 1]`（严格上升再严格下降）。`1 <= arr.length <= 10^4`，`0 <= arr[i] <= 10^4`。例：`[2,1]` → `false`；`[3,5,5]` → `false`；`[0,3,2,1]` → `true`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先爬坡到不能再升，再下坡到不能再降，山顶不能是起点或终点，最后恰好走到末尾才是山脉。

**识别。** 「先严格增再严格减」的形状判断：一遍双阶段扫描，用位置判断两个阶段是否都非空、是否覆盖全数组。

**推导。** 枚举山顶并验证两侧，`O(n²)`。更好：从左往右爬到第一个不再上升的位置 `i`，这就是山顶；山顶在 `0`（没有上坡）或 `n - 1`（没有下坡）则不是山脉；再从山顶继续下降，必须恰好走到 `n - 1`。平台（相等）会让两个阶段都停下，结果走不到末尾。

```python
def valid_mountain_array(arr: list[int]) -> bool:
    n = len(arr)
    i = 0
    while i + 1 < n and arr[i] < arr[i + 1]:     # 上坡：严格递增
        i += 1
    if i == 0 or i == n - 1:                     # 没有上坡，或者只有上坡没有下坡
        return False
    while i + 1 < n and arr[i] > arr[i + 1]:     # 下坡：严格递减
        i += 1
    return i == n - 1                            # 必须一路下坡走到末尾
```

运行：`[2,1]` → `False`，`[3,5,5]` → `False`，`[0,3,2,1]` → `True`；`[0,1,2,3]` → `False`（只有上坡），`[1,2,2,1]` → `False`（平台）。

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**拓展优化。**
- 两端同时向山顶逼近，两个指针必须在同一点相遇：

```python
def valid_mountain_array_two_pointers(arr: list[int]) -> bool:
    n = len(arr)
    left, right = 0, n - 1
    while left + 1 < n and arr[left] < arr[left + 1]:     # 左边爬坡
        left += 1
    while right > 0 and arr[right - 1] > arr[right]:      # 右边从末尾往回爬坡
        right -= 1
    return 0 < left == right < n - 1
```

- 最长山脉子数组（LC 845）：同样的上坡下坡扫描，记录每个山顶两侧的长度。

**易错点。**
- 没有检查山顶位置：`[0,1,2,3]` 只有上坡，爬完 `i = n - 1`，如果直接 `return i == n - 1` 会返回 `True`，正确是 `False`。
- 用 `<=` 当作上坡条件：平台被当成上坡，`[1,2,2,1]` 会返回 `True`，正确是 `False`；严格不等式才对。
- `arr.length < 3` 不用单独判断：上坡与下坡都非空已经隐含了至少 3 个元素。

**追问。**
- 允许平台（非严格）：把条件改为 `<=` 与 `>=`，其他不变，但要保证至少有一个严格上升和一个严格下降。
- 最少删除几个元素使数组成为山脉（LC 1671）：需要最长递增子序列，难度明显上升。

**同模式。** LC 845 数组中的最长山脉、LC 852 山脉数组的峰顶索引、LC 1095 山脉数组中查找目标值、LC 1671 得到山形数组的最少删除次数、LC 162 寻找峰值。
