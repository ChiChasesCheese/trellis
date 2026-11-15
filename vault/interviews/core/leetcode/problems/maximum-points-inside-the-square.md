---
slug: maximum-points-inside-the-square
---
## Q
**LC 3143 正方形中的最多点数**｜Medium

平面上的点各带一个字母标签。正方形以原点为中心、边平行坐标轴（边上算在内），内部不能有两个同标签的点。求合法正方形最多包含几个点。

## A
**一句话。** 点 `(x, y)` 落入半边长 `d = max(|x|,|y|)` 的正方形；每个标签记最小和次小的 `d`，所有次小值的最小者 `bound` 是半边长的严格上界，数 `d < bound` 的点。

```python
def max_points_inside_square(points, s):
    first = {}                  # 标签 -> 最小的 d
    bound = inf                 # 各标签次小 d 的最小值
    for (x, y), c in zip(points, s):
        d = max(abs(x), abs(y))
        if d < first.get(c, inf):
            d, first[c] = first.get(c, inf), d
        bound = min(bound, d)   # d 此时是较大的那个
    return sum(d < bound for d in first.values())
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`（最多 26 个标签）。

**易错点。**
- 用 `<=` 计数：半边长等于 `bound` 时那个标签的两个点都在边上，已经冲突。
- 用欧氏距离或 `|x|+|y|`：正方形对应切比雪夫距离 `max(|x|,|y|)`。

**追问。**
- 二分做法？：二分半边长，检查内部有无重复标签，`O(n log U)`，单调性是「越大越容易冲突」。
- 点数多但只有 26 种标签？：一遍扫描维护最小、次小即可，不必排序。

**同模式。** LC 875 爱吃香蕉的珂珂、LC 1552 两球之间的磁力
