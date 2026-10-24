---
id: pl-conc-locks-unique-rust-mutex
node: concurrency.locks-shared-memory
type: qa
step: 7
---
## Q
Rust 的 `Mutex<T>` 为什么把数据放在锁里面？守卫（guard）和「锁中毒」（poisoning）各是什么？

## A
在 Java、Go、Python 和 C++ 标准库的 `std::mutex` 里，锁和它保护的数据是两个独立的变量，「哪把锁保护哪份数据」只存在于注释和程序员脑中，忘了加锁照样编译、照样运行。Rust 的 `Mutex<T>` 把数据 `T` 包在锁里面：不加锁根本拿不到数据。

```rust
let m = Mutex::new(vec![1, 2, 3]);
m.push(4);
```
编译错误：`error[E0599]: no method named push found for struct Mutex<T>`，提示 `push` 在 `Vec<i32>` 上。必须先 `lock()`：

```rust
{
    let mut g = m.lock().unwrap();   // MutexGuard<Vec<i32>>
    g.push(4);
}                                    // guard dropped: unlock
```
`lock()` 返回**守卫**对象 `MutexGuard`，它解引用成 `&mut T`；守卫离开作用域时在 `Drop` 里自动解锁，无法忘记。借用检查器还保证守卫存活期间之外拿不到 `&mut T`。

**锁中毒**：如果一个线程持有守卫时 panic，数据可能只改了一半。Rust 把这把锁标记为中毒，之后别人的 `lock()` 返回 `Err(PoisonError)`：
```
thread panicked: true
is_poisoned: true
lock() = Err(PoisonError), data still readable: [1, 2, 3, 4]
```
调用方必须决定：`unwrap()` 让自己也 panic，或用 `e.into_inner()` 取回数据继续。Java 的 `synchronized`、Go 的 `Mutex` 没有这个概念，线程异常退出后别人拿到的是可能不一致的数据，而且不会收到任何提示。

这是 Rust 的独到点：把「锁住了才能访问」做成类型规则。C++ 的守卫（`lock_guard`，析构时解锁）与它同源，但 C++ 的守卫不管数据：数据放在锁外，仍可不加锁就读写；第三方库（folly 的 `Synchronized<T>`）才复刻了这一设计，标准库没有。
