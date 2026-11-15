---
slug: subtract-the-product-and-sum-of-digits-of-an-integer
---
## Q
**LC 1281 整数的各位积和之差**｜Easy

给整数 `n`，返回它各位数字之积减去各位数字之和的差。

## A
**一句话。** 反复 `divmod(n, 10)` 取出最低位，同时累乘和累加。

```python
def subtract_product_and_sum(n):
    prod, total = 1, 0            # 积的初值是 1
    while n:
        n, d = divmod(n, 10)      # d 是最低位
        prod *= d
        total += d
    return prod - total
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 积的初值设成 `0`：乘出来永远是 0。
- 先除后取模：`n //= 10` 之后再 `n % 10` 取到的是下一位，用 `divmod` 一次完成最稳。

**追问。**
- 也能转成字符串做吗？：`for ch in str(n)`，更直观，但多一次转换的开销。
- 数字里有 0 的影响？：积直接变 0，差等于负的数字和。

**同模式。** LC 258 各位相加、LC 202 快乐数、LC 7 整数反转、LC 9 回文数
