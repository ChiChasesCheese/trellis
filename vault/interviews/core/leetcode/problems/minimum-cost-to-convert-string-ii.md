---
slug: minimum-cost-to-convert-string-ii
---
## Q
**LC 2977 转换字符串的最小成本 II**｜Hard

`source`、`target` 等长（`<= 1000`）。规则 `original[i] → changed[i]` 花 `cost[i]`，可把子串整段替换；多次操作的区间要么不相交、要么完全相同（同一段可连续换多次）。求最小总成本，做不到返回 `-1`。

## A
**一句话。** 两步：把所有规则串当点跑 Floyd，得任意两串间的最便宜转换；再做线性 DP，`f[i]` 是前 `i` 个字符的最小成本，这一位相同可直接跳过，或枚举规则长度 `L` 整段转换。

```python
def minimum_cost(source, target, original, changed, cost):
    ids = {}
    for s in original + changed:
        ids.setdefault(s, len(ids))
    m = len(ids)
    d = [[inf] * m for _ in range(m)]
    for i in range(m):
        d[i][i] = 0
    for a, b, c in zip(original, changed, cost):
        x, y = ids[a], ids[b]
        d[x][y] = min(d[x][y], c)
    for k in range(m):         # Floyd：串之间的最便宜转换
        for i in range(m):
            if d[i][k] == inf:
                continue
            for j in range(m):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]

    lens = sorted({len(s) for s in original})
    n = len(source)
    f = [inf] * (n + 1)        # f[i]：前 i 个字符的最小成本
    f[0] = 0
    for i in range(n):
        if f[i] == inf:
            continue
        if source[i] == target[i]:
            f[i + 1] = min(f[i + 1], f[i])   # 这一位不动
        for L in lens:
            if i + L > n:
                break
            a, b = source[i:i + L], target[i:i + L]
            if a in ids and b in ids:
                c = f[i] + d[ids[a]][ids[b]]
                f[i + L] = min(f[i + L], c)
    return -1 if f[n] == inf else f[n]
```

**复杂度。** 时间 `O(m³ + n·|lens|·n)`（`m <= 200` 个不同串），空间 `O(m² + n)`。

**易错点。**
- 只用一步规则：`a → c → b` 可能更便宜，必须先做最短路。
- 相同字符时不允许跳过：`source[i] == target[i]` 时成本为 0，不必匹配任何规则。

**追问。**
- 子串比较太慢？：把规则串插进字典树，从 `i` 出发沿 `source`、`target` 两棵树同时往下走，一步拿到所有长度的编号。
- 为什么区间不能部分重叠？：题目限制保证 DP 可以按段切开，否则就不是线性划分了。

**同模式。** LC 139 单词拆分、LC 2976 转换字符串的最小成本 I、LC 743 网络延迟时间
