---
id: pl-rt-syntax-pitfall-bit-precedence
node: runtime.syntax-parsing
type: qa
step: 10
---
## Q
`x & mask == 0` 这一行在 C、C++、Java、Go、Rust、Python 里分别会怎样？优先级表的差异怎么变成线上 bug？

## A
想判断“`x` 的某个位是否为 0”，直觉写法是 `x & mask == 0`。`x = 10`（二进制 1010）、`mask = 4`（0100），期望结果为真（该位确实是 0）。

- **C**：`==` 比 `&` 优先级高，解析成 `x & (mask == 0)`，即 `10 & 0`，结果 `0`（假）。实测 `printf("%d %d\n", x & mask == 0, (x & mask) == 0)` 输出 `0 1`，两种读法结果相反，而且**能编译、跑得通**，编译器最多给一条 `-Wparentheses` 警告。
- **C++**：与 C 相同。实测同样的 `printf` 输出 `0 1`，能编译、能运行；`bool` 会提升为 `int`，所以类型检查不拦。Clang 在 `-Wall` 下有 `-Wparentheses` 警告，但不是错误。
- **Java**：沿用了 C 的优先级，解析成 `x & (mask == 0)`，但 `int & boolean` 没有定义，所以直接编译失败：
```
error: bad operand types for binary operator '&'
  first type:  int
  second type: boolean
```
- **Go**：`&` 被归入乘法级优先级，高于 `==`，所以写 `x&mask == 0` 就是期望的 `(x & mask) == 0`，输出 `true`。
- **Rust**：同样把位运算提高到比较运算之上，输出 `true`。
- **Python**：`&` 同样高于比较，输出 `True`。

**教训**：C 的这个优先级是历史原因（早期 C 没有 `&&`，位运算符兼任逻辑运算）。Go、Rust、Python 在设计时都把它修了，Java 为了兼容没有修，但它的类型检查把静默错误变成了编译错误。在 C 系语言里（还有 C++、JavaScript 等同样的表）这是经典的静默 bug。

做法：位掩码判断永远写 `(x & mask) == 0`，不依赖语言的优先级；在 C/C++/JS 项目里打开对应警告（`-Wparentheses`、ESLint 的 `no-mixed-operators`）并设为错误。
