---
id: pl-meta-annotations-intro-rust-attribute
node: metaprogramming.annotations-decorators
type: qa
step: 5
---
## Q
Rust 的属性（attribute）`#[...]` 是什么？编译器自己理解的属性和由宏处理的属性有什么区别？

## A
**是什么**：属性是写在条目（函数、结构体、字段、模块）前面的 `#[名字]` 或 `#[名字(参数)]`，给编译器或宏提供附加指示。样子和 Java 的注解相近，但处理方都在编译期。

**两类**：
1. **编译器内置**：编译器直接理解并改变行为。
   - `#[derive(Debug, Clone, PartialEq)]` 让编译器为结构体自动实现这些 trait（可理解为接口）。
   - `#[cfg(target_os = "macos")]` 条件编译：不满足条件的条目根本不进入编译。
   - `#[must_use]` 要求调用方必须使用返回值，丢弃就产生编译警告。
   - `#[inline]`、`#[test]` 也属此类。
2. **宏处理**：属性宏和 derive 宏是库作者写的过程宏，编译器把被标记条目的代码交给它，拿回改写后的代码。`#[tokio::main]` 就是把 `async fn main` 改写成能运行的同步入口。

**场景**：

```rust
#[derive(Debug, Clone, PartialEq)]
struct P { x: i32 }
#[cfg(target_os = "macos")] fn os() -> &'static str { "macos" }
#[must_use] fn compute() -> i32 { 1 }
// println!("{:?} {} {}", p.clone(), p == P{x:1}, os())  ->  P { x: 1 } true macos
// compute();  -> warning: unused return value of `compute` that must be used
```

**要记住的一点**：Rust 的属性不会在运行期留下任何东西，没有 Java 那种「运行时读标签」的路径。所有处理在编译期完成，所以没有额外的运行时成本，也不存在保留策略这类问题。
