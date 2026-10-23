---
id: hl-j19-q4-jit-warmup
node: java21.j19-runtime-zgc-jit
type: qa
step: 37
---
## Q
面试问：什么是 JIT 预热？上线前怎么处理？
What is JIT warm-up and how do you handle it before going live?

## A
- JVM 起步在**解释器**，热方法才被编译：先 **C1（带剖析）**，再 **C2（激进优化，如内联、逃逸分析）**；
- 在那之前延迟是稳态的数倍，玩具方法实测约 **6 倍**（801.7 ns 对 123 ns）；
- 对策：上线前用**回放流量预热**，让关键路径完成 C2 编译，再接真实订单；
- 保持调用点**单态**，避免投机内联后被去优化。

英文骨架：「Interpreter first, then C1 with profiling, then C2. I'd warm critical paths with replayed traffic before taking real orders and keep call sites monomorphic.」
