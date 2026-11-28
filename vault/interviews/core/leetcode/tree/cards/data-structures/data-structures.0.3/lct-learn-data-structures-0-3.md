---
id: lct-learn-data-structures-0-3
node: data-structures.0.3
type: qa
step: 1
---
## Q
**常用数据结构 › 常用枚举技巧 › 遍历对角线**｜学习卡

套路是什么？

## A
**一句话。** 对角线上的格子，同一条反对角线 `i + j` 相同，同一条主对角线 `i - j` 相同；按这个值分组（或直接按和遍历）就能一条条走完。

下图：格子里写的是 `i + j` 和 `i - j`；值相同的格子连成一条对角线。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<rect x="20" y="30" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="36" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="52" y="30" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="84" y="30" width="32" height="32" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="100" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="116" y="30" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="132" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="20" y="62" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="36" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="52" y="62" width="32" height="32" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="68" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="84" y="62" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="116" y="62" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="132" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="20" y="94" width="32" height="32" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="36" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="52" y="94" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="84" y="94" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="116" y="94" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="132" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="84" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">i + j（反对角线）</text>
<rect x="190" y="30" width="32" height="32" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="206" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<rect x="222" y="30" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="238" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="254" y="30" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-2</text>
<rect x="286" y="30" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="302" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-3</text>
<rect x="190" y="62" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="206" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="222" y="62" width="32" height="32" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="238" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<rect x="254" y="62" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="286" y="62" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="302" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-2</text>
<rect x="190" y="94" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="206" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="222" y="94" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="238" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="254" y="94" width="32" height="32" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="270" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<rect x="286" y="94" width="32" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="302" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<text x="254" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">i - j（主对角线）</text>
<text x="84" y="150" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i+j = 2：同一条 ↙ 线</text>
<text x="254" y="150" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i-j = 0：同一条 ↘ 线</text>
<text x="170" y="170" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一条线上的格子，这个值相同</text>
</svg>

```python
def diagonal_order(mat):
    m, n = len(mat), len(mat[0])
    res = []
    for k in range(m + n - 1):       # k = i + j，共 m+n-1 条
        lo = max(0, k - n + 1)       # i 的取值范围
        hi = min(k, m - 1)
        line = [mat[i][k - i] for i in range(lo, hi + 1)]
        if k % 2 == 0:               # 偶数条从下往上走，反向
            line.reverse()
        res += line
    return res
```

**要点。**
- 为什么对？：`i + j = k` 的格子就是一条斜线，`i` 从 `max(0, k-n+1)` 到 `min(k, m-1)` 取遍，`j = k - i` 自动落在合法范围。
- 主对角线怎么改？：用 `i - j` 分组，范围是 `-(n-1) .. m-1`，用字典或加偏移 `n - 1`。
- 要按顺序弹格子怎么改？：直接在 `i, j` 上走，撞墙时按方向换向，但分组写法更不容易错。

**易错点。**
- 方向与奇偶：LC 498 第一条（`k = 0`）向上，即 `k` 为偶数时要从下往上，列表正向收集就必须反转。
- 范围写成 `range(0, k + 1)`：`i` 超出行数或 `j` 超出列数会越界，`[[1,2,3]]` 就会出错。
- 非方阵：`m != n` 时斜线条数是 `m + n - 1`，别用 `2n - 1`。

**对应题目。** LC 498 对角线遍历
