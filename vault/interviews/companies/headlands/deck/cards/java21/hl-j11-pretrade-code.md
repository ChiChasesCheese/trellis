---
id: hl-j11-pretrade-code
node: java21.j11-structured-concurrency
type: qa
step: 12
---
## Q
下单前并行取行情、风控额度、合约参考数据，任一失败则整体失败并取消其他，整体最多等一个 deadline。写出 JDK 21 的代码。

## A
```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure(
        "pretrade", Thread.ofVirtual().factory())) {
    Subtask<Quote>      q = scope.fork(() -> quote());
    Subtask<Limit>      l = scope.fork(() -> risk());
    Subtask<Instrument> i = scope.fork(() -> refdata());
    scope.joinUntil(Instant.now().plus(deadline)).throwIfFailed();
    return new PreTrade(q.get(), l.get(), i.get());
}
```
关键：有名字的 scope + 虚拟线程工厂；`joinUntil` 给整体截止时间；`throwIfFailed()` 在有失败时抛出；最后 `get()` 取三个结果。
