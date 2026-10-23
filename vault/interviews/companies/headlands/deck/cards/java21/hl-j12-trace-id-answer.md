---
id: hl-j12-trace-id-answer
node: java21.j12-scoped-values
type: qa
step: 20
---
## Q
面试问：「服务怎么在线程间传 traceId？」
(How do you propagate a traceId across threads?) 怎么答？

## A
答案骨架：
- **老办法**：`ThreadLocal` / `MDC`，要处理线程池泄漏和跨线程拷贝（`InheritableThreadLocal` 复制整张表，池线程继承不到）。
- **JDK 21 起**：预览的 **`ScopedValue`**，不可变，随块结束自动解绑。
- 结构化并发的 `fork` 子线程**自动继承**，继承只复制一个快照引用。
- **JDK 25 转正**。

实现：外面套 `ScopedValue.where(TRACE, id).call(() -> mergeAll(...))`，所有 `fork` 出的生产者自动继承，不用改方法签名。
