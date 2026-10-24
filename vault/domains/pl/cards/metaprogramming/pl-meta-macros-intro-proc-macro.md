---
id: pl-meta-macros-intro-proc-macro
node: metaprogramming.macros
type: qa
step: 4
---
## Q
Rust 的过程宏（procedural macro）和 `#[derive(...)]` 是什么？它与 `macro_rules!` 的根本区别在哪里？

## A
**是什么**：过程宏是一个用普通 Rust 写的函数，输入是一段 token 流，输出是另一段 token 流。编译器遇到使用它的地方，就把这段代码交给它，拿回输出再继续编译。它必须放在一个单独的、标记为 `proc-macro` 的 crate（Rust 的编译与发布单位）里。

三种形式：
- **derive 宏**：`#[derive(Hello)]` 写在结构体上，宏读到结构体定义，输出一个配套的 `impl`。
- **属性宏**：`#[route(GET, "/")]` 写在函数上，可以改写整个函数。
- **函数式宏**：像 `macro_rules!` 一样调用，但内部逻辑是任意代码。

**心智模型**：`macro_rules!` 是模板匹配，能做的事受模式语言限制；过程宏是一个在编译期运行的完整程序，能读结构体的所有字段，能按字段生成任意代码。

**场景**：一个最小的 derive 宏，给被标记的结构体加一个 `hello()` 方法：

```rust
#[derive(Hello)]
struct Order;
fn main() { println!("{}", Order::hello()); }
```

真实输出：`hello from Order`。`Order` 本身没有手写任何方法，方法是宏在编译期生成的。真实项目里 `#[derive(Serialize)]`（serde）就是这样按字段生成序列化代码，没有任何运行时反射。

**要记住的一点**：过程宏是在编译机上运行的程序，所以它们能做任何事（包括读文件、联网），编译时间也因此变长；依赖里的过程宏需要和普通依赖一样被信任。
