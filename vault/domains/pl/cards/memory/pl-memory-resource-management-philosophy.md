---
id: pl-memory-resource-management-philosophy
node: memory.resource-management
type: qa
step: 4
---
## Q
Rust 把资源绑定在类型上，Go 却用函数级的 `defer`。这两种做法分别反映了什么设计哲学？

## A
**Rust：让错误用法无法表达。** 资源是一个值，拿着这个值就持有资源，值被丢弃就释放资源。锁是最好的例子：`Mutex<T>` 把数据和锁绑在一起，只有拿到 `MutexGuard` 才能访问数据，`Guard` 离开作用域自动解锁。

```rust
{
    let mut g = m.lock().unwrap();   // lock acquired
    g.push(2);
}                                    // g dropped: lock released
```

执行后 `try_lock()` 成功，说明锁已经释放；而在 `g2` 活着的时候 `try_lock()` 返回错误。你甚至无法在不持锁的情况下访问被保护的数据，也就没有「忘记解锁」或「没锁就访问」这两类 bug。Java 里 `synchronized` 或 `ReentrantLock` 与数据的关系只存在于注释和约定中。

**Go：简单、显式、可读。** `defer` 是一条语句，读代码时「获取」和「释放」相邻出现，一目了然，不需要理解类型的析构规则。Go 愿意用较弱的保证（可能忘记写）换取语言的小和代码的直观：

```go
f, err := os.Open(name)
if err != nil { return err }
defer f.Close()
```

另一个体现是错误处理：`Close()` 的错误是显式返回值，由你决定是否检查，而 Rust 的 `Drop` 无法把错误交给调用者。

**Java 与 Python：用语法糖补 GC 的缺口。** try-with-resources 和 `with` 是在已有的对象模型之上加的块级语法，不改变对象的模型，维持语言的向后兼容。

一句话：Rust 追求「编译期杜绝」，Go 追求「读起来清楚」，Java 与 Python 追求「在现有模型上能用」。
