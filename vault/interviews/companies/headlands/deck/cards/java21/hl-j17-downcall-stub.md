---
id: hl-j17-downcall-stub
node: java21.j17-ffm-api
type: qa
step: 14
---
## Q
`downcallHandle` 在 JVM 里是怎么实现的？为什么说它取代了 JNI？每次 `MemorySegment` 访问的成本如何？

## A
- JVM 运行时**生成一小段机器码**（桩，stub）做调用约定转换（寄存器传参、栈布局），不需要预编译的 C 胶水代码；一次调用成本与 JNI 同量级或更低。
- 每次 `MemorySegment` 访问做**边界检查 + 生命周期检查 + 线程检查**（`ofConfined`）。JIT 内联后消掉大部分（循环里的边界检查可外提/消除），热路径性能接近原生数组，但**不是零成本**。
- 分配底层是 `malloc`/`posix_memalign`，并保证清零；`close()` 是 `free`。
