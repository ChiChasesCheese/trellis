---
id: tlc-top-k-frequent-elements-4-followup
node: p2.top-k-frequent-elements
type: qa
step: 4
---
## Q
**LC 347 前 K 个高频元素**｜追问

面试官接着问：（1）频次相同时要按元素大小排序，并且按频次从高到低返回有序结果？（2）数据是源源不断的流，内存放不下所有不同元素？（3）`k` 远小于不同元素个数 `m` 和 `k` 接近 `m` 时，该选堆还是桶？

## A
1. **有序结果、同频按元素排序**：桶排序给不出稳定的并列顺序，改成对（频次, 元素）排序。`m` 是不同元素个数，代价 `O(m log m)`：
```python
from collections import Counter

def top_k_sorted(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    return sorted(count, key=lambda x: (-count[x], x))[:k]
```
   `[1,1,1,2,2,3]` → 前两个是 `[1, 2]`。若只要前 `k` 个有序，用 `heapq.nsmallest(k, count, key=lambda x: (-count[x], x))`，`O(m log k)`。
2. **流/内存放不下**：精确做法要存所有不同元素，放不下就退而求其次——Count-Min Sketch 估计频次，加一个大小为 `k` 的小根堆维护候选；或者 Misra-Gries / Space-Saving 算法只存 `O(k)` 个计数器，保证频率超过 `n/k` 的元素一定在其中。分布式时按元素哈希分片，每片求局部 Top-K 再归并。
3. **堆还是桶**：桶是 `O(n)` 时间 `O(n)` 空间，而且常数小，`k` 大小无关。堆是 `O(n log k)`，只在 `k` 很小时 `log k` 才接近常数，并且可以在线处理（不必先知道 `n`）。`k` 接近 `m` 时，两者都不如直接排序省事。

**Python 提醒**：`Counter.most_common(k)` 在 `k` 小于元素个数时内部调用 `heapq.nlargest`；不传 `k` 才是完整排序。并列项的顺序取决于元素第一次出现的顺序（字典有序），不要依赖它当作稳定的业务规则。
