---
id: pl-memory-substructural-types-best-practice
node: memory.substructural-types
type: qa
step: 10
---
## Q
资深工程师怎样利用「值只用一次」的思想设计 API？在 Rust 里和在没有仿射类型的 Go、Java、Python 里各怎么做？

## A
原则：**如果一个操作使得对象的旧状态失效，就让这个操作消耗对象；如果语言做不到，就用命名和作用域模拟。**

**Rust**
- **让转换方法按值接收 `self`**：`build(self)`、`finish(self)`、`into_inner(self)`、`close(self)`。调用之后原对象不能再用，状态错误在编译期可见。
- **用类型状态表达必须遵守的协议**（连接、事务、构造器）：状态是类型参数，转换返回新类型。协议少于五六个状态时值得；状态过多或可任意转换时改用枚举加运行时检查。
- **给携带责任的类型加 `#[must_use]`**：守卫、构造器、`Result` 风格的类型；不要为了消除警告而到处写 `let _ =`。
- **不要依赖 `Drop` 做安全性保证**，因为泄漏在安全代码里是允许的；`Drop` 做清理，不做正确性的最后防线。
- **不用 `Clone` 绕开所有权**：每次 `.clone()` 都问一遍是否可以改成借用或调整所有权。

**Go**
- 用 `defer f.Close()` 紧跟在获得资源之后，让获取和释放成对出现；不要把需要关闭的对象存进长寿命结构又不提供 `Close`。
- 需要「用完即废」的语义时，让方法在内部记录状态并拒绝再次使用（返回 `ErrClosed`）；`sync.Once` 保证只执行一次。

**Java**
- 一律使用 `try-with-resources`，把需要关闭的类型实现 `AutoCloseable`；构造器返回的对象若有生命周期，文档写明谁关闭。
- 设计「用一次」的对象（如构造器）：`build()` 之后把内部状态置空，再调用抛 `IllegalStateException`。

**Python**
- 用 `with`、`contextlib.contextmanager` 包装获取与释放；生成器和一次性迭代器明确标注「只能迭代一次」。

通用规则：能让错误用法**无法表达**（类型），就不要只让它**被检测到**（异常），也不要只是**被文档禁止**。
