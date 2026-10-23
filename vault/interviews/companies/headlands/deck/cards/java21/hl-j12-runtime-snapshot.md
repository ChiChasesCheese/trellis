---
id: hl-j12-runtime-snapshot
node: java21.j12-scoped-values
type: qa
step: 12
---
## Q
`ScopedValue` 在运行时是怎么实现的？为什么把绑定继承给子线程比 `InheritableThreadLocal` 便宜？

## A
1. **绑定是不可变的链式结构**：线程里保存的是指向「当前绑定快照」的引用，不是可变表。`where(...).run(...)` 进入 lambda 前把新绑定接在旧快照后形成新快照，退出时恢复旧引用。
2. 快照不可变，所以**继承给子线程只是复制一个引用**，不复制数据，这是比 `InheritableThreadLocal`（整张表复制）便宜的根本原因。
3. **生命周期绑定在调用栈上**：绑定 = 一次 `run`/`call` 的执行期，清理就是方法返回，不存在「忘了清理」。
4. 读取很快：`get()` 有专门的缓存和位图优化，成本与 `ThreadLocal` 相当甚至更低。

子线程继承靠 `StructuredTaskScope.fork` 把当前快照交给新线程。具体数据结构是 JDK 内部实现，可能变化。
