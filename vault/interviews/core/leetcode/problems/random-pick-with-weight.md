---
slug: random-pick-with-weight
---
## Q
**LC 528 按权重随机选择**｜Medium

给正整数数组 `w`，实现 `pickIndex()`，返回下标 `i` 的概率是 `w[i] / sum(w)`。

## A
**一句话。** 前缀和把权重铺成数轴，均匀取一个整数，再二分查它落在哪一段。

```python
class Solution:
    def __init__(self, w):
        self.prefix = list(accumulate(w))
        self.total = self.prefix[-1]

    def pickIndex(self):
        r = random.randrange(self.total)   # [0, total)
        return bisect_right(self.prefix, r)  # 首个 > r
```

**复杂度。** 时间 构造 `O(n)`，抽取 `O(log n)`，空间 `O(n)`。

**易错点。**
- `randrange(total)` 配 `bisect_left`：`w=[1,3]` 时下标 `0` 的概率变成 `2/4`，应为 `1/4`。
- `randint` 两端都含、`randrange` 不含上界，混用就差一位。
- 每次抽取都重新 `accumulate`：变成 `O(n)`，前缀和只在构造时算一次。

**追问。**
- 权重会动态更新？：树状数组维护前缀和，更新和抽取都是 `O(log n)`。
- 要 `O(1)` 抽取？：别名法（alias method），构造 `O(n)`，不支持更新。

**同模式。** LC 497 非重叠矩形中的随机点、LC 710 黑名单中的随机数、LC 398 随机数索引、LC 382 链表随机节点
