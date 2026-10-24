---
id: pl-types-numbers-unique-rust-explicit
node: types.numbers
type: qa
step: 4
---
## Q
Rust 为什么给整数提供 `checked_`、`wrapping_`、`saturating_`、`overflowing_` 四套运算？这体现了什么设计哲学，和 Python 的做法有什么对比？

## A
Rust 的哲学是：溢出行为不应该由语言替你默认，因为不同场景的正确答案不同。所以每个整数类型都提供四种显式运算：

```rust
let x: u8 = 250;
x.checked_add(10);       // None：失败用 Option 表达
x.wrapping_add(10);      // 4：有意回绕（哈希、校验和）
x.saturating_add(10);    // 255：停在上限（音量、颜色分量）
x.overflowing_add(10);   // (4, true)：结果加溢出标志
```

实际输出：`None 4 255 (4, true)`。同一个加法，四种场景各有一种正确含义，名字本身就写出了意图，代码评审时不用猜。

对比 Python：它选择「不让你做选择」，`int` 无限大，`250 + 10` 永远是 260，所以没有溢出问题，也不需要这套 API。代价是每个整数都是带头部的堆对象，运算要经过动态分派，比一条机器加法指令慢得多；而且当你确实想要 8 位回绕（解析二进制协议），必须自己写 `& 0xFF`。

两种哲学对应两种用户：Rust 面向要控制每个字节的系统程序员，宁可多写；Python 面向要快速得到正确答案的人，宁可多花算力。Java 和 Go 居中：默认回绕，要检查就自己调 `Math.addExact` 之类的函数。
