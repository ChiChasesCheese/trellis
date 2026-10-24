---
id: pl-conc-structured-found-java
node: concurrency.structured-concurrency
type: qa
step: 4
---
## Q
Java 的 `StructuredTaskScope` 是什么？它怎样把子线程限定在一个作用域里，现在是正式特性吗？

## A
`StructuredTaskScope`（`java.util.concurrent`）是 Java 为结构化并发提供的 API：
- 用 `try (var scope = StructuredTaskScope.open()) { ... }` 打开作用域（实现了 `AutoCloseable`，`try-with-resources` 结束时 `close`）；
- `scope.fork(任务)` 在作用域内**为每个子任务启动一个虚拟线程**；
- `scope.join()` 等待子任务，按策略（默认：全部成功才算成功，任一失败就整体失败）决定结果；
- 离开作用域时，如果子任务还在跑，会被取消（中断）。

**状态**：在 JDK 25 里仍然是**预览特性**，需要 `javac --release 25 --enable-preview` 编译、`java --enable-preview` 运行，API 在迭代中（早期版本用的是 `new StructuredTaskScope.ShutdownOnFailure()`）。

实验：A、C 各需 500 毫秒，B 在 100 毫秒后失败：
```java
try (var scope = StructuredTaskScope.open()) {
    scope.fork(() -> work("A", 500, false));
    scope.fork(() -> work("B", 100, true));
    scope.fork(() -> work("C", 500, false));
    scope.join();
} catch (Exception e) {
    System.out.println("caught: " + e);
}
System.out.println("scope exited");
```
（`work` 在被中断时打印 `cancelled` 并抛出 `InterruptedException`。）输出：
```
C cancelled
A cancelled
caught: ...StructuredTaskScope$FailedException: java.lang.IllegalStateException: B failed
scope exited
```
B 失败后，作用域中断 A、C，`join()` 抛出 `FailedException`，`catch` 之后作用域已经退出。

要点：Java 的取消靠**线程中断**（`interrupt`），任务必须在阻塞点响应 `InterruptedException`；这套 API 建立在虚拟线程之上，因为作用域内要开很多子线程，必须便宜。
