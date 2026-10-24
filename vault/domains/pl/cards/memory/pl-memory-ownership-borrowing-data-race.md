---
id: pl-memory-ownership-borrowing-data-race
node: memory.ownership-borrowing
type: qa
step: 6
---
## Q
Rust 的所有权规则怎样顺带消灭了数据竞争（data race）？和 Go、Java 比有什么独特之处？

## A
数据竞争的定义是：两个线程同时访问同一块内存，其中至少一个在写，且没有同步。这正好是「别名且可变」。Rust 的借用规则本来就禁止这种组合，所以同一套规则无需额外机制就能挡住它。

```rust
let mut count = 0;
let h = thread::spawn(|| { count += 1; });
count += 1;
h.join().unwrap();
```

```console
error[E0373]: closure may outlive the current function, but it borrows `count`
help: to force the closure to take ownership of `count`, use the `move` keyword
```

新线程可能比 `main` 的栈帧活得更久，所以借用 `count` 的闭包不合法；就算改成 `move` 把值复制进去，两个线程各改各的副本，也不会相互影响。要共享并修改，必须显式使用同步原语：

```rust
let count = Arc::new(Mutex::new(0));
// each thread: let c = Arc::clone(&count); spawn(move || *c.lock().unwrap() += 1)
// after joining 4 threads: prints 4
```

`Arc` 是跨线程共享的引用计数指针，`Mutex` 是互斥锁，里面包着数据。要访问 `Mutex` 里的数据只能先 `lock()`，不拿锁就拿不到数据，类型系统保证了「锁保护的数据只能在持锁时访问」。

对比：
- Go：只有约定，并发读写同一个变量不会被编译器拒绝，靠 `go run -race` 在运行时检测。
- Java：`synchronized` 与 `volatile` 要自己写对，忘了加锁照样编译。
- Rust 用 `Send`（可以把值移动到另一个线程）与 `Sync`（可以在线程间共享引用）两个标记 trait（不含方法、只做标签的约定）描述「可跨线程移动/共享」，编译器按它们检查。

这是 Rust 独有的：数据竞争在安全代码中不可能出现。死锁和逻辑上的竞态（race condition）仍然可能。
