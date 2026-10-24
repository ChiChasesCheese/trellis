---
id: pl-conc-parallel-found-rayon
node: concurrency.parallelism
type: qa
step: 3
---
## Q
Rust 的 rayon 是什么？`par_iter` / `into_par_iter` 怎样把顺序的迭代器变成并行的，它依赖 Rust 的哪些特性来保证安全？

## A
Rust 的**迭代器**（`Iterator`）是惰性的数据流水线：`v.iter().map(f).sum()` 与 Java 的 Stream 类似，编译后通常和手写循环一样快。**rayon** 是社区的数据并行库（不在标准库里，用 `cargo add rayon` 引入），核心是一个工作窃取线程池和一套与标准迭代器形状相同的**并行迭代器**。

用法几乎不变，只把 `iter()` 换成 `par_iter()`，`into_iter()` 换成 `into_par_iter()`：
```rust
use rayon::prelude::*;
let seq: f64 = (0..n).map(f).sum();                  // sequential
let par: f64 = (0..n).into_par_iter().map(f).sum();  // parallel
```
实测（1 亿个元素，`sqrt(i) * sin(i)` 求和，`-O`，一次测量）：顺序 275 毫秒，并行 45 毫秒，约 6.1 倍。

**安全如何保证**：并行迭代器的 `for_each`、`map` 等要求你传入的闭包是 `Fn + Send + Sync`（可被多线程同时调用，且不能独占修改外部变量）。所以：
```rust
let mut out = Vec::new();
(0..100_000).into_par_iter().for_each(|i| out.push(i));
```
编译错误：`error[E0596]: cannot borrow out as mutable, as it is a captured variable in a Fn closure`，提示 “expects Fn instead of FnMut”。要产出集合，用 `collect()`，让库自己并行地收集并合并。

要点：从顺序到并行的改动是一个词，但“**是否正确**”由编译器检查（数据竞争不可能出现），这正是 `Send`/`Sync` 与借用规则的用处。
