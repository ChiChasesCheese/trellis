---
id: tlc-evaluate-division-3-why
node: p4.evaluate-division
type: qa
step: 3
---
## Q
**LC 399 除法求值**｜正确性

为什么合并时 `ratio[ra] = v * ratio[b] / ratio[a]`？路径压缩之后，为什么 `ratio[x]` 仍然表示 `x / parent[x]`？

## A
**不变量。** 任意时刻，`ratio[x] = x / parent[x]`，所以 `x` 到根的比值是沿路径的 `ratio` 乘积。合并 `a / b = v`：`a / ra = ratio[a]`，`b / rb = ratio[b]`，要得到 `ra / rb`：

`ra / rb = (a / ratio[a]) / (b / ratio[b]) = (a / b) * ratio[b] / ratio[a] = v * ratio[b] / ratio[a]`。

路径压缩时，`find(p)` 返回后 `ratio[p] = p / root`，`ratio[x]` 原来是 `x / p`，相乘得 `x / root`，再把 `parent[x]` 改成 `root`，不变量保持。查询 `c / d`：两者同根 `r`，`(c / r) / (d / r) = c / d`，根抵消，所以直接 `ratio[c] / ratio[d]`。

**反例（错误写法一）：压缩时先改 `parent[x]` 再乘。** 先把 `parent[x]` 设成根，再用 `ratio[parent[x]]`（根自己，值为 `1`）去乘，比值没有累积。`a/b = 2, b/c = 3, c/d = 4`，查询 `a/d`，错误版本得 `2.0`，正确是 `24.0`。

**反例（错误写法二）：合并公式写成 `v * ratio[a] / ratio[b]`。** `[["a","b"],["c","d"],["a","c"]]`、`values = [2,3,5]`，查询 `b/d`，错误版本得 `3.33…`，正确是 `7.5`（`a/d = 15`，再除以 `a/b = 2`）。
