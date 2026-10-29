---
id: tlc-find-two-non-overlapping-sub-arrays-each-with-target-sum-0-whole
node: a.find-two-non-overlapping-sub-arrays-each-with-target-sum
type: qa
---
## Q
**LC 1477 找两个和为目标值且不重叠的子数组**｜Medium · CodeTop 国内累计 1 次 · 最近 2026-07-15（CodeTop）

给整数数组 `arr` 和整数 `target`，找**两个互不重叠**的子数组，它们的和都等于 `target`，返回两个子数组**长度之和的最小值**；找不到返回 `-1`。`1 <= arr.length <= 10^5`，`1 <= arr[i] <= 1000`，`1 <= target <= 10^8`。例：`arr = [3,2,2,4,3]`，`target = 3` → `2`（`[3]` 和 `[3]`）；`arr = [7,3,4,7]`，`target = 7` → `2`；`arr = [4,3,2,6,2,3,4]`，`target = 6` → `-1`；`arr = [3,1,1,1,5,1,2,1]`，`target = 3` → `3`（`[1,2]` 与 `[2,1]` 重叠，不能同时选）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 元素全为正，所以「和为 `target` 的子数组」可用滑动窗口在 `O(n)` 内逐个找出；扫描时用 `best[i]` 记录 `arr[:i]` 里已出现的**最短**目标子数组长度，每找到一个以 `right` 结尾的目标子数组，就和 `best[left]`（完全在它左边的最短者）配对更新答案。`O(n)`。

**识别。** 「子数组和 = target」+ 元素全为正 → 滑动窗口（和随窗口扩大单调增）或前缀和 + 哈希；「两个**不重叠**」→ 把区间一分为二：以当前子数组为右段，左段只能来自它左端之前，用「前缀最优值」`best[left]` 表示；`n = 10^5` 要 `O(n)`。

**推导。** 暴力：枚举所有和为 `target` 的子数组（最多 `O(n^2)` 个），再两两检查不重叠，更慢。浪费：只有「最短」的才有用——对每个目标子数组，左边只需要一个**最短**的合法搭档。洞察：元素为正时，以 `right` 结尾的目标子数组至多一个；于是顺序扫描，维护前缀最优值 `best[i]`（`arr[:i]` 内最短目标子数组长度），每找到 `[left, right]`，答案候选是 `best[left] + 长度`，同时更新 `best[right + 1]`。最优：一次滑动窗口 `O(n)` 完成。

```python
def min_sum_of_lengths(arr: list[int], target: int) -> int:
    n = len(arr)
    INF = n + 1                                  # 任何真实答案都 <= n
    best = [INF] * (n + 1)                       # best[i]：arr[:i] 里和为 target 的最短子数组长度
    ans = INF
    left = window = 0                            # 窗口 arr[left..right]，元素全为正所以可以收缩
    for right, x in enumerate(arr):
        window += x
        while window > target:
            window -= arr[left]
            left += 1
        best[right + 1] = best[right]
        if window == target:
            length = right - left + 1
            ans = min(ans, best[left] + length)  # 前一段必须完全在 left 之前
            best[right + 1] = min(best[right + 1], length)
    return -1 if ans == INF else ans
```

运行：`[3,2,2,4,3], 3` → `2`，`[7,3,4,7], 7` → `2`，`[4,3,2,6,2,3,4], 6` → `-1`，`[5,5,4,4,5], 3` → `-1`，`[3,1,1,1,5,1,2,1], 3` → `3`，`[1,2,1], 3` → `-1`。

**复杂度。** 时间 `O(n)`：窗口两端各只前进 `n` 步；空间 `O(n)`（`best` 数组）。

**易错点。**
- 忽略不重叠，直接取两个最短目标子数组之和：`[1,2,1]`，`target = 3`，`[1,2]` 和 `[2,1]` 都是目标子数组，长度和 `4`，但它们重叠，正确答案是 `-1`。必须用 `best[left]`（完全在当前子数组左边）配对。
- 用 `best[right]` 或 `best[right + 1]` 配对：会把当前子数组自己（或重叠部分）当成搭档。`best[left]` 才是严格位于 `left` 之前的前缀。
- 哨兵取 `inf` 浮点数再 `return`：答案类型变成 `float`；用整数哨兵 `n + 1`（真实答案不超过 `n`）更干净，返回前判断 `== INF`。

**追问。**
- 元素可以是负数或零（滑动窗口失效）：改用前缀和 + 哈希表（记录某前缀和最近出现的下标），其余不变。
- 要选 `k` 个互不重叠的子数组（`k` 大于 2）：状态变成 `dp[j][i]`（选 `j` 段、看前 `i` 个），完整二维表。
- 返回两个子数组的位置：`best` 里额外存最短者的起止下标。

**同模式。** LC 560 和为 K 的子数组、LC 209 长度最小的子数组、LC 1031 两个非重叠子数组的最大和、LC 2054 两个最好的不重叠活动、LC 1235 规划兼职工作。
