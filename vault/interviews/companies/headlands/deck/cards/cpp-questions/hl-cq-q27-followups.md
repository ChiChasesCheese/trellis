---
id: hl-cq-q27-followups
node: cpp-questions.f-ub-debug
type: qa
step: 26
---
## Q
三个追问：只在 Release 版崩溃且没有调试器怎么办？`assert` 在 Release 构建里做什么？什么是 watchpoint？

## A
- **Release 崩溃**：拿 core dump 和符号，看 backtrace；重新用 `-O2 -g` 构建，既保留优化又有行号。
- **`assert` 在 Release**：定义了 `NDEBUG` 就什么也不做，所以永远别放副作用。
- **Watchpoint**：对内存写入的硬件辅助断点，用来找出谁破坏了某个变量。
