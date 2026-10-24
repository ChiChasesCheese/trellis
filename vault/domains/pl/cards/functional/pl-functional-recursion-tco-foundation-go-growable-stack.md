---
id: pl-functional-recursion-tco-foundation-go-growable-stack
node: functional.recursion-tco
type: qa
step: 5
---
## Q
Go 的 goroutine 栈为什么能递归很深？栈溢出时会发生什么，能不能 `recover`？

## A
Go 的每个 goroutine 一开始只有很小的栈（约 2 KB），函数入口的序言代码会检查剩余空间，不够就**分配一块更大的栈（通常翻倍），把旧栈的内容复制过去，调整其中的指针，然后继续执行**。这叫可增长栈（growable stack），上限默认 1 GB（64 位系统）。

所以 Go 里深递归基本不是问题：

```go
func f(n int) int { if n == 0 { return 0 }; return 1 + f(n-1) }
f(10_000_000)    // 一千万层：输出 10000000，正常
f(50_000_000)    // runtime: goroutine stack exceeds 1000000000-byte limit
                 // fatal error: stack overflow
```

超过 1 GB 上限时是 **`fatal error`**，不是 panic：**无法用 `recover` 捕获，整个进程直接退出**。原因：栈已经没法再增长，运行时连"运行 recover 的 defer 链"的空间都没有，所以只能终止。

这个设计使得 Go 可以同时开几十万个 goroutine（每个只占几 KB），又允许需要时深递归；代价是：栈增长时要复制整块栈，因此运行时必须精确知道栈上哪些位置是指针（栈映射），这限制了 Go 与 C 的互操作（cgo 调用在专用的系统栈上执行），也让个别函数调用偶尔出现一次复制的延迟抖动。

对比：Java 的线程栈是固定大小、不能增长，要么一开始就开很大（浪费），要么冒溢出的风险；Go 的方案把"栈大小"这个参数从程序员那里拿走了。
