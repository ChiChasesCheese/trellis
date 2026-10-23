---
id: hl-hc03-call-stack
node: problems.hc03-recursive-sum
type: qa
step: 2
---
## Q
调用栈（call stack）与栈帧（stack frame）是什么？递归求和 `sum(n)` 的栈深是多少？栈满了 Java 和 C++ 分别会怎样？

## A
每个线程有一块专用内存叫调用栈。每次调用函数就在栈顶压入一个栈帧，存参数、局部变量、返回地址；返回时弹出（后进先出，LIFO）。

`sum(3)` 最深时栈上有 `sum(0)`（栈顶）、`sum(1)`、`sum(2)`、`sum(3)`、`main`。**递归求和同时存在 n+1 个栈帧，栈深 = n**。每帧几十到上百字节，栈总大小有限。

- **Java**：栈满抛 `StackOverflowError`。它是 `Error` 不是 `Exception`：JVM 资源耗尽，非业务错，可以 catch，但只该用来**测量**，业务上不该靠它兜底，也不能吞成 0。默认每线程栈约 1 MiB（`-Xss` 可改）；给新线程指定栈大小：`new Thread(null, runnable, "name", 64L * 1024 * 1024)`，第四个参数只是提示。
- **C++**：越过栈末尾的保护页，进程收到 `SIGSEGV` 直接死，**没有异常可抓**。量深度要在离栈末尾还有约 32 KiB 时停下（用 `__builtin_frame_address(0)` 算已用字节），确认会爆栈只能放子进程验证。macOS 主线程栈 8 MiB，其他线程 512 KiB。
