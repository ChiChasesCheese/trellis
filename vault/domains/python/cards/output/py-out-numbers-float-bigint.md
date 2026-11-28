---
id: py-out-numbers-float-bigint
node: output.numbers
type: qa
step: 3
---
## Q
**浮点误差与不会溢出的 int**｜读代码说输出

```python
from math import isclose
print(0.1 + 0.2 == 0.3, 0.1 + 0.2)
print(sum([0.1] * 10) == 1.0)
print(2**64 + 1, float(2**53) + 1 == float(2**53))
print(isclose(0.1 + 0.2, 0.3))
```

输出什么？（Python 3.14）

## A
**输出。**
```
False 0.30000000000000004
True
18446744073709551617 True
True
```

**为什么。**
- 0.1、0.2 在二进制里是无限小数，存成 64 位 double（IEEE 754）时各带一点误差，相加后不再等于 0.3 的那个 double。
- `sum` 对浮点数从 Python 3.12 起用补偿求和（compensated summation），十个 0.1 相加恰好得 1.0；3.11 及以前是 False，手写 `for` 累加仍然是 False。
- `int` 是任意精度（arbitrary precision），2**64 + 1 不会溢出；`float` 只有 53 位尾数，2**53 + 1 已经表示不出来，加 1 被吞掉。

**语言为什么这样设计。**
- 浮点遵循硬件和 IEEE 754，速度快，所以 Python 不偷偷改它；`int` 选无限精度是为了让整数运算永远正确，代价是比机器整数慢、占内存多。
- Java、C、Go 的 `int` 固定宽度，溢出会回绕；JavaScript 的 Number 全是 double，大于 2**53 就丢精度。

**怎么写才对。**
```python
isclose(a, b)                 # 比较浮点数；金额用 decimal.Decimal 或整数分
```

**面试里一句话。**
Floats are binary approximations so never compare them with `==`, while Python ints are arbitrary precision and cannot overflow.
