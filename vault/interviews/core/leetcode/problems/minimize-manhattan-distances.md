---
slug: minimize-manhattan-distances
---
## Q
**LC 3102 最小化曼哈顿距离**｜Hard

二维点集 `points`。删除恰好一个点后，剩余点中任意两点曼哈顿距离的最大值，取所有删除方案里最小的，返回这个最小值。

## A
**一句话。** 曼哈顿距离的最大值 = `max(x+y 的极差, x-y 的极差)`；删点只有删掉某个维度的最大值或最小值才可能有用，所以只需试 `4` 个候选点，每次 `O(n)` 重算。

```python
def minimum_distance(points):
    s = [x + y for x, y in points]
    d = [x - y for x, y in points]
    cand = {s.index(max(s)), s.index(min(s)),
            d.index(max(d)), d.index(min(d))}
    ans = inf
    for r in cand:
        ss = s[:r] + s[r + 1:]
        dd = d[:r] + d[r + 1:]
        far = max(max(ss) - min(ss), max(dd) - min(dd))
        ans = min(ans, far)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 对每个点都重算最大距离：`O(n²)`，只有极值点值得试。
- 直接枚举点对距离：`O(n²)`；利用坐标变换 `x ± y` 把绝对值去掉。

**追问。**
- 为什么曼哈顿距离等于 `max(|Δ(x+y)|, |Δ(x-y)|)`？：`|a| + |b| = max(|a + b|, |a - b|)`。

**同模式。** LC 1330 翻转子数组得到最大的数组值、LC 296 最佳的碰头地点、LC 1131 绝对值表达式的最大值
