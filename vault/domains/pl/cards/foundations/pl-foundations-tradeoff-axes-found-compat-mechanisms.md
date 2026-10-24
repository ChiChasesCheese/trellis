---
id: pl-foundations-tradeoff-axes-found-compat-mechanisms
node: foundations.tradeoff-axes
type: qa
step: 4
---
## Q
语言怎样在不破坏旧代码的前提下演进？Go 1 兼容承诺和 Rust 的 edition 机制各是什么？

## A
演进与兼容是一对矛盾：新语法常常需要占用旧代码里可能已经用作变量名的词。四种应对方式：

- Go 1 兼容承诺：Go 1.0（2012 年）起承诺，符合 Go 1 规范的程序，在以后的 Go 1.x 版本里继续能编译运行。语言只增加不删改，新特性被限制得很谨慎。
- Rust 的 edition（版本代）：每个 crate（Rust 的编译单元）在配置里声明自己属于哪个 edition（2015、2018、2021、2024）。编译器同时支持所有 edition，不同 edition 的 crate 可以互相链接。新 edition 允许做不兼容的语法改动，因为旧 crate 仍然按旧规则编译。
- C++ 的「几乎不删」：靠 `-std=c++11` 之类的编译选项选语言版本，新标准基本不破坏旧代码；删除极少且极慢（`std::auto_ptr` 在 C++11 弃用、C++17 才删）。为了不让已编译的库失效（ABI，二进制接口约定），标准库里一些公认有缺陷的实现（如 `std::regex` 的性能）也多年没法改。
- Python 3 的断裂：2008 年直接放弃与 Python 2 的兼容，一次性修正设计错误，代价是迁移持续了十年以上。

edition 的实际效果：`async` 在 2015 edition 里还是普通标识符，从 2018 起成为关键字。同一段代码：

```rust
fn main() { let async = 1; println!("{}", async); }
```

用 `--edition 2015` 编译通过，输出 `1`；用 `--edition 2018` 编译失败：`error: expected identifier, found keyword async`。

这是一种折中：用户按 crate 逐个迁移，工具（`cargo fix --edition`）自动改写，编译器内部多维护几套规则。
