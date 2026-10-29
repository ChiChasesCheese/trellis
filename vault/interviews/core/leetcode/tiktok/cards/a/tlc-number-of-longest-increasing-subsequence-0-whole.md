---
id: tlc-number-of-longest-increasing-subsequence-0-whole
node: a.number-of-longest-increasing-subsequence
type: qa
---
## Q
**LC 673 最长递增子序列的个数**｜Medium · CodeTop 国内累计 13 次 · 最近 2026-04-09（CodeTop）

给未排序的整数数组 `nums`，返回**最长严格递增子序列的个数**（子序列不要求连续）。`1 <= nums.length <= 2000`，`-10^6 <= nums[i] <= 10^6`。例：`[1,3,5,4,7]` → `2`（`[1,3,4,7]` 和 `[1,3,5,7]`），`[2,2,2,2,2]` → `5`（最长长度是 1，共有 5 个）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 在最长递增子序列（LIS）的 `O(n^2)` 动态规划上多带一个数组：`length[i]` 是以 `nums[i]` 结尾的最长长度，`count[i]` 是达到该长度的方案数；找到更长的就**覆盖**计数，一样长就**累加**；最后把所有 `length` 等于全局最长的位置的 `count` 加起来。

**识别。** 「子序列（不连续）」+「严格递增」+「最长」是以每个位置结尾的一维 DP；「求个数」说明状态要同时记方案数（counting DP）。`n <= 2000` 是给 `O(n^2)` 开的绿灯（约 `2 * 10^6` 次比较），不需要 `O(n log n)`。

**推导。** 暴力：枚举 `2^n` 个子序列，筛出递增的，统计最长者的个数，`O(2^n * n)`。浪费：许多子序列共享同一个前缀。以 `i` 结尾的递增子序列，去掉最后一个元素后，就是以某个 `j < i`（`nums[j] < nums[i]`）结尾的递增子序列，所以 `length[i] = 1 + max(length[j])`。要数个数：以 `i` 结尾的最长子序列，去掉末尾后一定是以 `j` 结尾的**最长**子序列（长度恰为 `length[i] - 1`），所以 `count[i]` 是这些 `j` 的 `count[j]` 之和。最长序列可以在任何位置结尾，所以答案是所有 `length[i] == 最长` 的 `count[i]` 之和，而不是 `count[-1]`。

```python
def find_number_of_lis(nums: list[int]) -> int:
    n = len(nums)
    length = [1] * n                 # length[i]：以 nums[i] 结尾的最长递增子序列长度
    count = [1] * n                  # count[i]：达到这个长度的子序列个数
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:        # 找到更长的：计数改成 j 的计数
                    length[i], count[i] = length[j] + 1, count[j]
                elif length[j] + 1 == length[i]:     # 一样长的另一种来源：累加
                    count[i] += count[j]
    longest = max(length)
    return sum(c for l, c in zip(length, count) if l == longest)
```

运行：`[1,3,5,4,7]` → `2`，`[2,2,2,2,2]` → `5`，`[1]` → `1`，`[1,2,3,4,5]` → `1`，`[5,4,3,2,1]` → `5`。

**复杂度。** 时间 `O(n^2)`：两层循环，`n = 2000` 约 `2 * 10^6` 次内层比较；空间 `O(n)`：两个长度为 `n` 的数组。

**易错点。**
- 更长时必须**覆盖**计数（`count[i] = count[j]`）。写成 `count[i] += count[j]` 会带上旧计数，`[1,3,5,4,7]` 得到 `12`（正确 `2`）。
- 答案不是 `count[-1]`，也不是第一个最长位置的计数：`[2,2,2,2,2]` 取第一个最长位置只得 `1`（正确 `5`）。
- 「严格」递增用 `<`。写成 `<=` 会把相等元素也串起来，`[2,2,2,2,2]` 得到 `1`（正确 `5`）。

**追问。**
- 只求长度（LC 300）：去掉 `count`；或用 `tails` 数组加 `bisect_left`，`O(n log n)`。
- 个数也做到 `O(n log n)`：按长度分层，每层按结尾值维护方案数的前缀和，用 `bisect` 查询；或用树状数组（Fenwick tree）。
- 返回其中一个最长子序列：多存一个 `prev[i]` 回溯；要返回全部，个数可能是指数级，只能回溯输出。

**同模式。** LC 300 最长递增子序列、LC 646 最长数对链、LC 354 俄罗斯套娃信封问题、LC 376 摆动序列。
