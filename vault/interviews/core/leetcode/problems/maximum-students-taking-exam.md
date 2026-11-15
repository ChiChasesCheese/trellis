---
slug: maximum-students-taking-exam
---
## Q
**LC 1349 参加考试的最大学生数**｜Hard

`m × n`（都 `<= 8`）座位表，`'#'` 坏座、`'.'` 好座。学生能看到左、右、左前、右前紧邻同学的答卷（正前方看不到）。求最多坐多少人且无人能作弊。

## A
**一句话。** 按行状压 DP：`f[i][mask]` 是前 `i` 行、第 `i` 行坐法为 `mask` 的最多人数；行内不能相邻，与上一行 `pre` 不能错开一位，即 `mask & (pre<<1)` 与 `mask & (pre>>1)` 都为 0。

**图解。** 前排第 2 列坐了人，本排第 1、3 列就看得到他，正后方第 2 列可以坐。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 126">
<text x="42" y="30.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">前排</text>
<rect x="50" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="80" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="110" y="12" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="125.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">●</text>
<rect x="140" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="42" y="64.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">本排</text>
<rect x="50" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="80" y="46" width="30" height="30" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="95.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">×</text>
<rect x="110" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="125.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">✓</text>
<rect x="140" y="46" width="30" height="30" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="155.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">×</text>
<rect x="170" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="16" y="90" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">× 处坐人能看到前排斜方</text>
<text x="16" y="108" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">mask & (pre<<1) 与 mask & (pre>>1) 都要为 0</text>
</svg>

```python
def max_students(seats):
    m, n = len(seats), len(seats[0])
    good = [sum(1 << j for j, c in enumerate(row)
                if c == ".") for row in seats]
    # f[i][mask]：前 i 行，第 i 行坐法为 mask 的最多人数
    f = [[-inf] * (1 << n) for _ in range(m + 1)]
    f[0][0] = 0
    for i in range(m):
        for mask in range(1 << n):
            if mask & ~good[i] or mask & (mask >> 1):
                continue        # 坐坏座位或左右相邻
            for pre in range(1 << n):
                if mask & (pre << 1) or mask & (pre >> 1):
                    continue    # 看得到前排斜方
                cand = f[i][pre] + mask.bit_count()
                f[i + 1][mask] = max(f[i + 1][mask], cand)
    return max(f[m])
```

**复杂度。** 时间 `O(m·4^n)`，空间 `O(m·2^n)`。

**易错点。**
- 把正前方也算冲突：题目说看不到前后，只限制左前、右前。
- 行内只检查坏座：同一行左右相邻也能看到，要 `mask & (mask >> 1) == 0`。

**追问。**
- 怎么加速？：先列出每行的合法 `mask`（行内不相邻的只有约 `55` 个），只在合法集合之间转移。
- 另一种思路？：把座位按列奇偶分成二分图，冲突连边，答案是好座位数减最大匹配。

**同模式。** LC 51 N 皇后、LC 1411 给 N x 3 网格图涂色的方案数、LC 1931 用三种不同颜色为网格涂色
