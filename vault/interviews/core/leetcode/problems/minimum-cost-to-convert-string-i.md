---
slug: minimum-cost-to-convert-string-i
---
## Q
**LC 2976 转换字符串的最小成本 I**｜Medium

两个等长小写字符串 `source`、`target`，以及数组 `original`、`changed`、`cost`：可以花 `cost[i]` 把字符 `original[i]` 变成 `changed[i]`（可多次使用，可连续变换）。求把 `source` 变成 `target` 的最小总成本，不可能返回 `-1`。

## A
**一句话。** 字符只有 `26` 种，建 `26 × 26` 的距离表，用 Floyd 求任意两字母间最小转换成本，再逐位累加。

```python
def minimum_cost(source, target, original, changed, cost):
    d = [[inf] * 26 for _ in range(26)]
    for i in range(26):
        d[i][i] = 0
    for a, b, c in zip(original, changed, cost):
        a, b = ord(a) - 97, ord(b) - 97
        d[a][b] = min(d[a][b], c)       # 同一对可能有多条
    for k in range(26):
        for i in range(26):
            for j in range(26):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    ans = sum(d[ord(a) - 97][ord(b) - 97]
              for a, b in zip(source, target))
    return -1 if ans == inf else ans
```

**复杂度。** 时间 `O(26³ + n)`，空间 `O(26²)`。

**易错点。**
- 同一对 `(a, b)` 直接覆盖：重复边要取最小值。
- 忘了 `d[i][i] = 0`：字符不变时成本应为 `0`。
- 只用直接转换：可以经过中间字符，要做最短路。

**追问。**
- 变换的是字符串（LC 2977）怎么做？：对"字符串"当节点做 Floyd，再对源串按长度做 DP。

**同模式。** LC 2977 转换字符串的最小成本 II、LC 743 网络延迟时间、LC 139 单词拆分
