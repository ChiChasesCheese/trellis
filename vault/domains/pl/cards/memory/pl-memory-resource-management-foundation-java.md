---
id: pl-memory-resource-management-foundation-java
node: memory.resource-management
type: qa
step: 2
---
## Q
Java 的 try-with-resources 是什么？执行顺序和异常叠加时怎么处理？

## A
Java 里能被“用完关闭”的资源实现 `AutoCloseable` 接口（要求有一个 `close()` 方法）。把它们写在 `try (...)` 的括号里，块结束时（无论正常结束还是抛出异常）语言保证自动调用它们的 `close()`，顺序与打开顺序**相反**：

```java
try (Res x = new Res("A"); Res y = new Res("B")) {
    System.out.println("body");
    throw new IllegalStateException("boom");
} catch (IllegalStateException e) { System.out.println("caught " + e.getMessage()); }
```

```console
open A
open B
body
close B
close A
caught boom
```

后打开的先关，因为后者可能依赖前者。如果块内抛出了异常，同时 `close()` 也抛出异常，`close()` 的异常会附在原异常上（suppressed 列表），原始异常不会丢。

没有这个语法时要手写 `try { ... } finally { x.close(); }`，在多个资源和异常叠加时容易出错（例如 `finally` 里的异常覆盖了原异常）。

要记住的一个事实：try-with-resources 是编译器为你生成 `try/finally`，但调用者必须记得使用它；忘了，资源就泄漏。
