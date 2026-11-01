---
id: tlc-tops-top-k-frequent-elements-0-whole
node: arrays-hashing.top-k-frequent-elements
type: qa
---
## Q
**LC 347 前 K 个高频元素**｜Medium · 全公司热度第 16 名 · Blind 75、NeetCode 150、Hot 100

给你一个整数数组 `nums` 和一个整数 `k`，请你返回其中出现频率前 `k` 高的元素，答案可以按任意顺序返回。`1 <= nums.length <= 10^5`，`-10^4 <= nums[i] <= 10^4`，`k` 的取值范围是 `[1, 数组中不相同的元素的个数]`，题目保证答案唯一。进阶：你所设计算法的时间复杂度必须优于 `O(n log n)`。例：`nums = [1,1,1,2,2,3], k = 2` → `[1,2]`；`nums = [1], k = 1` → `[1]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 计数（`Counter`）+ 大小为 `k` 的小根堆（Top-K 模板）。

**一句话。** 先数每个元素出现的次数，再用大小为 `k` 的小根堆保留频率最高的 `k` 个：新元素比堆顶频率高就挤掉堆顶。

**识别。** 「前 `k` 个最大 / 最频繁」不要整体排序：保留 `k` 个候选的堆是 Top-K 的标准模板，`O(m log k)`（`m` 是不同元素的个数）优于 `O(n log n)`，正好满足进阶要求。`n <= 10^5`。「答案唯一」说明不用处理第 `k` 名并列。

**推导。** 数完次数后排序全部不同元素，`O(m log m)`，进阶要求更好。只要前 `k` 名，维护一个大小不超过 `k` 的小根堆：堆里是目前最高频的 `k` 个，堆顶是其中最低的；新元素频率超过堆顶才有资格进堆，每次堆操作 `O(log k)`。

```python
import heapq
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    cnt = Counter(nums)                            # 元素 -> 次数
    heap: list[tuple[int, int]] = []               # 小根堆，元素是 (次数, 元素)，堆顶是候选里最低频的
    for x, c in cnt.items():
        heapq.heappush(heap, (c, x))
        if len(heap) > k:
            heapq.heappop(heap)                    # 超过 k 个就弹出最低频的，留下的一直是目前的前 k 名
    return [x for _, x in heap]
```

运行：`([1,1,1,2,2,3], 2)` → 元素集合 `{1, 2}`（顺序任意）；`([1], 1)` → `[1]`；`([1,2,1,2,1,2,3,1,3,2], 2)` → `{1, 2}`；`([5,5,5,2,2,-1], 2)` → `{5, 2}`。

**复杂度。** 时间 `O(n + m log k)`：计数 `O(n)`，每个不同元素一次堆操作；空间 `O(m)`，计数表加 `O(k)` 的堆。

**拓展优化。**
- 桶排序，真正的 `O(n)`：次数最大是 `n`，开 `n + 1` 个桶，按次数放入，从大到小收集 `k` 个：
```python
from collections import Counter

def top_k_frequent_bucket(nums: list[int], k: int) -> list[int]:
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]   # buckets[c]：恰好出现 c 次的元素
    for x, c in Counter(nums).items():
        buckets[c].append(x)
    res: list[int] = []
    for c in range(len(nums), 0, -1):              # 次数从高到低
        res.extend(buckets[c])
        if len(res) >= k:
            return res[:k]
    return res
```
- 一行写法：`[x for x, _ in Counter(nums).most_common(k)]`，内部就是 `heapq.nlargest`，面试时要能讲出它在做什么。

**易错点。**
- 堆里按元素值而不是次数比较（例如 `heapq.nlargest(k, cnt)` 不带 `key`）：选出的是数值最大的 `k` 个元素，`([1,1,1,2,2,3], 2)` 得 `[3, 2]`，正确是 `[1, 2]`。堆元素必须以次数为第一关键字。
- 用大根堆装下全部不同元素再弹 `k` 次：`O(m log m)`，没有达到进阶要求。
- 以为 `k` 可以超过不同元素个数：题目保证 `k` 不超过它。

**同模式。** LC 215 数组中的第 K 个最大元素、LC 692 前 K 个高频单词、LC 973 最接近原点的 K 个点、LC 451 根据字符出现频率排序。
