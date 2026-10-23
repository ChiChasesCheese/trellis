---
id: hl-c14-deadlock-scoped-lock
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 7
---
## Q
面试问：怎么避免死锁？`transfer(a, b)` 与 `transfer(b, a)` 同时执行，为什么用两个 `lock_guard` 会死锁？怎么修？
Interview question: How do you avoid deadlock?

## A
- 两个线程各持一把锁、等另一把（A→B 和 B→A 顺序）就死锁。
- 修法：`std::scoped_lock` 一次性锁多把，无论参数顺序都用死锁避免算法：

```cpp
void transfer(Account& from, Account& to, long amt) {
    std::scoped_lock lock(from.m, to.m);
    from.balance -= amt; to.balance += amt;
}
```
- 其他手段：全局统一加锁顺序；少持锁、不持锁调用外部代码；超时 `try_lock_for`。
