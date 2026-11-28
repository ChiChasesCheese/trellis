---
id: lct-learn-math-7-3
node: math.7.3
type: qa
step: 1
---
## Q
**数学算法 › 杂项 › 曼哈顿距离与切比雪夫距离**｜学习卡

套路是什么？

## A
**一句话。** 曼哈顿距离的绝对值拆成正负号的所有组合，每种组合下表达式是 `f(i) - f(j)`，答案是 `max f - min f`，各组合取最大。

下图：LC 1131，绝对值拆成 4 种符号组合，每种都是 `f(i) - f(j)`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="30" y="20" width="130" height="32" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="95" y="40" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f = +a +b + i</text>
<rect x="180" y="20" width="130" height="32" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="245" y="40" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">f = +a −b + i</text>
<rect x="30" y="64" width="130" height="32" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="95" y="84" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">f = −a +b + i</text>
<rect x="180" y="64" width="130" height="32" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="245" y="84" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">f = −a −b + i</text>
<text x="170" y="122" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">每种符号组合：答案 = max f - min f</text>
<text x="170" y="140" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">|x| = max(x, -x)：绝对值拆成符号的所有组合，取最大</text>
</svg>

```python
def max_abs_val_expr(arr1, arr2):
    ans = 0
    for p in (1, -1):                # i 项符号固定为 +
        for q in (1, -1):
            vals = [p * a + q * b + i for i, (a, b)
                    in enumerate(zip(arr1, arr2))]
            ans = max(ans, max(vals) - min(vals))
    return ans
```

**要点。**
- 为什么对？：`|x| = max(x, -x)`，三项绝对值拆成 `2^3` 种符号，把 `i`、`j` 分开后每种都是一个值的差；`i` 与 `j` 对称，`i` 项符号可固定。
- LC 1330 怎么改？：翻转只改变子数组两端的两条相邻差：贴着端点时直接算一条边的变化，在中间时增益是 `2 * (最大的线段小端 - 最小的线段大端)`。

**易错点。**
- 只算一种符号组合：示例二得 `14`，应为 `20`。
- 取 `max(vals)` 而不是 `max(vals) - min(vals)`：表达式是两点之差。
- LC 1330 漏掉贴着端点的情形：`[1,5,4]` 只算中间得 `5`，翻转 `[1,5]` 才得 `7`。

**对应题目。** LC 1131 绝对值表达式的最大值、LC 1330 翻转子数组得到最大的数组值
