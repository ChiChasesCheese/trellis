---
id: pl-conc-datarace-pitfall-check-then-act
node: concurrency.data-race-freedom
type: qa
step: 9
---
## Q
Rust 保证安全代码没有数据竞争，是不是说多线程 Rust 就不会出并发 bug？用 `Mutex` 保护余额，为什么仍可能透支？

## A
不是。Rust 阻止的是**数据竞争**（无同步地并发读写同一内存），不阻止**竞态条件**（逻辑上的交错错误）和死锁。每一次访问都被 `Mutex` 保护，也可能是错的：
```rust
let balance = Arc::new(Mutex::new(100i64));
// 8 threads, each:
let enough = *b.lock().unwrap() >= 100;   // lock released at the end of this statement
bar.wait();                                // barrier: widen the window, all threads reach here
if enough { *b.lock().unwrap() -= 100; }   // lock again: the check is stale
```
输出：`balance = -700`。每个线程的检查和扣款各自都在锁里，没有任何数据竞争，类型检查也通过了，但两步之间锁被释放，别的线程已经改了余额。栅栏（`Barrier`）只是让这个窗口必现；没有它，bug 也会在高并发下偶发。

修复：让一次持锁覆盖整个「检查 + 操作」：
```rust
let mut g = b.lock().unwrap();
if *g >= 100 { *g -= 100; }
```
（`MutexGuard` 在 `g` 离开作用域前一直持有锁。）

Rust 不能帮你的几类 bug：
- 竞态条件：检查-再-操作，以及「读两个各自加锁的值再比较」。
- 死锁：两个线程以相反顺序加两把锁；`Mutex` 重复加锁。
- 逻辑上的顺序依赖，例如原子变量的 `Relaxed` 用错。
- 性能问题：所有线程争一把锁。

所以更准确的说法是：Rust 让并发 bug 缩小到「逻辑错误」这一类，不再包含内存损坏。
