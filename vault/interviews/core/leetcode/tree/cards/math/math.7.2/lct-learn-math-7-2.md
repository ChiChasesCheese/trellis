---
id: lct-learn-math-7-2
node: math.7.2
type: qa
step: 1
---
## Q
**数学算法 › 杂项 › 整数拆分**｜学习卡

套路是什么？

## A
**一句话。** 整数拆分：切下第一块 `j`，剩下的 `i - j` 要么不再拆，要么按 `dp` 继续拆，取乘积最大；数学上尽量拆成 `3`。

下图：切下第一块 `j`，剩下的部分要么不拆、要么按 `dp` 继续拆。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<rect x="20" y="40" width="30" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="50" y="40" width="30" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="80" y="40" width="30" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="110" y="40" width="30" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="140" y="40" width="30" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="170" y="40" width="30" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="200" y="40" width="30" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="230" y="40" width="30" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="260" y="40" width="30" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="290" y="40" width="30" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<line x1="20" y1="34" x2="20" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="110" y1="34" x2="110" y2="28" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="20" y1="34" x2="110" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="65.0" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第一块 j</text>
<line x1="110" y1="34" x2="110" y2="28" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="320" y1="34" x2="320" y2="28" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="110" y1="34" x2="320" y2="34" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="215.0" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i - j：不拆，或按 dp 继续拆</text>
<text x="170" y="96" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">dp[i] = max(j · (i - j), j · dp[i - j])</text>
<text x="170" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10 = 3 + 3 + 4 → 36：尽量拆成 3</text>
</svg>

```python
def integer_break(n):
    dp = [0] * (n + 1)               # dp[i]：拆成至少两份的最大乘积
    for i in range(2, n + 1):
        for j in range(1, i):
            dp[i] = max(dp[i], j * (i - j), j * dp[i - j])
    return dp[n]
```

**要点。**
- 为什么对？：第一块是 `j`，剩下 `i - j` 有两种选择：不拆（`j * (i - j)`）或继续拆（`j * dp[i - j]`），枚举 `j` 取最大。
- 有数学解吗？：尽量拆成 `3`：余 `0` 取 `3^(n/3)`，余 `1` 取 `3^(n//3 - 1) * 4`，余 `2` 取 `3^(n//3) * 2`，`n <= 3` 取 `n - 1`。

**易错点。**
- 只写 `j * (i - j)`：只切两块，`n = 10` 得 `25`，应为 `36`。
- 只写 `j * dp[i - j]`：`dp[1]` 无意义，`n = 2` 得 `0`，应为 `1`。

**对应题目。** LC 343 整数拆分
