---
slug: maximum-number-of-alloys
---
## Q
**LC 2861 最大合金数**｜Medium

`k` 台机器，第 `i` 台造一份合金要 `composition[i][j]` 份金属 `j`；库存 `stock[j]`，补买一份花 `cost[j]`，预算 `budget`。所有合金必须由同一台机器造，求最多造几份。

## A
**一句话。** 枚举机器，对每台二分答案：造 `c` 份的花费随 `c` 单调增，找花费不超预算的最大 `c`。

```python
def max_number_of_alloys(n, k, budget, composition,
                         stock, cost):
    def can(comp, c):           # 这台机器造 c 份，钱够吗
        need = 0
        for a, s, p in zip(comp, stock, cost):
            need += max(0, a * c - s) * p
        return need <= budget

    ans = 0
    for comp in composition:
        lo, hi = ans, min(stock) + budget   # 只找比 ans 大的
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can(comp, mid):
                lo = mid
            else:
                hi = mid - 1
        ans = lo
    return ans
```

**复杂度。** 时间 `O(k·n·log U)`（`U = min(stock)+budget`），空间 `O(1)`。

**易错点。**
- 花费写成 `a*c*p - s`：库存抵的是份数，要先 `max(0, a*c - s)` 再乘单价。
- 求最大值时 `mid` 向下取整：`lo = mid` 会死循环，要 `(lo + hi + 1) // 2`。

**追问。**
- 上界怎么定？：每种金属至少用 1 份、单价至少 1，造 `c` 份要花 `c - stock[j]`，所以 `c <= min(stock) + budget`。
- 能多台机器混用？：就不是逐台二分了，变成整数规划，这里的单调性只对一台机器成立。

**同模式。** LC 875 爱吃香蕉的珂珂、LC 1011 在 D 天内送达包裹的能力、LC 2141 同时运行 N 台电脑的最长时间
