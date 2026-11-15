---
slug: minimum-time-to-break-locks-i
---
## Q
**LC 3376 破解锁的最少时间 I**｜Medium

`n <= 8` 把锁，第 `i` 把要剑的能量至少 `strength[i]`。剑能量从 0 起每分钟加 `x`（初始 1）；开一把锁后能量清零、`x` 加 `k`。求开完所有锁的最少分钟数。

## A
**一句话。** 开锁顺序决定 `x`，状压 DP：`f[mask]` 是打开 `mask` 这些锁的最少时间，此时 `x = 1 + k·popcount(mask)`，下一把锁 `i` 要 `ceil(strength[i] / x)` 分钟。

```python
def find_minimum_time(strength, k):
    n = len(strength)
    f = [inf] * (1 << n)     # f[mask]：开完 mask 的最少时间
    f[0] = 0
    for mask in range(1 << n):
        x = 1 + k * mask.bit_count()     # 当前每分钟增量
        for i in range(n):
            if not mask >> i & 1:
                t = (strength[i] + x - 1) // x   # 向上取整
                nxt = mask | 1 << i
                f[nxt] = min(f[nxt], f[mask] + t)
    return f[-1]
```

**复杂度。** 时间 `O(2^n·n)`，空间 `O(2^n)`。

**易错点。**
- 时间写成 `strength[i] // x`：能量要「至少」达到，必须向上取整。
- 按强度排序贪心：先开弱的锁让 `x` 变大不一定最优，取整会让顺序的影响不规则。

**追问。**
- `n` 到 80？：这是 II 版，转成锁与「第几个开」的二分图最小权匹配，用费用流或匈牙利算法。
- 直接枚举排列行吗？：`8! = 40320` 也能过，但状压把相同集合的前缀合并了。

**同模式。** LC 46 全排列、LC 526 优美的排列、LC 1879 两个数组最小的异或值之和
