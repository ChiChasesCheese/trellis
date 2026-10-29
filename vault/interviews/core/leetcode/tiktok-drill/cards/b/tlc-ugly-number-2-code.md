---
id: tlc-ugly-number-2-code
node: b.ugly-number
type: qa
step: 2
---
## Q
**LC 263 丑数**｜写出 Python 实现

整数 `n`（`-2^31 <= n <= 2^31 - 1`），判断它是否是只含质因数 2、3、5 的正整数（`1` 算）。要求 `O(log n)`。

## A
**思路。** 非正数直接 `False`。对 2、3、5 依次 `while n % p == 0: n //= p`，最后看 `n == 1`。

```python
def is_ugly(n: int) -> bool:
    if n <= 0:                       # 丑数必须是正整数；0 还会让下面的循环永不停止
        return False
    for p in (2, 3, 5):
        while n % p == 0:            # 把因子 p 除干净
            n //= p
    return n == 1                    # 只剩 1，说明没有 2、3、5 以外的质因数
```

运行：`6` → `True`，`1` → `True`，`14` → `False`，`0` → `False`，`-6` → `False`，`2^30` → `True`，`2^31 - 1` → `False`。

**复杂度。** 时间 `O(log n)`：每次整除至少让 `n` 减半；空间 `O(1)`。

**写法要点。** 先写守卫语句（guard clause）`if n <= 0: return False`，把特殊情况挡在前面，主逻辑不用嵌套；`for p in (2, 3, 5)` 用元组列出因子，比写三段重复的 `while` 清楚；`//=` 保持整数；直接返回布尔表达式 `n == 1`，不写 `if ...: return True`。
