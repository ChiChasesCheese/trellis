---
id: hl-javaq-c-q08-main
node: java-questions.c-languages
type: qa
step: 5
---
## Q
C++ 有 `unique_ptr`、`shared_ptr`、`weak_ptr`。Java 里对应什么？Java 怎么处理所有权和资源清理？
C++ has unique_ptr, shared_ptr and weak_ptr. What is the Java equivalent, and how does Java handle ownership and resource cleanup?

## A
一句话：Java 没有所有权概念。**每个引用都像 `shared_ptr`，但由 GC 追踪可达性而不是引用计数，所以没有循环引用泄漏**；`WeakReference` ≈ `weak_ptr`；RAII 对应 **try-with-resources**（`AutoCloseable`）；`Cleaner` 是兜底，不是析构函数。

要说的点：
- 内存归 GC；文件、socket、锁等**其他资源**必须显式关闭。
- 最接近 `unique_ptr` 的用法：把资源包在 `AutoCloseable` 里，在作用域内使用。
- Java 缺的是"这个对象归谁"的类型表达，靠约定和 try-with-resources。
