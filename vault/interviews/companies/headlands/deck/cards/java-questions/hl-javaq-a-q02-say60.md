---
id: hl-javaq-a-q02-say60
node: java-questions.a-speed
type: qa
step: 20
---
## Q
用英文 60 秒回答：You said Java is also compiled. Then what makes C++ faster than other compiled languages, and where does Java sit relative to C++, Go and Rust?

## A
结构：编译本身不决定速度 → 剩余运行时工作与内存布局控制权 → Java/Go 有 GC、Java 对象在引用后面 → 缓存局部性数字 → JIT 追回一部分，结构性差距要等值类型。

> "Compilation by itself doesn't decide speed - what matters is how much runtime work is left and how much control you have over memory. C++ and Rust let you lay data out contiguously, put structs inline in arrays, avoid allocation entirely, and there's no collector. Java and Go have a GC, and in Java almost everything except primitives is a heap object behind a reference, so a list of orders is a list of pointers. That's a cache-locality cost, not an instruction-count cost - in a quick test, summing a shuffled `Long[]` was roughly ten times slower than summing a `long[]`. Java gets some of it back with JIT optimizations that a static compiler can't do, but the memory model is the structural gap until value types arrive."
