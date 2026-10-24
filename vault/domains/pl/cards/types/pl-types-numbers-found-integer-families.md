---
id: pl-types-numbers-found-integer-families
node: types.numbers
type: qa
step: 2
---
## Q
C++、Go、Java、Rust、Python 各提供哪些整数类型？有符号与无符号、固定宽度与任意精度的区别是什么？

## A
计算机里的整数分为固定宽度和任意精度。固定宽度整数占固定的位数（8、16、32、64……），取值范围有限，运算是一条 CPU 指令；任意精度整数按需增长，永远不溢出，但每次运算更慢。

- C++：`short`、`int`、`long`、`long long` 各自有符号和无符号两套，但宽度只规定下限，由平台决定（本机 `int` 4 字节，`long` 8 字节，Windows 上 `long` 只有 4 字节）；需要固定宽度时用 `<cstdint>` 里的 `int32_t`、`uint64_t`。这是 C 留下的「按机器的字长来」的传统。
- Go：`int8`、`int16`、`int32`、`int64` 和对应的无符号 `uint8`…`uint64`；`int` 和 `uint` 的宽度跟平台字长（64 位机器上是 64 位）。
- Java：只有有符号的 `byte`（8）、`short`（16）、`int`（32）、`long`（64），加上 16 位无符号的 `char`；没有无符号整数类型，需要时用辅助方法（如 `Integer.toUnsignedString`）。
- Rust：`i8`…`i128` 有符号，`u8`…`u128` 无符号，`isize`/`usize` 随平台（用作下标和长度）；宽度写在类型名里。
- Python：只有一种 `int`，任意精度。

```java
int i = Integer.MAX_VALUE;           // 2147483647
System.out.println(Integer.toUnsignedString(-1));   // 4294967295
```

```rust
println!("{} {} {}", i32::MAX, u8::MAX, i128::MAX);
```

Java 的输出里 `-1` 按无符号解释是 `4294967295`；Rust 输出 `2147483647 255 170141183460469231731687303715884105727`。

有符号与无符号的区别只在位模式如何解释：同样 32 位，`11…1` 是 -1（有符号，补码）或 4294967295（无符号）。选择影响取值范围，也影响溢出和比较的行为。
