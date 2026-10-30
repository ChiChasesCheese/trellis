---
id: tlc-find-k-th-smallest-pair-distance-0-whole
node: b.find-k-th-smallest-pair-distance
type: qa
---
## Q
**LC 719 找出第 k 小的距离对**｜Hard · CodeTop 国内累计 2 次 · 最近 2025-11-18（国内 CodeTop）

数对 `(a, b)` 的距离定义为 `|a - b|`。给整数数组 `nums` 和整数 `k`，数对由 `nums[i]` 和 `nums[j]` 组成且 `0 <= i < j < nums.length`，返回所有数对距离中第 `k` 小的距离。`n == nums.length`，`2 <= n <= 10^4`，`0 <= nums[i] <= 10^6`，`1 <= k <= n * (n - 1) / 2`。例：`nums = [1,3,1]`，`k = 1` → `0`（数对距离是 `2, 0, 2`）；`nums = [1,1,1]`，`k = 2` → `0`；`nums = [1,6,1]`，`k = 3` → `5`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 对「距离值」做二分（binary search on answer）：排序后，距离 `<= d` 的数对个数 `count(d)` 可以用双指针 `O(n)` 数出，且随 `d` 单调不减；找最小的 `d` 使 `count(d) >= k`，它就是第 `k` 小的距离。`O(n log n + n log(max - min))`。

**识别。** 「第 `k` 小」+「候选是 `n^2` 个隐式数对」+ 值域不大（距离在 `[0, 10^6]`）：不要枚举数对，而是**猜一个距离 `d`，数有多少对不超过它**。`n = 10^4` 时数对约 `5 * 10^7`，排序全部数对放不下也太慢；数对数可以快速计数，这是「二分答案」的标志。

**推导。** 暴力：生成所有数对距离再排序取第 `k` 个，`O(n^2 log n)` 时间 `O(n^2)` 空间 → 浪费在把全部距离排序，而我们只要一个名次 → 名次可以换成计数：`count(d)` 单调不减，第 `k` 小的距离 `v` 满足 `count(v) >= k` 且 `count(v - 1) < k` → 排序后 `x - nums[left] > d` 时 `left` 只右移不回退，对每个右端点 `right`，合法的左端点有 `right - left` 个，`count(d)` 一趟 `O(n)` → 在 `[0, max - min]` 上二分，约 `20` 轮。

```python
def smallest_distance_pair(nums: list[int], k: int) -> int:
    nums = sorted(nums)

    def count_at_most(d: int) -> int:           # 距离 <= d 的数对个数（双指针，O(n)）
        count = left = 0
        for right, x in enumerate(nums):
            while x - nums[left] > d:           # 窗口里最小的数离 x 太远：左端右移
                left += 1
            count += right - left               # 以 right 为右端点的合法数对：left..right-1
        return count

    lo, hi = 0, nums[-1] - nums[0]              # 答案一定落在 [0, 最大差] 里
    while lo < hi:                              # 二分"最小的 d，使得 count_at_most(d) >= k"
        mid = (lo + hi) // 2
        if count_at_most(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

运行：`[1,3,1]`、`k = 1` → `0`；`[1,1,1]`、`k = 2` → `0`；`[1,6,1]`、`k = 3` → `5`；`[5,5]`、`k = 1` → `0`；`[0,1000000]`、`k = 1` → `1000000`；`10^4` 个范围 `0..10^6` 的随机数、`k` 取最大值也能瞬间算完。

**复杂度。** 时间 `O(n log n)`（排序）+ `O(n log V)`（二分约 `log2(10^6) = 20` 轮，每轮 `O(n)`），`V = max - min`；空间 `O(n)`（排序后的拷贝）。

**易错点。**
- 忘了先排序：双指针计数要求数组有序，`[2,6,2,4]`、`k = 4` 得到 `4`，正确是 `2`。
- 把条件写成 `count(mid) > k`：找的是第一个「个数 `>= k`」的 `d`，写成 `>` 会多走一步，`[2,7,8]`、`k = 1` 得到 `5`，正确是 `1`。
- 二分下界写成 `1`：距离可以是 `0`，`[1,1,1]`、`k = 2` 得到 `1`，正确是 `0`。

**追问。**
- `k` 很小：用最小堆做多路归并，每个 `i` 对应一条递增序列 `nums[j] - nums[i]`，弹 `k` 次，`O((n + k) log n)`，见另一种解法。
- 返回具体的数对：求出距离 `d` 后，对每个 `x` 用 `bisect_left` 找 `x - d`。
- 同样的「值域二分 + 计数」模板还能做 LC 378 有序矩阵中第 K 小的元素、LC 668 乘法表中第 k 小的数。

**同模式。** LC 378 有序矩阵中第 K 小的元素、LC 668 乘法表中第 k 小的数、LC 410 分割数组的最大值、LC 875 爱吃香蕉的珂珂、LC 1011 在 D 天内送达包裹的能力。
