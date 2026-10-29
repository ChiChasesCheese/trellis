---
id: uth-gaps-dp-join-order-2-bushy
node: gaps.dp-join-order
type: qa
step: 2
---
## Q
**连接树不一定是一条直线**｜PostgreSQL · 17

四张表可以 `((1⋈2)⋈3)⋈4` 一路接下去，也可以 `(1⋈2)⋈(3⋈4)` 两边各自拼好再合。PostgreSQL 的逐层 DP 每一层怎样把这些拼法都考虑到？

## A
**结构。** 每一层先试「上一层的结果 + 一张单表」（单表放在内侧或外侧两个方向），再试「两个较小的结果拼在一起」，后者叫浓密树（bushy plan）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 198">
<text x="85" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">直线式</text>
<text x="255" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">浓密树 (bushy)</text>
<line x1="85" y1="48" x2="55" y2="70" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="85" y1="48" x2="115" y2="70" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="55" y1="90" x2="30" y2="112" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="55" y1="90" x2="80" y2="112" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="30" y1="132" x2="15" y2="154" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="30" y1="132" x2="45" y2="154" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<rect x="72" y="28" width="26" height="20" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="85" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">连</text>
<rect x="42" y="70" width="26" height="20" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="55" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">连</text>
<rect x="102" y="70" width="26" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">4</text>
<rect x="17" y="112" width="26" height="20" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="30" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">连</text>
<rect x="67" y="112" width="26" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">3</text>
<rect x="2" y="154" width="26" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="15" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<rect x="32" y="154" width="26" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="45" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">2</text>
<line x1="255" y1="48" x2="220" y2="80" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="255" y1="48" x2="290" y2="80" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="220" y1="100" x2="205" y2="132" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="220" y1="100" x2="235" y2="132" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="290" y1="100" x2="275" y2="132" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="290" y1="100" x2="305" y2="132" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<rect x="242" y="28" width="26" height="20" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">连</text>
<rect x="207" y="80" width="26" height="20" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="220" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">连</text>
<rect x="277" y="80" width="26" height="20" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="290" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">连</text>
<rect x="192" y="132" width="26" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="205" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<rect x="222" y="132" width="26" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">2</text>
<rect x="262" y="132" width="26" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="275" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">3</text>
<rect x="292" y="132" width="26" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="305" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">4</text>
<text x="170" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">同一层 两种拼法都要比成本</text>
</svg>
```

**细节。**

- 凑 `{1 2 3 4}` 时，既能 `{1 2 3}` 并 `{4}`，也能 `{1 2}` 并 `{3 4}`
- 浓密树只在两边之间有连接条件时才试：源码注释说，这是为了避免规划时间增长失控
- 一张表和谁都没有连接条件，才会退而求其次去试笛卡尔积

**为什么。** 只看直线会错过「两边先各自缩小再合」的便宜方案；无条件地试所有浓密树又太慢，所以限定在有条件的组合上。

**例题：** LC 312 戳气球

`n` 个气球，戳破第 `i` 个得 `nums[i-1] * nums[i] * nums[i+1]` 枚硬币（越界当作 1）。求戳破所有气球最多得多少硬币。这里也是把区间切成左右两段、各自求最优再合并。`1 <= n <= 300`。

```python
def max_coins(nums):
    a = [1] + nums + [1]                      # virtual balloons at both ends
    n = len(a)
    dp = [[0] * n for _ in range(n)]          # dp[l][r]: best coins bursting everything strictly between l and r
    for length in range(2, n):                # widen the open interval (l, r)
        for l in range(n - length):
            r = l + length
            for k in range(l + 1, r):         # k is the LAST one burst: its neighbours are l and r
                dp[l][r] = max(dp[l][r], dp[l][k] + a[l] * a[k] * a[r] + dp[k][r])
    return dp[0][n - 1]
```
