---
id: tlc-kth-largest-element-in-an-array-0-whole
node: a.kth-largest-element-in-an-array
type: qa
---
## Q
**LC 215 数组中的第 K 个最大元素**｜Medium · LC TikTok 热度 63/100（近 6 个月） · 近一年被问：美国 4 次、国内 4 次 · CodeTop 国内累计 206 次 · 最近 2026-10-26（CodeTop）

给整数数组 `nums` 和整数 `k`，返回数组**排序后**的第 `k` 个最大元素（不是第 `k` 个不同的元素）。必须设计并实现时间复杂度为 `O(n)` 的算法。`1 <= k <= nums.length <= 10^5`，`-10^4 <= nums[i] <= 10^4`。例：`nums = [3,2,1,5,6,4], k = 2` → `5`；`nums = [3,2,3,1,2,4,5,5,6], k = 4` → `4`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 快速选择（quickselect）：随机选 pivot，三路划分成「大于 / 等于 / 小于」三堆，只钻进答案所在的那一堆，另外两堆整个丢掉。期望 `O(n)`。

**识别。** 「第 `k` 大」且题面明确要求 `O(n)`：排序 `O(n log n)` 和大小为 `k` 的堆 `O(n log k)` 都不达标，只有选择算法（selection）能做到。「第 `k` 大，不是第 `k` 个不同元素」说明有重复值，划分要处理相等的元素。

**推导。** 暴力排序取 `nums[-k]`，`O(n log n)` → 浪费：只要一个位置的元素，却排好了全部 → 快速排序每轮划分后，第 `k` 大一定落在三堆中的某一堆，只处理那一堆；每轮期望砍掉一半，总代价 `n + n/2 + n/4 + ... = O(n)` → 随机 pivot 避免被构造的输入退化成 `O(n^2)`；三路划分让大量重复值（比如全相同）一轮结束。

```python
import random

def find_kth_largest(nums: list[int], k: int) -> int:
    while True:
        pivot = random.choice(nums)
        bigger = [x for x in nums if x > pivot]
        equal = nums.count(pivot)
        if k <= len(bigger):                       # 答案在比 pivot 大的那一堆里
            nums = bigger
        elif k <= len(bigger) + equal:             # 落在 pivot 自己这一段
            return pivot
        else:                                      # 答案在比 pivot 小的那一堆里
            k -= len(bigger) + equal
            nums = [x for x in nums if x < pivot]
```

运行：`([3,2,1,5,6,4], 2)` → `5`，`([3,2,3,1,2,4,5,5,6], 4)` → `4`，`([7], 1)` → `7`，`([2,2,2], 3)` → `2`。

**复杂度。** 期望时间 `O(n)`，最坏 `O(n^2)`（概率极小）；空间 `O(n)`（列表推导复制）。

**易错点。**
- 重复值必须单独成「等于」一段：只分两堆（`>` 和 `<=`）时，全是相同元素的数组每轮只能排除一个元素，退化成 `O(n^2)`；三路划分一轮就返回。
- `k` 在进入「小于」那一堆时要减去 `len(bigger) + equal`，漏减会越界或返回错值，例如 `[3,2,1]`、`k = 3`：pivot 取 `2` 时，`bigger = [3]`、`equal = 1`，进入小堆的 `k` 应是 `1`，答案 `1`。
- 不要固定取第一个元素当 pivot：已排序的输入会让每轮只砍掉一个元素。

**追问。**
- 值域只有 `[-10^4, 10^4]`：计数数组，从大到小累减 `k`，`O(n + 值域)`，确定性线性。
- 数据流里持续维护第 `k` 大：大小为 `k` 的小根堆，堆顶就是答案，每个新元素 `heappushpop` 一次，`O(log k)`。
- 要求 `O(1)` 额外空间：原地划分（Hoare / Lomuto），把列表推导换成下标交换。

**同模式。** LC 347 前 K 个高频元素、LC 973 最接近原点的 K 个点、LC 703 数据流中的第 K 大元素、LC 295 数据流的中位数。
