---
id: pl-functional-closures-foundation-rust-fn-traits
node: functional.closures
type: qa
step: 4
---
## Q
Rust 的 `Fn`、`FnMut`、`FnOnce` 和 `move` 是什么？编译器怎样决定闭包捕获变量的方式？

## A
Rust 闭包不需要声明怎么捕获，编译器看**闭包体怎么使用变量**，选限制最小的方式：

- 只读 → 捕获不可变引用（`&T`）；
- 修改 → 捕获可变引用（`&mut T`）；
- 把值移走（返回、传给别人、`drop`）→ 捕获所有权（move）。

闭包的 trait 随之自动确定：

- **`Fn`**：只读捕获，可以调用任意多次，可同时被共享。
- **`FnMut`**：修改捕获的状态，可多次调用，但调用时需要独占。
- **`FnOnce`**：消耗了捕获的所有权，只能调用一次。

`Fn` 是 `FnMut` 的子集，`FnMut` 是 `FnOnce` 的子集；接受闭包的函数选择最宽松的约束（只调一次就写 `FnOnce`）。

三条典型的编译错误，对应三种破坏：

```rust
let mut push = |s: &str| log.push(s.to_string());  // FnMut，独占借用 log
push("a"); println!("{}", log.len());
// error[E0502]: cannot borrow `log` as immutable because it is also borrowed as mutable

fn twice<F: FnOnce() -> String>(f: F) -> String { f() + &f() }
// error[E0382]: use of moved value: `f`  （FnOnce 只能调用一次）

thread::spawn(|| println!("{}", v.len()));
// error[E0373]: closure may outlive the current function, but it borrows `v`
```

最后一个要加 `move`，强制闭包拿走 `v` 的所有权，这样新线程就不依赖原函数的栈。`move` 并不改变闭包实现哪个 `Fn` trait，只改变**怎么捕获**。
