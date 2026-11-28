---
id: lct-learn-dp-5-3
node: dp.5.3
type: qa
step: 1
---
## Q
**动态规划 › 划分型 DP › 约束划分个数**｜学习卡

套路是什么？

## A
**一句话。** 约束段数的划分：定义 `dfs(i, j)` 为前 `j` 个元素恰好分成 `i` 段的最优值，枚举最后一段的左端点 `L`，转移自 `dfs(i - 1, L)` 再加上 `a[L:j]` 这一段的代价。

下图：「前 `j` 个分成 `i` 段」来自上一行「前 `L` 个分成 `i-1` 段」加最后一段 `a[L:j]`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="40" y="30" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="80" y="30" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="100.0" y="48.0" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">L=1</text>
<rect x="120" y="30" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="140.0" y="48.0" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">L=2</text>
<rect x="160" y="30" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="180.0" y="48.0" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">L=3</text>
<rect x="200" y="30" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="220.0" y="48.0" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">L=4</text>
<rect x="240" y="30" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="280" y="30" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="40" y="58" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="80" y="58" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="120" y="58" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="160" y="58" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="200" y="58" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="240" y="58" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="260.0" y="76.0" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">dfs(i,j)</text>
<rect x="280" y="58" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="40" y="86" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="80" y="86" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="120" y="86" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="160" y="86" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="200" y="86" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="240" y="86" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="280" y="86" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="4" y="48" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i-1</text>
<text x="4" y="76" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i 段</text>
<text x="40" y="22" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">j：前 j 个元素 →</text>
<line x1="106.0" y1="54.0" x2="242.0" y2="64.0" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="146.0" y1="54.0" x2="242.0" y2="64.0" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="186.0" y1="54.0" x2="242.0" y2="64.0" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="226.0" y1="54.0" x2="242.0" y2="64.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="242.0,64.0 235.0,63.2 238.2,58.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="132" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">dfs(i, j) = min over L：dfs(i-1, L) + cost(a[L:j])</text>
<text x="170" y="150" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">倒着枚举 L，段内最大值边走边维护</text>
</svg>

```python
def min_difficulty(a, d):            # 分成 d 天，每天难度取最大值
    n = len(a)
    if n < d:
        return -1

    @cache
    def dfs(i, j):                   # 前 j 项分成 i 段的最小总难度
        if i == 1:
            return max(a[:j])
        res, mx = inf, 0
        for L in range(j - 1, i - 2, -1):  # 最后一段是 a[L:j]
            mx = max(mx, a[L])       # 倒着枚举，边走边维护段内最大
            res = min(res, dfs(i - 1, L) + mx)
        return res

    return dfs(d, n)
```

**要点。**
- 为什么对？：最后一段的左端点 `L` 把问题拆成「前 `L` 项分 `i - 1` 段」加「最后一段的代价」，两部分互不影响；`L` 至少为 `i - 1`，保证前面每段非空。
- 恰好 k 段和至多 k 段怎么改？：恰好型内层循环下界取 `i - 1`；至多型把 `i == 1` 的边界放宽，或对 `i` 取最小。
- 段代价怎么算？：段内最大值、和、不同元素数都可以边枚举 `L` 边增量维护，不要每次重算整段。

**易错点。**
- 天数多于项数：`len(a) < d` 时无解，要返回 `-1`，否则 `range` 为空，结果是 `inf`。
- 每次重算 `max(a[L:j])`：多出一个 `n` 的因子，应倒序枚举 `L` 并增量维护段内最大值。
- `i == 1` 的边界漏判：第一段必须从下标 `0` 开始，不能再枚举 `L`。

**对应题目。** LC 1335 工作计划的最低难度
