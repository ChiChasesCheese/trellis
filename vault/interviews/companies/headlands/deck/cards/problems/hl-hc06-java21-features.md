---
id: hl-hc06-java21-features
node: problems.hc06-cpu-register-bitwise
type: qa
step: 15
---
## Q
寄存器模拟用到哪些 Java 21 特性和标准库？各自的好处是什么？

## A
- **record + 紧凑构造器**：全部指令、`Run`、`Compiled`；非法指令构造不出来；`parseLine("AND 0xFF")` 可直接与 `new And(0xFF)` 比较。不该用：要继承其他类或需要可变字段时。
- **两层 sealed**：新增指令时所有 switch 编译报错；旧写法是 enum + 一堆可空字段，或 `instanceof` 链加最后 `else throw`。**别用 `default` 兜底**，否则编译器不再提醒漏了新指令。
- **模式匹配 switch + record 解构**：`case And(var m) -> reg & m;` 一步判型取字段，无强转。
- **switch 表达式**：每分支是值，无 fallthrough，无忘 `break` 的 bug。
- **未命名模式 `_`**（预览）：`case Not _ ->`、`case Popcount _ ->`，需要 `--enable-preview`。
- **标准库**：`Integer.compress/expand`（Java 19）、`rotateLeft`、`reverse`、`reverseBytes`、`bitCount`、`HexFormat`（Java 17）、`Integer.toUnsignedString/toUnsignedLong`、`Math.clamp(long,int,int)`（Java 21）、`StringBuilder.repeat`（Java 21）、`body.getFirst()`（Sequenced Collections）代替 `get(0)`。标准库一行代替手写循环，且是 JIT intrinsic。
- 文本块：测试里的多行程序原样可读；`Stream`：`Arrays.stream(out).boxed().toList()`。

测试思路：每条指令真值表；边界（0、全 1、最高位、位 0 / 31）；性质（`expand(compress(x,m),m) == x & m`、`reverse(reverse(x)) == x`）；用 `long` 写独立参照实现随机对拍；编译版与解释版逐程序比较。
