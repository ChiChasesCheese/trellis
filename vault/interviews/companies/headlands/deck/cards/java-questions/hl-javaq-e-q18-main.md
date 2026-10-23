---
id: hl-javaq-e-q18-main
node: java-questions.e-jit-gc
type: qa
step: 1
---
## Q
JIT 是怎么工作的？讲解释器、C1、C2、分层编译（tiered compilation）和 OSR。
How does the JIT work? Explain the interpreter, C1, C2, tiered compilation, and OSR.

## A
一句话：分层编译——tier 0 **解释器**（收集计数）→ tier 1–3 **C1**（快速编译，tier 3 带完整 profiling）→ tier 4 **C2**（用 profile 做激进优化）；热点循环用 **OSR** 在循环中途切换；编译在后台线程完成，完成前继续用旧版本。

- 为什么分层：C2 编译慢但产出快，C1 编译快但产出一般；分层让你**先快速变快，再慢慢变极快**。
- 流程：字节码 → 计数器超阈值 → 编译队列 → 后台线程 → C1 代码（带 profile）→ 更热 → C2 代码。
- **去优化**（deopt）：推测失败，回到解释器 / C1 重新 profile。
