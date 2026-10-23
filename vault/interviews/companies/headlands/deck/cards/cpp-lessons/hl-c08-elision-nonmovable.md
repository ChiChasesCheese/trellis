---
id: hl-c08-elision-nonmovable
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 16
---
## Q
自测：C++17 的保证复制省略为什么让「不可移动类型」能按值返回？

## A
- C++17 起，用**纯右值**（如 `return Pinned(7);`）初始化对象时，**不会创建临时对象**，目标位置直接构造。
- 因此不需要拷贝构造或移动构造函数，连既不可拷贝也不可移动的类型也能这样按值返回。
