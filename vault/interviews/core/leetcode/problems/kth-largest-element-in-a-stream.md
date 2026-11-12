---
slug: kth-largest-element-in-a-stream
---
## Q
**LC 703 数据流中的第 K 大元素**｜Easy

实现 `KthLargest(k, nums)`，`add(val)` 插入后返回当前数据流里第 `k` 大的元素（重复值各算一个）。

## A
**一句话。** 小根堆只保留最大的 `k` 个数，堆顶就是第 `k` 大。

```python
class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.h = sorted(nums)[-k:]   # 升序列表即合法最小堆

    def add(self, val):
        if len(self.h) < self.k:
            heappush(self.h, val)
        elif val > self.h[0]:
            heapreplace(self.h, val)
        return self.h[0]
```

**复杂度。** 时间 每次 `add` `O(log k)`，空间 `O(k)`。

**易错点。**
- 用大根堆保留前 `k` 大：堆顶是最大值，取第 `k` 大要弹 `k - 1` 次。
- 没处理堆未满：`KthLargest(1, [])` 对空堆读 `h[0]` 会 `IndexError`。
- 对值去重：`[7,7,7,7,8,3]` 的第 `4` 大是 `7`，去重就错。

**追问。**
- 为什么用小根堆？：堆顶是这 `k` 个里最小的，正好是第 `k` 大，且新数只需与堆顶比较。
- 还要支持删除？：用两个堆加懒删除，或有序容器。

**同模式。** LC 215 数组中的第 K 个最大元素、LC 347 前 K 个高频元素、LC 295 数据流的中位数、LC 973 最接近原点的 K 个点
