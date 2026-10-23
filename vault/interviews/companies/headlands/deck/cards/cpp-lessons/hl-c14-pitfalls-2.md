---
id: hl-c14-pitfalls-2
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 17
---
## Q
C++ 多线程里，关于 `notify` 的时机、`detach` 线程访问局部变量、同一把 `mutex` 重复加锁、`std::thread` 构造失败，各有什么坑？

## A
6. **通知时机**：正确性问题是在改状态**之前**通知；持锁时 `notify` 并立刻等待同一把锁只是性能问题。
7. **`detach` 的线程访问已销毁的局部变量**。
8. **对同一 `mutex` 重复加锁**（不可重入）→ 死锁/UB。
9. **`std::thread` 构造可能抛 `system_error`**（资源不足），线程数不能无限。
