---
id: lct-learn-dp-7-6
node: dp.7.6
type: qa
step: 1
---
## Q
**动态规划 › 其他线性 DP › 多维 DP**｜学习卡

套路是什么？

## A
**一句话。** 多维 DP：把题目里的「条件」当作状态的一维（余数、上一跳步长、蛋数），转移就只是在状态之间走一步。

下图：LC 1262，「和能被 3 整除」这个条件变成第二维余数 `r`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="50" y="34" width="56" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="78.0" y="53.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">不选</text>
<rect x="106" y="34" width="56" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="162" y="34" width="56" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="190.0" y="53.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">选 x</text>
<rect x="50" y="64" width="56" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="78.0" y="83.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[i+1][0]</text>
<rect x="106" y="64" width="56" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="162" y="64" width="56" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">r = 0</text>
<text x="134" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">r = 1</text>
<text x="190" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">r = 2</text>
<text x="20" y="54" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i</text>
<text x="14" y="84" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i+1</text>
<line x1="78.0" y1="59.0" x2="78.0" y2="67.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="78.0,67.0 75.0,60.7 81.0,60.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="172.0" y1="61.0" x2="98.0" y2="69.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="98.0,69.0 104.0,65.3 104.6,71.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="235" y="44" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x = 4</text>
<text x="235" y="62" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">(0 - 4) % 3 = 2</text>
<text x="235" y="80" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">从余 2 选 x 到余 0</text>
<text x="170" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">条件变成状态的一维：f[i][r] = 前 i 个、和模 3 为 r 的最大和</text>
</svg>

```python
def max_sum_div_three(nums):     # 状态：(前 i 个, 和模 3)
    n = len(nums)
    f = [[-inf] * 3 for _ in range(n + 1)]   # -inf：凑不出
    f[0][0] = 0                  # 空集的和是 0，余 0
    for i, x in enumerate(nums):
        for r in range(3):
            f[i+1][r] = max(f[i][r],              # 不选 x
                            f[i][(r - x) % 3] + x)  # 选 x
    return f[n][0]
```

**要点。**
- 为什么对？：余数 `r` 的和要么不含 `x`，要么含 `x` 且之前的余数是 `(r - x) % 3`，所以三个余数状态足够；不可达用 `-inf`。
- LC 403 怎么改？：状态是（石子位置，上一步步长）；用「位置 → 步长集合」的字典从左到右推，每个步长试 `k-1, k, k+1` 且必须 `> 0`。
- LC 887 怎么改？：倒过来问：`m` 次操作、`j` 枚蛋最多能确定几层，`f[m][j] = f[m-1][j-1] + f[m-1][j] + 1`（碎了、没碎、扔的这一层），逐行填到 `>= n`，行数即答案。

**易错点。**
- 初值全写 `0`：等于承认空集余 `1`、`2` 也可达，`[4]` 得 `4`，应为 `0`。
- LC 403 漏掉 `step > 0`：`step = 0` 时目标是自己，往正在遍历的集合里加元素，`RuntimeError`。
- LC 887 转移读本行 `f[m][j-1]`：同一次操作用了两次，应读 `f[m-1]`。

**对应题目。** LC 1262 可被三整除的最大和、LC 403 青蛙过河、LC 887 鸡蛋掉落
