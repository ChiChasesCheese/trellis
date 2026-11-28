---
id: lct-learn-dp-9-1
node: dp.9.1
type: qa
step: 1
---
## Q
**动态规划 › 状态压缩 DP（状压 DP） › 排列型状压 DP ① 相邻无关**｜学习卡

套路是什么？

## A
**一句话。** 排列型状压 DP：用二进制集合 `S` 记录「已经填过的元素」，已填个数就是当前位置；枚举这一位填哪个没用过的元素，从 `f[S]` 转移到 `f[S | 1 << j]`，把 `O(n!)` 降到 `O(n * 2^n)`。

下图：集合 `S` 记录用过哪些数，个数就是当前位置；每次往 `S` 里加一个没用过的数。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="20" y="60" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="31" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="42" y="60" width="22" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="53" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="64" y="60" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="75" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="86" y="60" width="22" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="97" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<text x="20" y="50" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">S：已用数 {1, 3}</text>
<text x="20" y="104" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已用 2 个 → 填第 3 位</text>
<rect x="220" y="20" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="231" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="242" y="20" width="22" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="253" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="264" y="20" width="22" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="275" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="286" y="20" width="22" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="297" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="220" y="100" width="22" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="231" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="242" y="100" width="22" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="253" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="264" y="100" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="275" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="286" y="100" width="22" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="297" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<line x1="112" y1="66" x2="214" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="214.0,34.0 208.9,38.7 207.1,33.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="112" y1="80" x2="214" y2="110" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="214.0,110.0 207.1,111.1 208.8,105.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="150" y="40" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">放 2</text>
<text x="150" y="112" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">放 4</text>
<text x="170" y="144" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">f[S | 1 &lt;&lt; j] += f[S]：n! 个排列压成 2^n 个集合</text>
</svg>

```python
def count_arrangement(n):            # LC 526 优美的排列
    f = [0] * (1 << n)               # f[S]：已用数集合为 S 的方案数
    f[0] = 1
    for S in range(1 << n):
        i = S.bit_count() + 1        # 现在要填第 i 个位置
        for j in range(n):           # 试着放数 j + 1
            if S >> j & 1:
                continue             # 已用过
            if (j + 1) % i == 0 or i % (j + 1) == 0:
                f[S | 1 << j] += f[S]
    return f[-1]
```

**要点。**
- 为什么对？：位置按顺序填，只关心「哪些数已用」，而不是它们的顺序；不同顺序到达同一集合 `S` 的后续可能完全一样，所以合并成一个状态。
- 定义成「还能选的集合」怎么改？：从全集往下走，`f[S]` 表示剩下集合 `S` 时的最优值，位置序号由 `n - popcount(S)` 得出。
- 求最优值怎么改？：`f[S | 1 << j] = min(f[S | 1 << j], f[S] + cost)`，初值 `inf`，起点 `f[0]` 为 `0`。

**易错点。**
- 位置漏了加一：`i = S.bit_count()` 在 `S = 0` 时为 `0`，`% i` 会除零；题目位置从 `1` 起算。
- 忘了判断 `S >> j & 1`：同一个数会被填多次。
- 遍历顺序：`S | 1 << j` 总比 `S` 大，所以 `S` 升序遍历就是合法的转移顺序，不用倒序。

**对应题目。** LC 526 优美的排列
