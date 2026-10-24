---
id: pl-conc-locks-found-rust-mutex
node: concurrency.locks-shared-memory
type: qa
step: 3
---
## Q
Rust 的 `Arc<Mutex<T>>` 是什么？`Arc`、`Mutex`、`lock()` 的守卫（guard）各自解决什么问题？
为什么 4 个线程累加计数器要这样写？

## A
Rust 里想让多个线程修改同一份数据，需要解决两件事：
1. **共享所有权**：多个线程都要“拥有”这份数据，谁最后用完谁释放。普通的值只能有一个所有者。**`Arc<T>`**（Atomic Reference Counted，原子引用计数指针）解决它：`Arc::clone` 只是计数加 1 并返回指向同一份数据的新指针，最后一个指针销毁时数据才释放。
2. **互斥修改**：**`Mutex<T>`** 把数据 `T` **包在锁里面**。要访问数据必须先 `lock()`，它返回一个**守卫**（`MutexGuard`），守卫解引用后就是 `&mut T`；守卫离开作用域时自动解锁。

所以“多线程共享可变数据”的标准组合是 `Arc<Mutex<T>>`：
```rust
let count = Arc::new(Mutex::new(0u64));
let c = Arc::clone(&count);          // one clone per thread
thread::spawn(move || { for _ in 0..1_000_000 { *c.lock().unwrap() += 1; } });
// after joining 4 threads:
println!("{}", *count.lock().unwrap());
```
输出：4 个线程合计 `4000000`（约 126 毫秒，一次测量）。

不加锁让闭包直接借用计数器，则编译失败：
```rust
let mut count = 0;
let hs: Vec<_> = (0..4).map(|_| thread::spawn(|| { count += 1; })).collect();
```
报错：`lifetime may not live long enough ... argument requires that '1 must outlive 'static`。线程可能比 `count` 活得久，借用不被允许。

`lock()` 返回 `Result`（所以要 `unwrap()`）：如果一个线程在持锁时 panic，这把锁会被标记为**中毒**（poisoned），之后的 `lock()` 返回 `Err`，提醒你数据可能处于不一致状态。

对比其他语言：Java、Go、Python 的锁和数据是两个独立的变量；Rust 的数据在锁里面，不拿到守卫就访问不到数据。
