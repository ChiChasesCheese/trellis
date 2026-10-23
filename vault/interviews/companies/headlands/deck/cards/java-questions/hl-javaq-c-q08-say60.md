---
id: hl-javaq-c-q08-say60
node: java-questions.c-languages
type: qa
step: 17
---
## Q
用英文 60 秒回答：C++ has `unique_ptr`, `shared_ptr` and `weak_ptr`. What is the Java equivalent, and how does Java handle ownership and resource cleanup?

## A
结构：内存归 GC（可达性，无循环泄漏）→ WeakReference 对应 weak_ptr → 非内存资源用 try-with-resources → Cleaner 只是兜底 → Java 缺所有权的类型表达。

> "Java doesn't need smart pointers for memory, because the garbage collector traces reachability from roots - so there's no reference counting and no leak from cycles that you get with `shared_ptr`. `WeakReference` is the analogue of `weak_ptr`. The place where RAII matters in Java is non-memory resources like files, sockets and locks, and there we use try-with-resources: `AutoCloseable.close()` runs deterministically at the end of the block, in reverse order, even on exceptions. `Cleaner` exists as a safety net, but it has no timing guarantee, and `finalize` is deprecated for removal. What Java lacks is ownership in the type system - nothing says 'this object belongs to that one'."
