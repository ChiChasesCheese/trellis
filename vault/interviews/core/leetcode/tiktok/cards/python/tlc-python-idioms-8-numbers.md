---
id: tlc-python-idioms-8-numbers
node: python.idioms
type: qa
step: 8
---
## Q
**Python 工具箱｜数字、哨兵与位运算小工具**

商和余数、无穷大哨兵、整数平方根、二进制位数，各有什么内置函数？Python 的整数除法对负数怎么取整？

## A
```python
import math
print(divmod(17, 5), divmod(-17, 5))          # (3, 2) (-4, 3)：一次得到商和余数
print(-17 // 5, -17 % 5, int(-17 / 5))        # -4 3 -3：// 向负无穷取整，% 与除数同号
print(math.inf > 10**18, -math.inf)           # True -inf：任何整数都比它小
print(math.isqrt(99), (13).bit_count(), (8).bit_length())   # 9 3 4
print(next((x for x in [1, 3, 4] if x % 2 == 0), None))     # 4：找第一个满足条件的元素
```

- `//` 向**负无穷**取整，不是向 0：`-17 // 5 = -4`。C++ / Java 是向 0 取整，从那边移植代码时要留意；需要向 0 取整写 `int(a / b)`（浮点，大数会不准）。
- `divmod(a, b)` 同时得到商和余数：进位加法（LC 2、415）`carry, d = divmod(x + y + carry, 10)`，转换时间 / 进制。
- 哨兵：`best = math.inf`（最小化）、`-math.inf`（最大化）；整数最小值问题也可以用 `float('inf')`，比较时 `int` 与 `float` 混用没问题。
- `math.isqrt(n)` 是精确整数平方根（3.8+），`int(n ** 0.5)` 对超过 `2^52` 的整数可能差 1；`n.bit_count()`（3.10+）数 1 的个数；`n.bit_length()` 是二进制位数。
- `next(gen, default)` 取第一个满足条件的元素，没有则返回默认值，不抛 `StopIteration`。
- 整数**没有溢出**，不必像 Java 那样担心 `int` 越界；但题目要求「对 `10^9 + 7` 取模」时，每次乘法后都要取模，避免大整数拖慢速度。
- **坑**：`==` 比较浮点数要用 `math.isclose`；`inf` 参与整数运算会变成 `float`，结果不要再当下标用。
