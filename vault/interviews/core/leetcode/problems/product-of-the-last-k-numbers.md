---
slug: product-of-the-last-k-numbers
---
## Q
**LC 1352 最后 K 个数的乘积**｜Medium

设计 `ProductOfNumbers`：`add(num)` 追加一个数，`getProduct(k)` 返回最后 `k` 个数的乘积，要求都是 `O(1)`。

## A
**一句话。** 维护前缀积，最后 `k` 个的乘积是两个前缀积相除，遇到 `0` 就清空重来。

```python
class ProductOfNumbers:
    def __init__(self):
        self.pre = [1]         # 最近一个 0 之后的前缀积

    def add(self, num):
        if num == 0:
            self.pre = [1]     # 之前的前缀作废
        else:
            self.pre.append(self.pre[-1] * num)

    def getProduct(self, k):
        if k >= len(self.pre):  # 跨过了最近的 0
            return 0
        return self.pre[-1] // self.pre[-1 - k]
```

**复杂度。** 时间 每次 `O(1)`，空间 `O(n)`。

**易错点。**
- 遇到 `0` 不清空：之后前缀全是 `0`，查询时 `0 // 0` 抛 `ZeroDivisionError`。
- 条件写成 `k > len(pre)`：`pre` 带哨兵 `1`，`k == len(pre)` 时下标越界。
- 用 `/` 代替 `//`：返回浮点数，大数还丢精度。

**追问。**
- `k` 有上限、想省内存？：只留最近 `K+1` 个前缀积，用 `deque(maxlen=K+1)`，另记一个 `0` 之后的个数。

**同模式。** LC 303 区域和检索、LC 238 除自身以外数组的乘积、LC 560 和为 K 的子数组、LC 713 乘积小于 K 的子数组
