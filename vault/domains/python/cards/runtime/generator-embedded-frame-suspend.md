---
id: generator-embedded-frame-suspend
node: runtime.frames-eval
type: qa
source: cpython-internals
---
## Q
生成器（generator）为什么能在 `yield` 处挂起，之后又从原来的位置恢复执行？

## A
生成器对象把自己的帧直接内嵌在对象结构体里，而不是放在会随调用返回而失效的 per-thread 栈上。执行到 `yield` 时，`YIELD_VALUE` 字节码把值压栈、更新帧的指令指针（instruction pointer）、把解释器的异常状态保存到生成器对象上，再把控制权还给调用者——但帧本身不销毁。下次调用 `send()` 恢复时，解释器从这个内嵌帧保存的指令指针处继续执行。
