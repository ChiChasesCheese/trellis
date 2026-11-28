---
id: lct-learn-greedy-7
node: greedy.7
type: qa
step: 1
---
## Q
**贪心算法 › 交互题**｜学习卡

套路是什么？

## A
**一句话。** 交互题只能调用不能看内部：利用单调性每次询问排除一行或一列，双指针从一个角出发。

下图：LC 1237，`f` 对 `x`、`y` 都单调，从一个角出发每次排除一整行或一整列。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<rect x="30" y="20" width="40" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="70" y="20" width="40" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="110" y="20" width="40" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="150" y="20" width="40" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="30" y="54" width="40" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="70" y="54" width="40" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="110" y="54" width="40" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="150" y="54" width="40" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="30" y="88" width="40" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="70" y="88" width="40" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="110" y="88" width="40" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="150" y="88" width="40" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="30" y="122" width="40" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="70" y="122" width="40" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="110" y="122" width="40" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="150" y="122" width="40" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="30" y="14" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x →（增大）</text>
<text x="14" y="40" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">y</text>
<text x="14" y="58" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">↓</text>
<text x="4" y="76" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">减小</text>
<text x="50" y="41" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">起点</text>
<text x="200" y="40" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">x = 1，y = 1000 出发</text>
<text x="200" y="62" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f &lt; z：x += 1</text>
<text x="200" y="78" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（这个 x 再配更小的 y</text>
<text x="200" y="92" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只会更小）</text>
<text x="200" y="114" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f &gt; z：y -= 1</text>
<text x="200" y="136" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">f = z：记下，x+1、y-1</text>
<text x="170" y="170" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每问一次排除一行或一列：O(x + y) 次询问</text>
</svg>

```python
def find_solution(customfunction, z):
    ans = []
    x, y = 1, 1000                   # x 最小、y 最大
    while x <= 1000 and y >= 1:
        v = customfunction.f(x, y)
        if v < z:
            x += 1                   # 该 x 配更小的 y 只会更小
        elif v > z:
            y -= 1                   # 该 y 配更大的 x 只会更大
        else:
            ans.append([x, y])
            x += 1                   # 严格单调：这行这列不会再有解
            y -= 1
    return ans
```

**要点。**
- 为什么对？：`f` 对 `x`、`y` 都严格递增，在 `(x, y)` 处太小，则这个 `x` 配所有不大于 `y` 的都更小，整个 `x` 排除；太大则排除这个 `y`。
- 不知道范围怎么改？：先倍增 `x = 1, 2, 4, ...` 找到 `f(x, 1) > z` 的上界，再双指针；或对每个 `x` 二分 `y`，`O(X log Y)`。

**易错点。**
- 从 `(1,1)` 出发同时增大：没有方向，判断不了该动哪个。
- 边界写成 `x < 1000`：漏掉 `x = 1000` 的解。

**对应题目。** LC 1237 找出给定方程的正整数解
