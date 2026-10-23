---
id: hl-j11-handlecomplete-threadsafe
node: java21.j11-structured-concurrency
type: qa
step: 15
---
## Q
自定义 `StructuredTaskScope` 策略时，`handleComplete` 在哪个线程里运行？这对收集结果的容器有什么要求？

## A
`handleComplete` 在**子线程**里被调用，多个子任务完成时会**并发**执行，所以收集结果的容器必须线程安全，例如 `ConcurrentLinkedQueue`。内置策略用 `AtomicReference` 之类保证安全，自己写时同样要保证。

这是自定义策略比内置策略难的地方：并发安全由你负责。
