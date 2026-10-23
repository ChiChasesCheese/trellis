---
id: hl-j12-request-context-code
node: java21.j12-scoped-values
type: qa
step: 15
---
## Q
把请求上下文（traceId、账户）传给结构化并发的子任务，不改任何方法签名：写出声明、绑定和 `fork` 的核心代码。

## A
```java
record RequestContext(String traceId, String account) {}
static final ScopedValue<RequestContext> CTX = ScopedValue.newInstance();

static void handleOrder() throws Exception {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        Subtask<Long> q = scope.fork(Svc::fetchQuote);  // 子线程继承 CTX
        Subtask<Long> l = scope.fork(Svc::fetchLimit);
        scope.join().throwIfFailed();
    }
}
ScopedValue.where(CTX, new RequestContext("t-001", "ACC-7"))
           .call(() -> { handleOrder(); return null; });
```
深层 `log(msg)` 不接受上下文参数，却用 `CTX.isBound() ? CTX.get() : null` 知道自己在服务哪个请求。值用 `record`（不可变）。
