---
id: hl-j11-custom-policy
node: java21.j11-structured-concurrency
type: qa
step: 14
---
## Q
「尽力从 5 个交易所取价，失败的忽略」内置策略做不到，怎么写自定义策略？补全 `handleComplete`。

## A
继承 `StructuredTaskScope<T>`，重写 `handleComplete(Subtask)`：每个子任务结束时调用一次，你在里面决定收集结果、记录失败、是否 `shutdown()`。

```java
class CollectOk<T> extends StructuredTaskScope<T> {
    Queue<T> ok = new ConcurrentLinkedQueue<>();
    Queue<Throwable> failed = new ConcurrentLinkedQueue<>();
    @Override protected void handleComplete(Subtask<? extends T> st) {
        switch (st.state()) {
            case SUCCESS -> ok.add(st.get());
            case FAILED  -> failed.add(st.exception());
            case UNAVAILABLE -> throw new IllegalStateException();
        }
    }
}
```
示例输出：成功 4 个，失败 1 个。
