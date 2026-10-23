---
id: hl-j16-jit-hoisting
node: java21.j16-concurrency-primitives
type: qa
step: 3
---
## Q
`while (!stop) n++;` 里 `stop` 是普通字段，JIT 会怎么优化？为什么这个优化在单线程下完全正确却会破坏多线程？

## A
JIT 看到循环里没人写 `stop`，就把 `stop` 读到寄存器里**只读一次**（循环不变量外提，loop-invariant hoisting）。单线程下这是完全正确的优化；多线程下另一个线程之后写 `stop = true`，循环却永远看不到，永不退出。

编译器和 CPU 都会重排、缓存你的读写，所以需要 `volatile` 这类规则来约束。`volatile` 字段读写会让 JIT 插入内存屏障，并禁止编译器跨屏障重排和缓存。
