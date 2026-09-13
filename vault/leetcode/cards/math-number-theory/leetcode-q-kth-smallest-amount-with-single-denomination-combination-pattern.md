---
id: leetcode-q-kth-smallest-amount-with-single-denomination-combination-pattern
node: math-number-theory.number-theory
type: qa
anki: 1787354596706
tags: [lc::3116, leetcode, pattern, recall]
---
## Q
给定若干面值 coins，求 1~x 中能被任意一个面值整除的数的个数，如何用子集容斥原理配合二分查找求第 k 小的数？

## A
1) 预处理去冗余：若 y 整除 x，则保留 x 无意义（能被 x 整除的数集合是能被 y 整除的数集合的子集），排序后只保留不能被已保留元素整除的新面值，避免子集数爆炸。2) 对每个非空子集 mask，用增量法算 lcm[mask]：mask 去掉最低位 1 得到 pre_mask，lcm[mask] = lcm(lcm[pre_mask], 新加入的面值)，复杂度从 O(n·2^n) 降到 O(2^n)；若 lcm 超过二分上界 hi 就标记为哨兵值防止大数计算。3) count(x) = Σ_mask (-1)^(|mask|+1) · ⌊x/lcm[mask]⌋（容斥：奇数大小子集加，偶数减）。4) 二分范围 [k, coins[0]*k]（最坏情况只用最小面值），二分找最小的 x 使 count(x) >= k。

**Evidence**

```
coins.sort()
reduced = []
for x in coins:
    if all(x % y != 0 for y in reduced):
        reduced.append(x)
coins = reduced

lo, hi = k, coins[0] * k
lcm = [1] * m
for mask in range(1, m):
    pre_mask = mask & (mask - 1)
    i = (mask & -mask).bit_length() - 1
    merged = base // gcd(base, coin) * coin
    lcm[mask] = merged if merged <= hi else hi + 1

def count(x):
    total = 0
    for mask in range(1, m):
        if lcm[mask] > x: continue
        term = x // lcm[mask]
        total += term if mask.bit_count() & 1 else -term
    return total
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3116%20-%20Kth%20Smallest%20Amount%20With%20Single%20Denomination%20Combination)
