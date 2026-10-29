---
id: tlc-adding-two-negabinary-numbers-2-code
node: b.adding-two-negabinary-numbers
type: qa
step: 2
---
## Q
**LC 1073 负二进制数相加**｜写出 Python 实现

两个以 -2 为基数的数，用无前导零、高位在前的 0/1 数组给出（长度 `1` 到 `1000`），返回它们之和的同样表示。不要转成整数再转回。

## A
**思路。** 两个数组都从末尾（低位）往前对齐相加，本位和 `x` 写下 `x & 1`，进位取 `-(x >> 1)`。输入走完后把剩下的进位展开，再去掉前导零，最后反转成高位在前。

```python
from itertools import zip_longest


def add_negabinary(arr1: list[int], arr2: list[int]) -> list[int]:
    out: list[int] = []                      # 从低位到高位收集结果
    carry = 0                                # 进位只可能是 -1、0、1
    for a, b in zip_longest(reversed(arr1), reversed(arr2), fillvalue=0):
        x = a + b + carry                    # x 在 [-1, 3] 内
        out.append(x & 1)                    # 本位：x 的奇偶（-1 & 1 == 1，负数也对）
        carry = -(x >> 1)                    # 进位是 -(x // 2)：因为 2 = (-1) * (-2)
    while carry:                             # 进位 1 → [1]；进位 -1 → [1, 1]（-1 = 1*(-2) + 1）
        out.append(carry & 1)
        carry = -(carry >> 1)
    while len(out) > 1 and out[-1] == 0:     # 去掉前导零（高位在列表末尾）
        out.pop()
    return out[::-1]
```

运行：`[1,1,1,1,1], [1,0,1]` → `[1,0,0,0,0]`（11 + 5 = 16），`[0], [0]` → `[0]`，`[0], [1]` → `[1]`，`[1], [1]` → `[1,1,0]`（1 + 1 = 2 = 4 - 2），`[1,1], [1]` → `[0]`（-1 + 1 = 0），`[1,1], [1,1]` → `[1,0]`（-1 + -1 = -2）。

**复杂度。** 时间 `O(max(m, n))`；空间 `O(max(m, n))`：结果数组。

**写法要点。** `zip_longest(reversed(arr1), reversed(arr2), fillvalue=0)` 一次解决「从低位对齐」和「短的补零」，不用两个下标；`reversed` 返回迭代器，不复制列表；结果先按低位在前 `append`，最后 `out[::-1]` 反转一次，避免 `insert(0, …)` 的 `O(n)`；`x & 1`、`x >> 1` 对负数也是数学上的模 2 和向下取整除以 2。
