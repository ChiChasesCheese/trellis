---
id: pl-binding-calling-convention-pitfall-recursion-depth
node: binding.calling-convention
type: qa
step: 10
---
## Q
同一个无限递归（或很深的递归），在 Python、Java、Go、Rust、C++ 里分别怎么失败？哪一种最危险？

## A
递归深度受栈限制，但五门语言的**失败方式**完全不同。

Python：

```python
def down(): global d; d += 1; down()
# RecursionError: maximum recursion depth exceeded     (d = 999)
```

在第 999 层抛出一个普通异常，可以 `try/except` 捕获，进程不受影响。上限是 `sys.getrecursionlimit()`，默认 1000。

Java：

```java
static void down() { depth++; down(); }
// catch (StackOverflowError e): depth = 45024 in one run
```

抛出 `StackOverflowError`（它是 `Error`，不是 `Exception`），实测深度约 4.5 万层，具体数字随栈大小、帧大小和 JIT 状态而变。可以捕获，但捕获后程序状态可能已不一致（锁、半更新的数据），一般只用来记录日志后退出。

Go：深度为五百万的递归（每层加一）正常返回 `10000000`，因为栈会自动增长。无限递归的结局是：

```text
runtime: goroutine stack exceeds 1000000000-byte limit
fatal error: stack overflow
```

这是**致命错误**（fatal error），不是 `panic`，`recover` 抓不住，整个进程退出。而在触顶之前，它会先吃掉接近 1 GB 内存。

Rust：同样的五百万层递归直接失败：

```text
thread 'main' has overflowed its stack
fatal runtime error: stack overflow, aborting
```

进程以 SIGABRT 终止，退出码 134，不能被 `catch_unwind` 捕获。

C++：同样五百万层递归（`-O0`，每层放一个小数组防止被优化掉），栈（本机 8 MB）早已用完，进程被操作系统以 `SIGSEGV`（非法内存访问信号）杀死，退出码 139，没有任何输出。这是未定义行为（标准不规定后果），不保证一定崩溃：栈下面如果恰好有别的可写内存，它会悄悄改写那里。
从危险程度排序：Python 最温和，是一个可处理的异常；Java 次之，是一个可捕获但不应当恢复的错误；Go 先消耗大量内存，再让整个进程崩溃；Rust 立刻中止进程，没有任何恢复机会；C++ 最危险，崩溃只是最好的情形，最坏的是静默破坏数据。

共同的教训是：这类故障通常由**输入**触发（深层嵌套的 JSON、恶意构造的树），所以它是安全问题，不仅是 bug。对策是校验深度、改用显式栈、给解析器设嵌套上限；标准库的 JSON 解析器大多已经有深度限制，自己写递归下降解析器时要自己加。
