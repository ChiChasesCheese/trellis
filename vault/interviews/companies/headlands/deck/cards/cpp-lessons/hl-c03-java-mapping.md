---
id: hl-c03-java-mapping
node: cpp-lessons.c03-smart-pointers
type: qa
step: 14
---
## Q
面试问：Java 里什么东西对应 C++ 的 `shared_ptr`、`weak_ptr`、`unique_ptr`？
Interview question: What are the Java counterparts of C++ smart pointers?

## A
- Java 的普通引用 ≈ 无限 `shared_ptr`，但由 tracing GC 回收，所以**能回收环**；C++ 的引用计数不能。
- `WeakReference` ≈ `weak_ptr`。
- `try-with-resources` ≈ `unique_ptr` + 自定义删除器（资源作用域内独占、离开时释放）。
- 本质区别：Java 里"谁拥有对象"不存在，引用够多就活着，没人引用就回收，回收时机不可预测；C++ 把所有权写进类型，释放时刻确定。
