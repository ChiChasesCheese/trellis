---
id: hl-c12-virtual-cost
node: cpp-lessons.c12-why-cpp-is-fast
type: qa
step: 7
---
## Q
面试问：虚函数有多慢？怎么避免？
Interview question: How expensive are virtual calls and how do you avoid them?

## A
慢在三点：
1. 一次**间接调用**（读虚表）。
2. **阻止内联**。
3. 目标不稳定时**分支预测失败**。

避免：模板 / CRTP / `std::variant`、按类型分批处理、给类标 `final` 让编译器去虚化。实测随机混合的虚调用约 4 ns/形状，同类型模板 < 0.5 ns。
