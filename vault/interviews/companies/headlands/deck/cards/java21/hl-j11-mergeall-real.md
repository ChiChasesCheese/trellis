---
id: hl-j11-mergeall-real
node: java21.j11-structured-concurrency
type: qa
step: 22
---
## Q
一次性合并 k 路数据流、任一路出错整体失败，如何用 `ShutdownOnFailure` 实现？取消和真正失败怎么区分？

## A
```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure(
        "merge-all", Thread.ofVirtual().factory())) {
    for (int i = 0; i < srcs.size(); i++) {
        final int idx = i;
        scope.fork(() -> {
            try { produce(idx, srcs.get(idx), queues.get(idx)); }
            catch (InterruptedException e) { throw e; }       // 被取消：原样抛
            catch (Exception e) { throw new MergeException(idx, e); }
            return null;
        });
    }
    scope.join();
    scope.throwIfFailed(e -> e instanceof MergeException me ? me : new MergeException(-1, e));
}
```
- 每路一个子任务，另有一个合并子任务；
- `catch (InterruptedException e) { throw e; }` 把「被取消」和「真正失败」分开，子任务让中断异常往外传而不是吞掉；
- `throwIfFailed(Function)` 映射成自己的 `MergeException`；
- 动机：离开 try 块时所有子线程一定已结束，不会泄漏。
