---
slug: maximum-tastiness-of-candy-basket
---
## Q
**LC 2517 礼盒的最大甜蜜度**｜Medium

`price[i]` 是第 `i` 种糖果的价格。从中选出 `k` 种做礼盒，礼盒的甜蜜度是其中任意两种糖果价格差的绝对值的最小值。求最大甜蜜度。

## A
**一句话。** 二分答案 `d`：价格排序后，贪心地每次选第一个与上一个相差至少 `d` 的糖果，能选够 `k` 个就说明 `d` 可行；可行性随 `d` 增大而单调变差。

```python
def maximum_tastiness(price, k):
    price.sort()
    def ok(d):                   # 能否选出 k 个，相邻差都 >= d
        cnt, last = 1, price[0]
        for p in price:
            if p - last >= d:
                cnt += 1
                last = p         # 贪心：越早选越好
        return cnt >= k
    lo, hi = 0, (price[-1] - price[0]) // (k - 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2      # 上取整，防死循环
        if ok(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
```

**复杂度。** 时间 `O(n log n + n log V)`，空间 `O(1)`（不计排序）。

**易错点。**
- 求最大值的二分用了下取整：`lo = mid` 会死循环，必须 `mid = (lo + hi + 1) // 2`。
- 贪心时不先选最小价格：从最小的开始选，才能留给后面最多的余地。
- 上界取 `price[-1] - price[0]`：`k` 个糖果平均间隔不超过 `(max - min) / (k - 1)`，更紧也可以。

**追问。**
- 为什么只检查相邻差？：排序后最小的两两差一定出现在相邻选中的两个之间。
- 二分判定的套路？：「最大化最小值」是经典的二分答案加贪心验证，LC 1552、LC 410 同类。

**同模式。** LC 1552 两球之间的磁力、LC 410 分割数组的最大值、LC 1011 在 D 天内送达包裹的能力
