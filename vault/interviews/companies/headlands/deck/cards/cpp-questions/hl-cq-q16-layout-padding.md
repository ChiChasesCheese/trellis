---
id: hl-cq-q16-layout-padding
node: cpp-questions.c-memory-ownership
type: qa
step: 30
---
## Q
面试题：`sizeof`、`alignof` 和填充（padding）是什么意思？你怎么给一个热路径结构体设计布局？
What do `sizeof`, `alignof` and padding mean? How would you lay out a hot struct?

## A
- CPU 要求每种类型放在**对齐的地址**上，编译器在成员之间插**填充**，整个结构体大小补齐到最大对齐的倍数。
- 把**大的成员放前面**可以消除多余填充；`alignas(64)` 让对象独占一条缓存行。
- 热路径结构体的原则：
  - 常用字段放在一起；
  - 大成员放前面；
  - 总大小尽量 ≤ 一条缓存行（64 字节）；
  - 不同线程写的字段放不同缓存行（避免伪共享）；
  - 用 `<cstdint>` 的定宽类型。
