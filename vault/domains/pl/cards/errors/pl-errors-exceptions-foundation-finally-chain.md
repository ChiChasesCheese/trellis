---
id: pl-errors-exceptions-foundation-finally-chain
node: errors.exceptions
type: qa
step: 4
---
## Q
Java 的 `finally` 和异常链（cause）是什么？它们在抛出的过程中怎样表现？

## A
**`finally`**：跟在 `try` 后面的块，无论 `try` 正常结束、抛出异常还是执行了 `return`，都会执行，用于清理。运行顺序：异常抛出后，先在当前方法里执行 `finally`，再继续向上寻找处理器。

```java
static int f() { try { return 1; } finally { System.out.println("cleanup"); } }
```

输出 `cleanup`，返回值仍是 `1`。

**异常链**：捕获一个底层异常后，常常抛出一个更高层的异常，同时把原异常作为 **cause** 带上，`new IllegalStateException("startup failed", e)`。栈追踪里就会出现两段：

```console
Exception in thread "main" java.lang.IllegalStateException: startup failed
	at Ex.start(Ex.java:6)
Caused by: java.io.FileNotFoundException: cfg.yml
	at Ex.load(Ex.java:3)
```

上半段说明应用层发生了什么，下半段（`Caused by`）是根因。没有带 cause，原因就丢了。

C++ 没有 `finally`：清理放在局部对象的析构函数里，展开途中自动运行（RAII）；原因链用 `std::throw_with_nested` 把当前异常嵌进新异常，捕获后再用 `std::rethrow_if_nested` 逐层取出。
异常对象创建时会记录栈追踪：要遍历调用栈的每一帧，所以抛出一次的代价与栈深度成正比。

要记住的一个事实：`finally` 保证清理，cause 链保证根因不丢；两者都依赖你正确使用，不是自动发生的。
