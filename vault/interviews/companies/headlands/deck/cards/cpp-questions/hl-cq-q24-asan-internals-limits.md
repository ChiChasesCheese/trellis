---
id: hl-cq-q24-asan-internals-limits
node: cpp-questions.f-ub-debug
type: qa
step: 9
---
## Q
三个追问：ASan 怎么工作？sanitizer 能证明代码正确吗？生产环境崩溃时先用什么？

## A
- **原理**：用影子内存（shadow memory）记录每个字节是否可访问；给每次分配前后加被“毒化”的红区（redzone）；插桩的读写先查影子内存。
- **不能证明正确**：只能报告实际执行到的路径上的 bug。
- **生产崩溃**：先用 core dump + 调试器；再在测试环境用 ASan / TSan 复现。
