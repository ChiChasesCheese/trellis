---
slug: maximum-of-absolute-value-expression
---
## Q
**LC 1131 绝对值表达式的最大值**｜Medium

求 `|arr1[i]-arr1[j]| + |arr2[i]-arr2[j]| + |i-j|` 在所有下标对上的最大值。

## A
**一句话。** 绝对值拆成正负号组合，每种组合下是 `f(i) - f(j)`，答案是 `max f - min f`。

```python
def max_abs_val_expr(arr1, arr2):
    ans = 0
    for p, q in product((1, -1), repeat=2):   # i 项符号固定为 +
        vals = [p * a + q * b + i
                for i, (a, b) in enumerate(zip(arr1, arr2))]
        ans = max(ans, max(vals) - min(vals))
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只算 `(+,+)` 一种组合：示例二得 `14`，应为 `20`。
- 取 `max(vals)` 而不是 `max(vals) - min(vals)`：表达式是两点之差。

**追问。**
- 推广到 `k` 个数组呢？：符号组合 `2^k` 种，总 `O(2^k·n·k)`。
- 为什么 `i` 项符号可以固定？：`i`、`j` 对称，翻转全部符号得到同一个值。

**同模式。** LC 3102 最小化曼哈顿距离、LC 1330 翻转子数组得到最大的数组值、LC 296 最佳的碰头地点
