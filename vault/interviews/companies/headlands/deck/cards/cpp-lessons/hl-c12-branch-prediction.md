---
id: hl-c12-branch-prediction
node: cpp-lessons.c12-why-cpp-is-fast
type: qa
step: 8
---
## Q
机制四：分支预测怎样影响性能？同一个循环，数据随机 vs 已排序，差多少？C++ 让你能控制什么？

## A
```cpp
for (int x : v) { if (x >= 128) { t += x; out.push_back(x); } }
```
- 随机数据：2.39 ns/元素；已排序：0.378 ns/元素，随机约 **6 倍慢**。
- 原因：随机数据下 `if` 一半对一半错，**分支预测器失败**。
- C++ 让你控制：数据顺序、无分支写法、`alignas(64)` 对齐、预分配避免 `malloc`、`__builtin_prefetch`、SIMD 内建函数、线程绑核——这些在 JVM 之上要么不可能要么需要绕路。
