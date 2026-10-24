---
id: pl-errors-panics-foundation-rust
node: errors.panics
type: qa
step: 3
---
## Q
Rust 的 `panic!` 会发生什么？展开（unwind）和中止（abort）有什么区别？

## A
`panic!`、`unwrap()` 遇到 `None`/`Err`、数组越界都会触发 panic：先打印消息和位置（如 `index out of bounds: the len is 0 but the index is 0`），然后选择两种方式之一终止：

- **展开**（unwind，默认）：从 panic 处向上逐层退出，沿途对每个作用域里的值执行 `Drop`（释放资源、解锁），最后终止**当前线程**。主线程 panic 则进程以状态码 101 退出。可以用 `std::panic::catch_unwind` 拦截，但不是为常规错误处理设计的。
- **中止**（abort）：在 `Cargo.toml` 设 `panic = "abort"`，panic 时直接终止整个进程，不展开，不运行 `Drop`；二进制更小，本机实测退出码 134（SIGABRT）。

线程是隔离的：子线程 panic 只让该线程终止，`join()` 返回 `Err`，主线程可以决定怎么办。

```rust
let r = std::panic::catch_unwind(|| { let v: Vec<i32> = vec![]; v[0] });
println!("caught: {}", r.is_err());     // caught: true
let x: Option<i32> = None;
x.expect("config must have port");      // panics with this message
```

`expect("...")` 比 `unwrap()` 好：panic 信息里带着你写的理由，说明你为什么认为这里不会失败。

要记住的一个事实：Rust 的 panic 默认是线程级的、会清理资源的终止；可以选择更激进的 abort。
