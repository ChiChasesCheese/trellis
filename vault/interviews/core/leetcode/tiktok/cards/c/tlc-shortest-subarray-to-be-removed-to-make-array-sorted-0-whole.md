---
id: tlc-shortest-subarray-to-be-removed-to-make-array-sorted-0-whole
node: c.shortest-subarray-to-be-removed-to-make-array-sorted
type: qa
---
## Q
**LC 1574 删除最短的子数组使剩余数组有序**｜Medium · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 1 次 · 最近 2021-04-20（国内 CodeTop）

给定整数数组 `arr`，删除一个子数组（连续的，可以为空），使得剩下的元素非递减。返回满足要求的最短子数组的长度。`1 <= arr.length <= 10^5`，`0 <= arr[i] <= 10^9`。例：`[1,2,3,10,4,2,3,5]` → `3`（删除 `[10,4,2]`，剩下 `[1,2,3,3,5]`）；`[5,4,3,2,1]` → `4`；`[1,2,3]` → `0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 保留一个非递减的前缀和一个非递减的后缀，且前缀的末尾不超过后缀的开头；双指针枚举前缀长度，后缀起点单调右移。

**识别。** 「删一段连续的，剩下的有序」等价于「保留一个有序前缀加一个有序后缀并保证拼接处有序」。前缀越长，后缀的起点越靠右，双指针单调。

**推导。** 暴力：枚举删除的区间 `[i, j)` 并检查剩余是否有序，`O(n³)`。先求最长非递减后缀的起点 `right`（若 `right == 0` 数组已有序，返回 `0`），保留它只需删除 `arr[:right]`，长度 `right`。再枚举保留前缀 `arr[:left + 1]`（前缀自身必须非递减，否则 `break`），后缀的起点必须满足 `arr[right] >= arr[left]`，所以 `right` 只增不减地右移到第一个合格位置，删除 `arr[left + 1:right]`，长度 `right - left - 1`。

```python
def find_length_of_shortest_subarray(arr: list[int]) -> int:
    n = len(arr)
    right = n - 1
    while right > 0 and arr[right - 1] <= arr[right]:    # 最长非递减后缀的起点
        right -= 1
    if right == 0:                               # 整个数组已经非递减
        return 0
    ans = right                                  # 只保留后缀：删掉 arr[:right]
    for left in range(n):                        # 保留前缀 arr[:left + 1]
        if left > 0 and arr[left - 1] > arr[left]:
            break                                # 前缀自己已经不有序，更长的前缀都不行
        while right < n and arr[right] < arr[left]:
            right += 1                           # 后缀起点右移，直到能接在 arr[left] 后面
        ans = min(ans, right - left - 1)         # 删掉 arr[left + 1:right]
    return ans
```

运行：`[1,2,3,10,4,2,3,5]` → `3`，`[5,4,3,2,1]` → `4`，`[1,2,3]` → `0`，`[1]` → `0`；`[2,2,2,1,1,1]` → `3`。

**复杂度。** 时间 `O(n)`（`left` 与 `right` 各只前进一次），空间 `O(1)`。

**拓展优化。**
- 后缀起点也可以对每个 `left` 用二分查找：`right = bisect_left(arr, arr[left], right)`，`O(n log n)`，不用依赖双指针的单调性证明，面试里更容易写对。
- 若要求删除后严格递增，把 `<=`、`<` 比较改成严格版本。

**易错点。**
- 只考虑「删除前缀」或「删除后缀」：示例 1 的最优解夹在中间，必须同时枚举前缀和后缀。
- 前缀不再非降时不 `break`：继续枚举会把一个无序前缀当作可保留的部分，`[5,0,0,5,2]` 会返回 `0`，正确是 `4`。
- `right` 走到 `n`（后缀为空）也是合法的：此时删除 `arr[left + 1:]`，长度 `n - left - 1`，不要把 `right` 限制在 `n - 1`。

**追问。**
- 返回具体删除的区间：记录取得最小值时的 `left + 1` 与 `right`。
- 要删除的是不连续元素（最长非递减子序列）：改用 LIS，`n - LIS`，复杂度 `O(n log n)`。

**同模式。** LC 209 长度最小的子数组、LC 845 数组中的最长山脉、LC 581 最短无序连续子数组、LC 300 最长递增子序列、LC 1760 袋子里最少数目的球。
