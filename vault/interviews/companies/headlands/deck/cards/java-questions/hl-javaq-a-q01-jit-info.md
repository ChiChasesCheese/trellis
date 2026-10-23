---
id: hl-javaq-a-q01-jit-info
node: java-questions.a-speed
type: qa
step: 3
---
## Q
HotSpot 的 JIT 相比 C++ 静态编译器，优势在"信息"上。具体能利用哪些运行时信息？逃逸分析（escape analysis）开关对分配量和耗时有多大影响？

## A
JIT 的优势是**信息**：C++ 编译器不知道某个接口调用点运行时是哪个实现类；HotSpot 看到"这个调用点只见过一种类型 `Sq`"，就直接内联 `Sq.area`，并留一个陷阱（uncommon trap）防止猜错。这等于自动、在线的 profile 引导优化（PGO）。

要点：
- **逃逸分析**：证明对象不会跑出方法，就不分配，字段拆进寄存器。同一段代码：开启时稳态分配 **0 字节**、约 **48 ms**；`-XX:-DoEscapeAnalysis` 关掉后分配 **4,800,000,000 字节**、约 **386 ms**，慢约 8 倍。
- **内联 + 去检查**：循环里的边界检查常被提到循环外（range check elimination）；空指针检查用"出了信号再处理"的隐式检查，热路径几乎无开销。
- 运行时 profile 例子：调用点只见过 1 种类型；某分支 99.9% 不走。
