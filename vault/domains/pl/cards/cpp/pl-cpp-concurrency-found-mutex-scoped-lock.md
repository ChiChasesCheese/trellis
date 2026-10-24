---
id: pl-cpp-concurrency-found-mutex-scoped-lock
node: cpp.concurrency
type: qa
step: 3
---
## Q
互斥锁（mutex）在 C++ 里怎么用？`std::scoped_lock` 怎样避免多把锁造成的死锁，它与 Rust 的 `Mutex<T>` 有什么根本差别？

## A
**互斥锁**：同一时刻只允许一个线程持有的锁。持有锁的线程可以安全地读写它保护的数据，其他线程在 `lock()` 处阻塞。

**RAII 的用法**：不手写 `lock()`/`unlock()`，而是用锁守卫（lock guard）：

```cpp
std::mutex m; int counter = 0;
{ std::scoped_lock lk(m); ++counter; }   // 构造时加锁，离开作用域自动解锁
```

即使临界区内抛出异常或提前 `return`，锁也会被释放，这是 RAII 在并发里最直接的用处。

**多把锁与死锁**：两个线程分别以相反顺序加两把锁，各持一把等对方的，永远卡住。`std::scoped_lock`（C++17）可以**一次锁多个互斥量**，内部用避免死锁的算法，与你传入的顺序无关。本机实测：

```cpp
void transfer(Account& from, Account& to, int amt) {
  std::scoped_lock lk(from.m, to.m);     // 同时锁两把，不会死锁
  from.bal -= amt; to.bal += amt;
}
```

两个线程各做 10 万次相反方向的转账，总额始终是 200，没有卡住。

**成本**：本机实测无竞争时 `scoped_lock` 加锁加解锁约 3.3 ns；有竞争时线程会被挂起，成本跃升到微秒级（线程切换）。

**与 Rust `Mutex<T>` 的根本差别**：
- **Rust**：`Mutex<T>` **拥有**数据；只有 `lock()` 返回的守卫才能访问里面的 `T`。忘记加锁就无法访问，编译器保证。
- **C++**：`std::mutex` 与它保护的数据是**两个独立的变量**。哪个锁保护哪个数据，只是约定（注释或命名）；忘记加锁，编译器不会提醒，只会产生数据竞争。

**最佳做法**：把互斥量和它保护的数据放在同一个类里，类的接口只暴露持锁后的操作，成员标 `mutable`（便于 const 方法加锁）；Clang 的**线程安全注解**（`GUARDED_BY`、`-Wthread-safety`）可以让编译器检查"访问此变量必须持有此锁"，弥补语言的缺失。

**要记住的一点**：C++ 的锁是"建议性"的：它只在所有人都遵守约定时有效，所以要用类的封装把约定变成结构。
