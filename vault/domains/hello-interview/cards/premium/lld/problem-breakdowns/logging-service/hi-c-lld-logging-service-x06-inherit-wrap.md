---
id: hi-c-lld-logging-service-x06-inherit-wrap
node: lld.problem-breakdowns.logging-service.exam
type: qa
step: 9
---
## Q
**日志库 · 继承版本想加缓冲和重试怎么办**｜考点 · 加分

用"抽象 `Destination` + 子类实现 `do_write`"的设计，现在要加缓冲，再要加失败重试，且两者可以叠加。继承版本会变成什么样，组合版本怎么做？

## A
- **继承版本：** 为了复用 `FileDestination` 的文件逻辑，要子类化出 `BufferedFileDestination`；再要重试就是 `RetryingBufferedFileDestination`，要是每种目标都支持，类数量按组合增长，三层继承只为表达"包装"。
- **组合版本：** 缓冲和重试本身也是 `Sink`，只是它们内部包着另一个 `Sink`：`RetrySink(BufferedSink(FileSink(path)))`。叠加顺序是构造参数，各个包装器各管一件事。
- **模式：** 装饰器（Decorator）。因为 `Destination` 只依赖 `Sink` 接口，包装后对它不可见。
- **更本质的原因：** 继承表达"是一种"，包装表达"在外面再加一层行为"；这里的变化是后者。
- **仍要说：** 继承版本在只有两三种目标且不需要包装时更简单，面试里能讲清取舍比记住唯一答案更重要。
