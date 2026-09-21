---
id: function-vs-generator-frame-return
node: runtime.frames-eval
type: qa
source: cpython-internals
---
## Q
普通函数调用和生成器函数调用，两者的帧「把控制权还给调用者」这件事有什么本质区别？

## A
普通函数的帧只会把控制权还给调用者一次——一旦 `return`，帧立刻被销毁。生成器函数的帧可以多次把控制权还给调用者：每执行到一次 `yield` 就通过 `YIELD_VALUE` 「返回」一次，但帧不销毁、状态保留在生成器对象里，直到下一次 `send()` 才恢复执行——所以生成器可以理解成一个能被反复挂起/恢复的特殊函数调用。
