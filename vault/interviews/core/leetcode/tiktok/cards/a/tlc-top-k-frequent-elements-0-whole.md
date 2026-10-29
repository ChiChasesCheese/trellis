---
id: tlc-top-k-frequent-elements-0-whole
node: a.top-k-frequent-elements
type: qa
---
## Q
**LC 347 前 K 个高频元素**｜Medium · LC TikTok 热度 75/100（近 6 个月） · 近一年被问：美国 4 次、国内 4 次 · CodeTop 国内累计 17 次 · 最近 2026-10-17（面试记录）

给整数数组 `nums` 和整数 `k`，返回出现频率前 `k` 高的元素，可按任意顺序返回。`1 <= nums.length <= 10^5`，`-10^4 <= nums[i] <= 10^4`，`k` 的取值范围是 `[1, 数组中不相同元素的个数]`，数据保证答案唯一。例：`nums = [1,1,1,2,2,3], k = 2` → `[1,2]`；`nums = [1], k = 1` → `[1]`。进阶：时间复杂度必须优于 `O(n log n)`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先用 `Counter` 统计频次；频次最大只能是 `n`，所以按「频次」做桶排序（bucket sort），从高频桶往低频桶取，凑够 `k` 个就停。`O(n)`。

**识别。** 「前 `k` 个最大/最频繁」是 Top-K 信号：排序 `O(n log n)`，大小为 `k` 的堆 `O(n log k)`；进阶要求优于 `O(n log n)`。频次是 `1` 到 `n` 的整数，范围小，可以直接当下标做桶排序，降到 `O(n)`。

**推导。** 暴力：统计频次后整体排序，`O(n log n)` → 浪费：只要前 `k` 个，不需要全序 → 维护大小为 `k` 的小根堆，`O(n log k)` → 频次是不超过 `n` 的整数，不需要比较，直接按频次分桶（下标 = 频次），从后往前取 → `O(n)`。

```python
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]   # 下标 = 出现次数
    for x, c in count.items():
        buckets[c].append(x)
    ans: list[int] = []
    for bucket in reversed(buckets):          # 从高频到低频
        ans.extend(bucket)
        if len(ans) >= k:
            return ans[:k]
    return ans
```

运行：`([1,1,1,2,2,3], 2)` → `[1, 2]`，`([1], 1)` → `[1]`，`([1,2,1,2,1,2,3,1,3,2], 2)` → `[1, 2]`，`([4,4,5,6], 3)` → `[4, 5, 6]`。

**复杂度。** 时间 `O(n)`：统计一遍、分桶一遍、取出一遍；空间 `O(n)`：计数表和桶。

**易错点。**
- 桶数组长度必须是 `n + 1`：全是同一个数时频次等于 `n`。`[1,1,1]`、`k = 1` 若只开 `n` 个桶，访问 `buckets[3]` 会 `IndexError`。
- 「前 k 大」指频次，不是数值：`heapq.nlargest(k, count)` 不带 `key` 时按**元素值**取最大，`[1,1,1,2,2,3]`、`k = 2` 会返回 `[3, 2]`，正确是 `[1, 2]`；要写 `key=count.get`。
- 桶里同频次的元素不止一个，取够 `k` 个后要截断 `ans[:k]`。

**追问。**
- 数据流/内存放不下：用近似计数（Count-Min Sketch）加堆，或先按哈希分片再各自统计、最后合并各片的 Top-K。
- 要保持稳定顺序、或频次相同按字典序：改用 `sorted(count, key=lambda x: (-count[x], x))`，代价 `O(m log m)`，`m` 是不同元素个数。
- 只要第 `k` 高频的频次：对频次数组做快速选择（quickselect），期望 `O(m)`。

**同模式。** LC 215 数组中的第 K 个最大元素、LC 692 前 K 个高频单词、LC 973 最接近原点的 K 个点、LC 451 根据字符出现频率排序。
