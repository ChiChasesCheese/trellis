---
id: lct-learn-dp-4-1-1
node: dp.4.1.1
type: qa
step: 1
---
## Q
**动态规划 › 经典线性 DP › 最长公共子序列（LCS） › 基础**｜学习卡

套路是什么？

## A
**一句话。** 两个序列的前缀 DP：`f[i][j]` 看 `a[:i]` 与 `b[:j]`，末尾相等就一起去掉，不等就丢掉其中一个末尾取最优。

下图：`f[i+1][j+1]` 只看左上、上、左三格。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="20" y="20" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="66" y="20" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="112" y="20" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="158" y="20" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="48" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="66" y="48" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="89.0" y="66.0" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">左上</text>
<rect x="112" y="48" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="135.0" y="66.0" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">上</text>
<rect x="158" y="48" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="76" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="66" y="76" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="89.0" y="94.0" text-anchor="middle" font-size="9" font-family="sans-serif" fill="currentColor">左</text>
<rect x="112" y="76" width="46" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="135.0" y="94.0" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[i+1][j+1]</text>
<rect x="158" y="76" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="104" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="66" y="104" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="112" y="104" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="158" y="104" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="105.0" y1="70.0" x2="117.0" y2="80.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="117.0,80.0 110.2,78.2 114.1,73.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="135.0" y1="68.0" x2="135.0" y2="77.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="135.0,77.0 132.0,70.7 138.0,70.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="102.0" y1="90.0" x2="111.0" y2="90.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="111.0,90.0 104.7,93.0 104.7,87.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="215" y="40" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">a[i] == b[j]：</text>
<text x="215" y="56" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">左上 + 1，一起去掉</text>
<text x="215" y="84" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">a[i] ≠ b[j]：</text>
<text x="215" y="100" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">max(上, 左)</text>
<text x="215" y="116" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">丢掉其中一个末尾</text>
<text x="215" y="140" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 0 行 / 列：空串 = 0</text>
</svg>

```python
def lcs(a, b):
    m, n = len(a), len(b)
    # f[i][j]：a[:i] 与 b[:j] 的最长公共子序列长度
    f = [[0] * (n + 1) for _ in range(m + 1)]   # 空串行列为 0
    for i, x in enumerate(a):
        pre, cur = f[i], f[i + 1]
        for j, y in enumerate(b):
            if x == y:
                cur[j + 1] = pre[j] + 1          # 末尾配上
            else:                                # 丢掉一个末尾
                cur[j + 1] = max(pre[j + 1], cur[j])
    return f[m][n]
```

**要点。**
- 为什么对？：看两串末尾：相等则它们一定可以配成一对（斜上加一）；不等则两者至少有一个不在公共部分，丢掉其一取大。
- LC 72 怎么改？：`f[i][0] = i`、`f[0][j] = j`；末尾相等取斜上，不等取「替换 `f[i-1][j-1]`、删除 `f[i-1][j]`、插入 `f[i][j-1]`」最小再加 `1`。
- LC 718 怎么改？：子数组要连续：不等直接归零，相等取斜上加一，答案是全表最大值，不是右下角。

**易错点。**
- LCS 不等时归零（按子串处理）：`"abcde"` 与 `"ace"` 得 `1`，应为 `3`。
- LC 718 答案取 `f[m][n]`：子数组可在任意位置结束，要取全表最大值。
- LC 72 边界没初始化：`("", "a")` 得 `0`，应为 `1`。

**对应题目。** LC 1143 最长公共子序列、LC 72 编辑距离、LC 718 最长重复子数组
