---
slug: tt-die-beats-probability
---
## Q
**一个骰子掷出更大点数的概率**｜Medium

两个公平骰子 `A`、`B`，每面写一个整数（面数可不同，数字可重复）。各掷一次，返回 `A` 的点数严格大于 `B` 的精确概率（分数）。

## A
**一句话。** 排序 `B`，对 `A` 的每一面用 `bisect_left` 数 `B` 中严格更小的面数，求和除以 `p·q`。

```python
def beat_probability(a, b):
    sb = sorted(b)
    # bisect_left：B 中严格小于 x 的面数
    wins = sum(bisect_left(sb, x) for x in a)
    return Fraction(wins, len(a) * len(b))
```

**复杂度。** 时间 `O((p + q) log q)`，空间 `O(q)`。

**易错点。**
- 用 `bisect_right`：平局被算成赢，`A = [2,5]`、`B = [2,5]` 得 `3/4`，应为 `1/4`。
- 浮点除法：`1/3` 这类值不精确，用 `Fraction`。

**追问。**
- 平局算一半？：每面再数平局数 `bisect_right - bisect_left`，返回 `Fraction(2·赢 + 平, 2·p·q)`。
- 三个骰子能排出最强的吗？：不能，`A=[2,2,4,4,9,9]`、`B=[1,1,6,6,8,8]`、`C=[3,3,5,5,7,7]` 循环相胜，概率都是 `5/9`。

**同模式。** LC 2300 咒语和药水的成功对数、LC 1855 下标对中的最大距离、LC 2563 统计公平数对的数目、LC 315 计算右侧小于当前元素的个数
