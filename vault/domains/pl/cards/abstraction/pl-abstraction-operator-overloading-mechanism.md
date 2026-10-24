---
id: pl-abstraction-operator-overloading-mechanism
node: abstraction.operator-overloading
type: qa
step: 5
---
## Q
运算符重载在编译期和运行期分别怎样解析？一个 `a + b` 的成本取决于什么？

## A
- **Python**：运行期解析。`a + b` 编译成 `BINARY_OP` 字节码，执行时按上一张卡的协议查 `type(a)` 的 `__add__`、必要时查 `type(b)` 的 `__radd__`。对 `int + int` 解释器有特化的快路径；自定义类型走完整查找，每次一次完整的 Python 函数调用，量级远高于一次整数加法。
- **Rust**：编译期解析。类型已知，编译器直接选出 `Add::add` 的具体实现，作为普通函数调用，常常内联到和手写一样的机器码。所以 Rust 里 `a + b` 的成本由实现决定，但不会有任何分派开销。
- **Java / Go**：`+` 只作用于内置类型，成本固定；`BigDecimal.add` 是普通方法调用。

数值计算里 Python 的做法有个有趣的结果：Python 本身慢，但 NumPy 的数组实现了 `__add__`、`__matmul__`，把 `a + b` 变成**对整块数组的一次 C 循环**，运算符成了在 Python 里调用 C 代码的接口。Python 3.5 专门增加 `@` 运算符（PEP 465）就是为了矩阵乘法，让科学计算社区写出和数学公式一样的代码。

所以运算符重载的价值，不只是语法糖：它让**领域专用类型**与数学符号对齐，同时把真正的计算放到实现里最高效的地方。代价是必须相信重载的实现不会做出意外的事。
