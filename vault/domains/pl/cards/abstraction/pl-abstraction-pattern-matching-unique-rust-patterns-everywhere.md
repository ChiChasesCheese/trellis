---
id: pl-abstraction-pattern-matching-unique-rust-patterns-everywhere
node: abstraction.pattern-matching
type: qa
step: 8
---
## Q
Rust 里「模式」不只出现在 `match` 里，这说明它怎样把模式匹配当成语言的基础？

## A
在 Rust 里，**模式是一种基本的语法类别**，在很多地方都能出现，而不只是 `match`：

```rust
let (a, b) = (1, 2);                       // let 解构
fn dist(&(x, y): &(f64, f64)) -> f64 { }   // 函数参数里的模式
if let Some(n) = lookup(k) { /* 只处理有值的情形 */ }
while let Some(top) = stack.pop() { /* 弹到空为止 */ }
let Some(v) = opt else { return };         // let-else：不匹配就走出
```

因为 Rust 没有 `null`，`Option<T>` 是普通的 enum，取出里面的值唯一的办法就是匹配它，这把「你必须处理没有值的情形」变成了语言层面的强制。同样，`Result` 的错误处理也是靠匹配（`?` 运算符是它的语法糖）。

这与 Java 的路线对比：Java 的模式匹配是**后来加在 `instanceof` 和 `switch` 上的**，仍只出现在这两个位置，是一种「增强的类型判断」；Rust 的模式匹配是**一等语法**，变量绑定本身就是一种模式。

哲学：Rust 继承自 ML、Haskell 的函数式传统，认为「数据的结构」和「处理数据的代码的结构」应当镜像对应。写一个 enum 就等于声明了所有处理它的代码必须覆盖的情形；而编译器会在每处检查，让这种对应成为可验证的。这是 Rust 能以「编译通过就基本正确」闻名的一个重要来源。
