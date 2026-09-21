---
id: jit-hot-loop-tracing
node: runtime.adaptive-jit
type: qa
source: cpython-internals
---
## Q
JIT 怎么判断一段代码「热」（hot）到值得为它生成 trace？判断为热之后发生什么？

## A
执行到 `JUMP_BACKWARD`（循环回跳）或 `RESUME` 指令时，检查其内联缓存里的计数器是否超过阈值来判定是否「热」。一旦判定为热，解释器切换进「追踪模式」，把随后执行的每条字节码指令翻译成微操作（micro-op，简称 uop）序列并记录，同时重置沿途自适应指令的计数器逼它们重新特化，把最新类型信息喂给追踪记录器；追踪按启发式规则结束后，uop 序列交给优化器构造出一个「执行器」（executor）对象。
