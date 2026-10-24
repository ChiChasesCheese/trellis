---
id: pl-errors-exceptions-pitfall-finally
node: errors.exceptions
type: qa
step: 9
---
## Q
`finally` 里写了 `return`，或者 Python 里 `except` 得太宽，会怎样悄悄吞掉错误？

## A
**Java：`finally` 里的 `return` 会覆盖异常。**

```java
static int g() {
    try { throw new RuntimeException("x"); }
    finally { return 2; }          // the exception is silently discarded
}
```

调用 `g()` 返回 `2`，没有任何异常，也没有任何日志。`finally` 是为了清理而设计的，不要在里面 `return`、`break` 或抛出新的异常。（只有加 `javac -Xlint:finally` 才会得到 `finally clause cannot complete normally` 的警告，默认不提示。）

对照：正常的清理型 `finally` 不改变结果。

```java
static int f() { try { return 1; } finally { System.out.println("cleanup"); } }
```

输出 `cleanup`，返回值仍是 `1`。

**Python：过宽的 `except`。**

```python
try:
    run()
except Exception:      # swallows every bug, including typos
    pass
```

这会把 `NameError`、`TypeError` 这类程序错误一并吞掉，程序带着错误状态继续运行。更糟的是裸 `except:`，它还拦住了 `Ctrl+C`（`KeyboardInterrupt`）和 `sys.exit()`（`SystemExit`），进程无法被正常终止。

**共同点**：异常机制把错误路径藏了起来，所以一旦在路径上有人把它吞掉，没有人会知道。防护措施：
- linter 开启 `bare-except`、`broad-except`、`finally-return` 之类的规则；
- 捕获后至少记录一次日志，或重新抛出；
- 代码评审时看到空 `catch` 就追问理由。
