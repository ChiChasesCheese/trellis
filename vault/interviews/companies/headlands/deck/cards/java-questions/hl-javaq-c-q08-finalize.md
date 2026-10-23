---
id: hl-javaq-c-q08-finalize
node: java-questions.c-languages
type: qa
step: 9
---
## Q
Java 的 `finalize()` 和 `Cleaner` 能不能当析构函数用？忘了关流会怎样？为什么 Java 不用引用计数？
What happens if you forget to close a stream? Why not reference counting?

## A
- **`finalize()`**：已弃用且在被移除（JEP 421，Java 18），不要用。
- **`Cleaner`**：只是安全网，**没有时机保证**（要等 GC 才见到清理动作），不能依赖它释放稀缺资源。
- **忘了关流**：文件描述符泄漏，直到 GC 回收对象并跑 Cleaner 才可能关；长时间运行会出现 `Too many open files`。
- **为什么不用引用计数**：有循环问题、每次赋值有开销、多线程下计数要原子操作；GC 批量处理更适合吞吐。
