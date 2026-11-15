---
slug: maximum-number-of-balls-in-a-box
---
## Q
**LC 1742 盒子中小球的最大数量**｜Easy

编号 `lowLimit` 到 `highLimit`（`<= 10^5`）的小球放进编号等于其数位和的盒子，求球最多的盒子里有几个球。

## A
**一句话。** 计数即可；数位和用递推 `s[i] = s[i // 10] + i % 10`，每个数 `O(1)` 得到。

```python
def count_balls(low_limit, high_limit):
    s = [0] * (high_limit + 1)   # s[i]：i 的数位和
    cnt = Counter()
    for i in range(1, high_limit + 1):
        s[i] = s[i // 10] + i % 10   # 去掉末位再加回来
        if i >= low_limit:
            cnt[s[i]] += 1
    return max(cnt.values())
```

**复杂度。** 时间 `O(H)`，空间 `O(H)`（`H = highLimit`）。

**易错点。**
- 递推从 `low_limit` 开始算：`s[i // 10]` 可能小于 `low_limit` 还没算，要从 1 开始填表。
- 盒子数组开得太小：`10^5` 以内数位和最大是 `9·5 = 45`，用 `Counter` 或开 46 格都行。

**追问。**
- 范围到 `10^18`？：数位 DP，对每个可能的数位和 `t` 数 `[low, high]` 里数位和为 `t` 的数，取最大。
- 不开数组？：逐个 `sum(map(int, str(i)))`，多一个 `log` 因子，也能过。

**同模式。** LC 338 比特位计数、LC 788 旋转数字、LC 233 数字 1 的个数
