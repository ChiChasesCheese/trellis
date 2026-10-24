---
id: pl-binding-calling-convention-foundation-go-stack-abi
node: binding.calling-convention
type: qa
step: 4
---
## Q
Go 1.17 为什么把函数参数从栈改到寄存器？Go 的函数入口为什么要检查栈、栈又怎样增长？

## A
**调用约定的演进。**Go 在 1.16 及以前，参数和返回值都通过栈传递：调用者把它们写进栈，被调用者再读出来。这样简单、对运行时友好，但每次调用都有内存读写。Go 1.17 起在 amd64 上改为**寄存器传参**，后续版本扩展到 arm64 等平台，官方发布说明称典型程序约提速 5%。

实际编译结果（ARM64）里，`add3(a, b, c int) int` 的函数体就是一条 `MADD R1, R0, R2, R0` 和一个 `RET`：参数在 `R0`、`R1`、`R2`，返回值在 `R0`。

**栈检查。**Go 的每个协程（goroutine）从很小的栈起步，所以函数不能假设栈够用。任何调用别的函数的 Go 函数，入口都有这三条指令：

```text
MOVD  16(g), R16    ; load the goroutine's stack limit
CMP   R16, RSP      ; compare with the stack pointer
BLS   morestack     ; too low: grow the stack first
```

`g` 是保存当前协程指针的寄存器，偏移 16 处是栈的下限。叶子函数且栈帧很小时，编译器可以省略这个检查。

**栈增长。**检查失败时调用 `runtime.morestack`：运行时分配一块**两倍大**的新栈，把旧栈的内容**整体复制**过去，同时修正栈里所有指向栈内部的指针，然后重新执行刚才的函数。这叫连续栈（contiguous stack）。更早的「分段栈」（segmented stack）靠链接多个小段来增长，热点循环恰好卡在段边界时会反复分配和释放，造成性能抖动，所以 Go 1.3 起改成了复制。

后果与取舍：

1. 协程栈初始只有几 KB，可以同时存在上百万个协程；栈上的递归深度几乎只受 1 GB 上限（64 位默认）的限制。
2. 复制栈要求运行时能找出栈里的每一个指针并修正它，所以指向栈内部的指针只能存在于同一个栈里，不能被存到堆上或别的协程里（逃逸分析会把这样的变量放到堆上）。
3. 每次调用多三条指令，换来无需预先估算栈大小。
