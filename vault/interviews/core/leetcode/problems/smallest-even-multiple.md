---
slug: smallest-even-multiple
---
## Q
**LC 2413 最小偶倍数**｜Easy

正整数 `n`。返回 `2` 和 `n` 的最小公倍数。

## A
**一句话。** `n` 是偶数时答案是 `n`，奇数时是 `2n`。

```python
def smallest_even_multiple(n):
    return n if n % 2 == 0 else 2 * n
```

**复杂度。** 时间 `O(1)`，空间 `O(1)`。

**易错点。**
- 总是返回 `2n`：偶数时 `n` 本身已经是偶数倍数。

**追问。**
- 一般的最小公倍数？：`a * b // gcd(a, b)`。

**同模式。** LC 2235 两整数相加、LC 1071 字符串的最大公因子
