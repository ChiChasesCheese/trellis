---
id: hl-cq-q11-script
node: cpp-questions.c-memory-ownership
type: qa
step: 6
---
## Q
用英文 60 秒回答：What is RAII, and how does it replace `finally` / try-with-resources? Where do objects live: stack, heap, static?

## A
结构：RAII 定义与逆序析构 → 为什么不需要 `finally`（锁/文件/`unique_ptr`，异常中途仍释放）→ 零法则/五法则、析构不抛 → 对比 Java 是自动的。

- **RAII** means the constructor acquires a resource and the destructor releases it, and destructors are guaranteed to run, in **reverse order of construction**, when the scope exits - whether normally or by exception.
- That's why C++ has no `finally`: a `lock_guard` unlocks the mutex, a file handle closes the file, a `unique_ptr` frees memory. In my test, throwing in the middle still closed the file and released the lock.
- Practical rules: follow the **Rule of Zero** - build classes from standard RAII members; if I do own a resource I implement or delete all **five** special members. Destructors must not throw.
- Compared with Java's try-with-resources it's automatic and enforced by the type, not by the caller's discipline.
