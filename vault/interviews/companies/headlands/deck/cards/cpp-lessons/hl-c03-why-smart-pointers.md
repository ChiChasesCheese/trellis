---
id: hl-c03-why-smart-pointers
node: cpp-lessons.c03-smart-pointers
type: qa
step: 1
---
## Q
C++ 为什么需要智能指针（smart pointer）？裸指针 `T*` 表达不出什么？

## A
- C++ 堆对象不会自动回收（Java 靠 GC，C++ 没有）。
- 裸指针 `T*` 看不出：它是**拥有**对象（要负责 `delete`），还是只是**借用**？谁释放、释放几次？答错就是**泄漏**或**双重释放**。
- 智能指针把所有权写进**类型**，并借助 RAII（资源绑定到对象寿命，析构函数自动释放）自动释放。
- 现代 C++ 几乎不写 `new`/`delete`：裸 `new`/`delete` 在异常、提前 `return` 时易泄漏，智能指针让所有权可读、可编译期检查。
- 规则：裸指针不拥有；拥有就用智能指针。
