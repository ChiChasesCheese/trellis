---
id: pl-memory-stack-heap-foundation-thread-stacks
node: memory.stack-heap
type: qa
step: 4
---
## Q
每个线程各有一个调用栈：Java 线程、Rust 与 C++ 线程和 Go 的 goroutine 的栈有什么不同？

## A
线程（thread）是操作系统调度的执行单元，每个线程有自己独立的调用栈，因此函数调用互不干扰。栈的大小是一个重要的设计参数：

- **Java 线程、Rust 线程（`std::thread`）**：对应一个操作系统线程，创建时就保留一块固定大小的栈（Java 默认约 1 MB 量级，可用 `-Xss` 调；Rust 主线程通常 8 MB，`thread::spawn` 的线程默认 2 MiB）。用满就溢出，Java 抛 `StackOverflowError`，Rust 直接终止进程。
- **C++ 线程（`std::thread`）**：同样对应一个操作系统线程，栈大小固定，由系统和线程属性决定（主线程通常 8 MB）；溢出是未定义行为（标准不规定后果），实际表现为段错误，进程被终止，不能捕获。
- **Go 的 goroutine**：Go 运行时调度的轻量“协程”，一个程序里可以有几十万个。它的栈从很小（KB 量级）开始，函数入口检查剩余空间，不够就换成一块更大的连续内存并把旧栈内容复制过去，称为可增长栈（growable stack）。上限默认 1 GB（64 位）。
- **Python**：解释器的调用深度由 `sys.getrecursionlimit()`（默认 1000）限制，超过抛 `RecursionError`，防止 C 栈真的崩溃。

一个小场景：同一个每层加 1 的递归函数，在 Go 里递归 1000 万层可以正常返回；在 Java 默认栈上约 4.4 万层就 `StackOverflowError`；在 Python 里 1000 层就 `RecursionError`（均为本机一次实测）。

要记住的一个事实：**栈是固定上限的资源**，是否可增长，决定了一门语言能开多少并发任务、能递归多深。
