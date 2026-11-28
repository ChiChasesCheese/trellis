---
id: lct-learn-dp-3-2
node: dp.3.2
type: qa
step: 1
---
## Q
**动态规划 › 背包 › 完全背包**｜学习卡

套路是什么？

## A
**一句话。** 完全背包：每种物品可用无限次，转移读本行 `f[i+1][j - c]`（用了一枚之后还能再用），读上一行才是 0-1 背包。

下图：和 0-1 背包只差一格：「再用一枚」读的是本行 `f[i+1][j-c]`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<rect x="20" y="30" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="66" y="30" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="112" y="30" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="158" y="30" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="204" y="30" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="250" y="30" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="60" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="66" y="60" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="112" y="60" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="158" y="60" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="204" y="60" width="46" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="227.0" y="79.0" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">f[i][j]</text>
<rect x="250" y="60" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="90" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="66" y="90" width="46" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="89.0" y="109.0" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">f[i+1][j-c]</text>
<rect x="112" y="90" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="158" y="90" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="204" y="90" width="46" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="227.0" y="109.0" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[i+1][j]</text>
<rect x="250" y="90" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="227.0" y1="84.0" x2="227.0" y2="93.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="227.0,93.0 224.0,86.7 230.0,86.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<path d="M 89.0 120.0 Q 158.0 147.0 227.0 120.0" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="227.0,120.0 224.2,126.4 220.3,121.9" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="4" y="66" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i</text>
<text x="4" y="96" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i+1</text>
<text x="262" y="70" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">不用这种</text>
<text x="170" y="160" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">再用一枚：读本行（已经可能用过）</text>
</svg>

```python
def coin_change(coins, amount):  # 最少硬币数
    n = len(coins)
    # f[i][j]：只用前 i 种硬币凑 j 元的最少枚数
    f = [[inf] * (amount + 1) for _ in range(n + 1)]
    f[0][0] = 0                  # 不用硬币凑 0 元
    for i, c in enumerate(coins):
        pre, cur = f[i], f[i + 1]
        for j in range(amount + 1):
            cur[j] = pre[j]                  # 不用第 i 种
            if j >= c:                       # 再用一枚：读本行
                cur[j] = min(cur[j], cur[j - c] + 1)
    ans = f[n][amount]
    return ans if ans < inf else -1
```

**要点。**
- 为什么对？：`f[i+1][j - c]` 已经考虑过用第 `i` 种，再加一枚就是「多用一枚」，所以同一种硬币可以重复用任意次。
- LC 518 怎么改？：求组合数：`f[0][0] = 1`，`f[i+1][j] = f[i][j] + f[i+1][j - c]`；外层是硬币所以不计顺序（外层改成金额就是 LC 377 的排列数）。
- LC 279 怎么改？：「硬币」是所有 `<= n` 的完全平方数 `1, 4, 9, ...`，金额 `= n`，一定有解；平方数用 `isqrt` 枚举。

**易错点。**
- 转移读上一行 `f[i][j - c]`：变成 0-1 背包，`coins = [2]`、`amount = 4` 得 `-1`，应为 `2`。
- 贪心取最大面额：`[1,3,4]`、`6` 得 `4+1+1` 三枚，应为 `3+3` 两枚。
- LC 518 漏了 `f[0][0] = 1`：`amount = 0` 应得 `1`，会得 `0`。

**对应题目。** LC 322 零钱兑换、LC 518 零钱兑换 II、LC 279 完全平方数
