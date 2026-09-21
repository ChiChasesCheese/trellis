---
id: jit-executor-reuse
node: runtime.adaptive-jit
type: qa
source: cpython-internals
---
## Q
JIT 生成的执行器（executor）之后怎么被复用，而不是每次经过这段循环都重新追踪一遍？

## A
执行器被存在触发它的代码对象（code object）的 `co_executors` 数组里，同时原来触发追踪的那条 `JUMP_BACKWARD` 指令被就地替换成 `ENTER_EXECUTOR`，其操作数就是该执行器在数组里的下标。下次执行到这里直接进入执行器，不用重新判断热度或重新追踪；执行器结束后要么回到自适应解释器继续执行，要么经由「side exit」跳转到另一个执行器继续走 JIT 路径。
