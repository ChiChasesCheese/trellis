---
id: pl-errors-exceptions-foundation-checked
node: errors.exceptions
type: qa
step: 2
---
## Q
Java 的受检异常（checked exception）和非受检异常（unchecked exception）是什么？区别在哪里？

## A
Java 所有异常都是 `Throwable` 的子类，按能否被编译器强制分成两类：
- **受检异常**（如 `IOException`）：继承 `Exception` 但不是 `RuntimeException`。方法如果可能抛出它，要么用 `try/catch` 处理，要么在签名里写 `throws IOException` 交给调用者；编译器检查这一点，不满足就拒绝编译。
- **非受检异常**：`RuntimeException` 的子类（`NullPointerException`、`IllegalArgumentException`）和 `Error`。不用声明也不用处理，随时可能抛出。

```java
String s = Files.readString(Path.of("x"));   // may throw IOException
```

```console
error: unreported exception IOException; must be caught or declared to be thrown
```

设计意图：外部世界不可靠，I/O 失败是调用者必须面对的，所以把它写进签名，让编译器保证没人漏掉；而空指针之类是 bug，不该强迫每个调用点处理。

Python、C#、Kotlin 的异常全部是非受检的：不在签名里声明，编译器也不检查。

要记住的一个事实：Java 的受检异常是在语言里强制“失败要在签名中可见”的尝试，其他主流语言基本没有跟进。
