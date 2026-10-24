---
id: tlc-kth-largest-element-in-an-array-4-followup
node: a.kth-largest-element-in-an-array
type: qa
step: 4
---
## Q
**LC 215 数组中的第 K 个最大元素**｜追问

面试官接着问：（1）值域只有 `[-10^4, 10^4]`，有没有确定性的线性解？（2）数据是持续到来的流，随时要报告当前第 `k` 大？（3）要 `O(1)` 额外空间原地做？

## A
1. **值域小 → 计数数组**：统计每个值出现的次数，从最大值往小累减 `k`，减到 `<= 0` 的那个值就是答案。时间 `O(n + 值域)`，空间 `O(值域)`，没有随机性。
```python
def kth_largest_count(nums: list[int], k: int) -> int:
    cnt = [0] * 20001                     # 下标 = 值 + 10000
    for x in nums:
        cnt[x + 10000] += 1
    for v in range(20000, -1, -1):
        k -= cnt[v]
        if k <= 0:
            return v - 10000
    raise ValueError("k out of range")
```
2. **数据流**：大小为 `k` 的小根堆，堆顶即第 `k` 大。每来一个元素，堆没满就 `heappush`，满了就 `heappushpop`（先入后出，比 push 再 pop 少一次调整），`O(log k)`。快速选择不适合在线场景，因为每次查询都要重新划分。
```python
import heapq

def kth_largest_heap(nums: list[int], k: int) -> int:
    heap: list[int] = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        else:
            heapq.heappushpop(heap, x)
    return heap[0]
```
3. **原地 `O(1)` 空间**：用 Lomuto 或 Hoare 划分在原数组上交换元素，循环维护 `[lo, hi]` 区间，目标排名换算成升序下标 `n - k`。注意原地版会打乱调用方的数组，也需要三路划分（Dutch flag）才能处理大量重复值。

**Python 提醒**：`heapq` 只有小根堆。求第 `k` **大**用大小为 `k` 的小根堆（堆顶是其中最小的，也就是第 `k` 大）；求第 `k` **小**才需要把值取负数放进去模拟大根堆。`heapq.nlargest(k, nums)[-1]` 也能得到答案，内部是同样的 `O(n log k)`。
