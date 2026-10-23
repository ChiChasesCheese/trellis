---
id: hl-j16-varhandle-static-final
node: java21.j16-concurrency-primitives
type: qa
step: 18
---
## Q
为什么 `VarHandle` 必须声明为 `static final`？

## A
JIT 知道它是**常量**，才能把整个访问内联成一条机器指令。放在普通字段或局部变量里会走较慢的通用路径，这是最容易被忽略的性能前提。

访问方法需强转返回值，类型错误在运行时才抛 `WrongMethodTypeException`/`ClassCastException`。`compareAndSet` 本身是 intrinsic，被 C2 直接编译成 CPU 原子指令。
