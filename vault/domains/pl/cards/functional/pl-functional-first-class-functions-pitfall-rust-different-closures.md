---
id: pl-functional-first-class-functions-pitfall-rust-different-closures
node: functional.first-class-functions
type: qa
step: 10
---
## Q
Rust 里一个函数在 `if/else` 的两个分支返回不同的闭包，为什么编译失败？怎么修？

## A
每个闭包表达式都有自己唯一的类型，即使两个闭包写得一模一样，类型也不同。`impl Fn(i32) -> i32` 作为返回类型表示「某一个具体的、实现了 Fn 的类型」，所有分支必须返回**同一个**类型：

```rust
fn make(flag: bool, k: i32) -> impl Fn(i32) -> i32 {
    if flag { move |x| x + k } else { move |x| x * k }
}
```

```text
error[E0308]: `if` and `else` have incompatible types
  = note: no two closures, even if identical, have the same type
  = help: consider boxing your closure and/or using it as a trait object
```

修法是用 trait 对象把类型擦掉，付一次堆分配和一次动态分派：

```rust
fn make(flag: bool, k: i32) -> Box<dyn Fn(i32) -> i32> {
    if flag { Box::new(move |x| x + k) } else { Box::new(move |x| x * k) }
}
```

一个容易让人困惑的细节：**没有捕获**的闭包可以自动转成 `fn` 指针，所以 `if flag { |x| x + 1 } else { |x| x * 2 }` 这种不捕获变量的写法其实能通过编译，只要加上 `move` 捕获了变量就不行。这让同样的代码因为是否捕获而时过时不过。

对比 Java：同样的需求在 Java 里没有这个问题，两个 lambda 都是 `Function<Integer, Integer>` 的实例，随意返回。这是 Rust 的静态性与 Java 的运行期统一性的直接体现。
