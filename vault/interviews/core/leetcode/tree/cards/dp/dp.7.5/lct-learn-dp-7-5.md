---
id: lct-learn-dp-7-5
node: dp.7.5
type: qa
step: 1
---
## Q
**动态规划 › 其他线性 DP › 子矩形 DP**｜学习卡

套路是什么？

## A
**一句话。** 子矩形 DP：`f[i+1][j+1]` 是以 `(i, j)` 为右下角的全 `1` 最大正方形边长，等于上、左、左上三格的最小值加一。

下图：以 `(i, j)` 为右下角的正方形，由左上、上、左三个正方形拼出来。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="40" y="30" width="46" height="40" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="63.0" y="54.0" text-anchor="middle" font-size="13" font-family="sans-serif" fill="currentColor">2</text>
<rect x="86" y="30" width="46" height="40" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="109.0" y="54.0" text-anchor="middle" font-size="13" font-family="sans-serif" fill="currentColor">2</text>
<rect x="40" y="70" width="46" height="40" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="63.0" y="94.0" text-anchor="middle" font-size="13" font-family="sans-serif" fill="currentColor">1</text>
<rect x="86" y="70" width="46" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="109.0" y="94.0" text-anchor="middle" font-size="13" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<line x1="79.0" y1="64.0" x2="93.0" y2="76.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="93.0,76.0 86.2,74.2 90.1,69.6" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="109.0" y1="60.0" x2="109.0" y2="72.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="109.0,72.0 106.0,65.7 112.0,65.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="75.0" y1="90.0" x2="89.0" y2="90.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="89.0,90.0 82.7,93.0 82.7,87.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="63" y="24" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">左上</text>
<text x="109" y="24" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">上</text>
<text x="34" y="94" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">左</text>
<text x="160" y="46" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f = 1 + min(左上, 上, 左)</text>
<text x="160" y="66" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= 1 + min(2, 2, 1) = 2</text>
<text x="160" y="96" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">最短的那条腿决定边长：</text>
<text x="160" y="112" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">三格都 ≥ k，才能拼出 k+1</text>
</svg>

```python
def maximal_square(matrix):
    m, n = len(matrix), len(matrix[0])
    # f[i+1][j+1]：以 (i, j) 为右下角的最大边长；多一圈 0 哨兵
    f = [[0] * (n + 1) for _ in range(m + 1)]
    side = 0
    for i, row in enumerate(matrix):
        pre, cur = f[i], f[i + 1]
        for j, ch in enumerate(row):
            if ch == "1":                    # 元素是字符
                cur[j+1] = 1 + min(pre[j], pre[j+1], cur[j])
                side = max(side, cur[j+1])
    return side * side
```

**要点。**
- 为什么对？：边长 `s` 的正方形要求上、左、左上三个方向都至少有 `s-1` 的正方形；取三者最小值再加一，正好是三者能同时撑住的最大边长。
- LC 1277 怎么改？：统计所有全 `1` 正方形：把每格的 `f` 累加，边长 `s` 的右下角贡献 `s` 个。
- 最大矩形（LC 85）怎么办？：正方形的递推不适用：每行当作柱状图的底，用单调栈求最大矩形。

**易错点。**
- 漏掉左上角：`[["1","1","1"],["1","0","1"],["1","1","1"]]` 把右下角算成边长 `2`，应为 `1`。
- 返回边长：题目要面积 `side * side`。
- 元素是字符：写成 `== 1` 永远为假，`[["1"]]` 得 `0`。

**对应题目。** LC 221 最大正方形
