---
id: tlc-python-itertools-functools-7-cmp-reduce
node: python.itertools-functools
type: qa
step: 7
---
## Q
**Python 工具箱｜`cmp_to_key`、`reduce` 与 `math.gcd`**

排序规则不是「给每个元素算一个键」，而是「两两比较」（拼接后更大者在前）时，怎么用 `sort`？`reduce` 在面试里怎么用？

## A
`sort` 只接收 `key`；两两比较的规则用 `functools.cmp_to_key` 把「比较函数」转成键：比较函数返回负数表示 `a` 排在 `b` 前，正数反之，0 表示相等。

```python
from functools import cmp_to_key
def largest_number(nums: list[int]) -> str:
    s = list(map(str, nums))
    # 若 a+b > b+a，则 a 应排在 b 前：返回 -1
    s.sort(key=cmp_to_key(lambda a, b: -1 if a + b > b + a else (1 if a + b < b + a else 0)))
    r = "".join(s)
    return "0" if r[0] == "0" else r       # 全是 0 时只保留一个 "0"
print(largest_number([3, 30, 34, 5, 9]), largest_number([10, 2]), largest_number([0, 0]))
# 9534330 210 0
```

- 这是 LC 179 最大数的标准写法；关键是比较的传递性（`a+b > b+a` 构成全序），这是它正确的前提。
- `reduce(func, iterable, initial)` 折叠成一个值：

```python
from functools import reduce
from math import gcd, lcm
import operator
print(reduce(operator.xor, [4, 1, 2, 1, 2]))   # 4：异或抵消成对元素（LC 136）
print(gcd(12, 18, 24), lcm(4, 6))              # 6 12：math.gcd 3.9+ 支持多个参数
```

- 能用 `sum`、`max`、`math.gcd(*nums)` 就别用 `reduce`；`reduce` 适合按位异或、自定义二元运算。
- **坑**：比较函数不满足传递性或反对称（例如总返回 `-1`），`sort` 不报错但结果不可预期；能算出键就用 `key`，更快。
