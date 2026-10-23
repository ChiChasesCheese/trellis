---
id: hl-hc02-structured-scope
node: problems.hc02-merge-k-streams
type: qa
step: 15
---
## Q
`StructuredTaskScope.ShutdownOnFailure` 解决什么问题？`mergeAll` 怎么用它，限制是什么？

## A
**问题**：传统 `ExecutorService.submit` 得一堆 `Future` 逐个 `get()`；第二个失败时其余仍在跑（甚至永远阻塞），忘关线程池则线程泄漏。结构化并发原则：**谁启动子任务，谁等它们结束**，像 `{ }` 作用域。

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure("merge-all", Thread.ofVirtual().factory())) {
    for (int i = 0; i < srcs.size(); i++) { final int idx = i;
        scope.fork(() -> { try { produce(idx, ...); }
            catch (InterruptedException e) { throw e; }
            catch (Exception e) { throw new MergeException(idx, e); }
            return null; }); }
    var merged = scope.fork(() -> { /* Combiner 阻塞循环 */ });
    scope.join();
    scope.throwIfFailed(e -> e instanceof MergeException me ? me : new MergeException(-1, e));
    return merged.get();
}
```
- 一个生产者失败 → scope 关闭 → **中断**所有兄弟（含卡在 `take()` 的合并任务）；记录**第一个**失败，兄弟因被中断而抛的异常不会覆盖它。
- 离开 `try` 块时所有线程已结束，不可能泄漏；不需要 `Failed` 标记，代码更短。
- 限制：只能一次性合并全部，不能边合并边消费；它在 JDK 21 是**预览** API，需 `--enable-preview`，未来版本可能改。
- 用普通线程池 + `Future.get()` 时，永远阻塞的 source 会让方法挂住。
