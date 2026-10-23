---
id: hl-j19-loop-opts
node: java21.j19-runtime-zgc-jit
type: qa
step: 27
---
## Q
除了内联、去虚化、逃逸分析，JIT 的循环优化有哪些？

## A
**循环优化与边界检查消除**：展开循环（loop unrolling）、把数组下标检查外提；对 `long` 计数循环尤其明显。

前面还有：
- 把循环不变量外提（loop-invariant hoisting），这也是普通字段 `stop` 在多线程下不可见的原因；
- 内联让后面的常量折叠、循环优化看到更大的代码块。
