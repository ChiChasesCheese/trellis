---
id: pl-types-numbers-found-decimal-types
node: types.numbers
type: qa
step: 4
---
## Q
浮点数 `double` 之外，Java 的 `BigDecimal` 和 Python 的 `Decimal` 是什么？什么时候该用它们？

## A
`double` / `float`（二进制浮点，遵循 IEEE 754）用二进制小数近似实数，速度快，但 0.1 这样的十进制小数无法精确表示。`BigDecimal`（Java）和 `Decimal`（Python 标准库的 `decimal` 模块）是十进制数类型：把数字存成「整数加小数点位置」，十进制小数可以精确表示，加减乘的结果也精确。代价是慢（每次运算是软件实现，不是一条 CPU 指令）和写法繁琐。

```python
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"), 0.1 + 0.2)
```

实际输出 `0.3 0.30000000000000004`。

使用要点：必须用字符串构造（`Decimal("0.1")`、Java 的 `new BigDecimal("0.1")`）。从浮点数构造会把已有的误差原样带进来：Java 的 `new BigDecimal(0.1)` 得到 `0.1000000000000000055511151231257827021181583404541015625`。

适用场景：金额、税率、需要和人工账目逐位对得上的计算。不适用：科学计算、图形、机器学习，那里误差在容许范围内，速度更重要。C++、Go 和 Rust 的标准库没有十进制类型，通常用以最小货币单位计的整数，或第三方库（C++ 里常用 Boost.Multiprecision）。
