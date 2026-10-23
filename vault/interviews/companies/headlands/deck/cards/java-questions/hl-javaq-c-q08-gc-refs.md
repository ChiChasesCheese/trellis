---
id: hl-javaq-c-q08-gc-refs
node: java-questions.c-languages
type: qa
step: 7
---
## Q
Java 的 GC 怎么管内存？有哪几种引用强度（强、软、弱、虚）？为什么不会有 `shared_ptr` 那种循环泄漏？

## A
- **管内存**：GC 从根（线程栈、静态变量等）出发做**可达性分析**，不可达就回收。不需要 `delete`。两个互相引用的 1 MB 对象，丢掉外部引用后照样能回收；`shared_ptr` 在同样结构下会泄漏。
- **引用强度**：强引用（普通）；`SoftReference`（内存紧张时回收，适合缓存）；`WeakReference`（下次 GC 就回收，≈ `weak_ptr`，`WeakHashMap` 用它）；`PhantomReference` / `Cleaner`（回收后的清理回调）。
- 验证：`b = null; System.gc()` 之后 `weak.get() == null`。
