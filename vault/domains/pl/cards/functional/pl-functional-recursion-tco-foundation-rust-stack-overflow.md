---
id: pl-functional-recursion-tco-foundation-rust-stack-overflow
node: functional.recursion-tco
type: qa
step: 6
---
## Q
Rust 递归太深会怎样？为什么同一份代码在 debug 下崩溃、在 release 下却可能没事？

## A
Rust 的线程使用操作系统分配的固定栈（主线程通常 8 MB，`std::thread` 创建的线程默认 2 MB，可用 `Builder::stack_size` 调整）。没有 GC，也没有可增长栈。递归过深时，进程收到栈溢出信号，Rust 的运行时打印一条信息后**中止**（abort），不是可以捕获的 panic：

```text
thread 'main' (12652249) has overflowed its stack
fatal runtime error: stack overflow, aborting
```

```rust
fn f(n: u64) -> u64 { if n == 0 { 0 } else { 1 + f(n - 1) } }
f(10_000_000)
```

实测：`rustc`（debug，无优化）下深度 1000 万的调用栈溢出中止；`rustc -O`（release）下同一份代码正常输出 `10000000`。原因是 LLVM 优化器把这个"加 1 再递归"的形式识别为累加循环，改写成了 `while`，根本没有递归调用了。

这引出一个重要事实：**Rust 语言没有保证 TCO，但优化器可能在 release 下替你做**。不能依赖它：debug 构建会崩，改一点写法优化器就认不出来，不同编译器版本的行为也可能变化。要深递归，就显式写成循环或用显式栈，或者给线程开更大的栈。

debug 下每层栈帧也比 release 大得多（没有优化、局部变量都留在栈上），所以同样的代码在 debug 里能递归的深度要小得多。测试通过、上线崩溃的事故，有时就出在这一差异上。
