---
id: pl-trends-effects-pitfall-guard-across-await
node: trends.effects
type: qa
step: 10
---
## Q
在 Rust 的 `async` 函数里持有 `std::sync::MutexGuard` 并跨过 `.await`，为什么编译器报 future 不能跨线程发送？这说明了效应之间怎样互相干扰？

## A
Rust 的 `async` 块会被编译成一个状态机结构体，**所有跨越 `.await` 仍然存活的局部变量都变成这个结构体的字段**。如果这个 future 要被多线程运行时（tokio 的默认调度器）在线程间搬运，它必须是 `Send`；于是所有字段都必须是 `Send`。

`std::sync::MutexGuard` 不是 `Send`：标准库规定锁必须由加锁的同一线程释放（操作系统的互斥量常常有这个要求）。所以下面的代码被拒绝：

```rust
fn assert_send<T: Send>(_: T) {}
let m = std::sync::Mutex::new(0);
assert_send(async {
    let g = m.lock().unwrap();
    std::future::ready(()).await;   // g is still alive across this await
    drop(g);
});
```

```console
error: future cannot be sent between threads safely
  the trait `Send` is not implemented for `std::sync::MutexGuard<'_, i32>`
note: future is not `Send` as this value is used across an await
  has type `std::sync::MutexGuard<'_, i32>` which is not `Send`
```

编译器还指出了守卫是在哪个 `await` 前被持有的。

这是两种效应相互干扰的典型例子：**「持有锁」**（一种临界区效应）**与「可能挂起」**（`async`）组合。挂起点把线程让给别的任务，可能让另一个任务在同一线程上尝试加同一把锁（死锁）；在多线程运行时里，恢复时还可能换了线程，锁的所有权规则被破坏。Rust 把这个隐患变成了编译错误。

在没有这种检查的语言里，同样的问题在运行时出现：Python 的 `asyncio` 里持有 `threading.Lock` 跨 `await`，另一个任务在同一个事件循环线程上试图加这把锁，整个循环就卡死；Go 里持有 `sync.Mutex` 时阻塞在通道或网络调用上，同样会让所有等这把锁的协程排队，只是编译器和运行时都不会提醒。

对策：

- 缩小临界区，守卫在 `.await` 之前就释放：`{ let mut g = m.lock().unwrap(); *g += 1; }` 之后才 `.await`；
- 必须跨 `await` 持有时，用异步锁（tokio 的 `Mutex`，守卫是 `Send` 的），代价是更慢；
- Python 用 `asyncio.Lock`，不用 `threading.Lock`；Go 里不要在持锁时做通道操作或网络调用。

教训：当语言把效应分开标记时，效应的**组合**才是真正的难题；检查出的每一条组合错误，都对应另一种语言里线上才会出现的问题。
