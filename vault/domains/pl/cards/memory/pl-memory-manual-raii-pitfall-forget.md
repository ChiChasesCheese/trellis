---
id: pl-memory-manual-raii-pitfall-forget
node: memory.manual-raii
type: qa
step: 9
---
## Q
RAII 能保证资源一定被释放吗？Rust 里有哪些情况下 `Drop` 不会运行？

## A
不能。RAII 保证的是「值被销毁时一定运行析构」，而不是「值一定会被销毁」。在 Rust 里，以下情况 `Drop` 不运行：

1. 显式调用 `std::mem::forget(x)`，它是安全函数。
2. 引用计数循环：两个 `Rc`（引用计数的共享指针） 互相持有，计数永远不归零。
3. 进程以 `abort` 结束，或 `panic = "abort"` 配置下发生 panic，不展开栈。
4. `std::process::exit` 直接结束进程，不会运行剩余局部变量的析构。

演示 `forget`：

```rust
let a = Noisy("a");
let b = Noisy("b");
std::mem::forget(a);
let _ = b;
println!("end");
```

```console
end
drop b
```

`drop a` 从未出现：`a` 的资源被泄漏了，但程序完全合法，内存安全不受影响。

实践含义：
- 不要依赖 `Drop` 做「必须执行」的业务动作（如提交事务、写日志收尾），应写成显式调用，`Drop` 只做兜底清理。
- 泄漏在安全 Rust 中是允许的；要避免泄漏，对循环结构使用 `Weak`。
- 在 C 中同类问题更严重：提前 `return` 忘记 `free`，没有任何东西兜底。
