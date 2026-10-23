---
id: hl-c10-java-new
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 2
---
## Q
Java 的 `new Foo()` 和 C++ 的 `new Foo` 在分配方式和控制权上有什么区别？

## A
- **Java**：在线程私有分配缓冲区（TLAB）里「指针碰撞」分配 + 跑构造函数，分配极快，回收交给 GC。你无法决定对象放在哪里，也无法单独释放。
- **C++**：把「拿内存」和「造对象」**拆开**，并让你完全控制：`malloc` 拿字节，placement new 造对象，自定义分配器/池决定来源。
- 对比：Java 分配快、回收由 GC，代价在 GC 暂停与对象头/指针；C++ 分配可以更慢但完全可控，也能完全避免。
