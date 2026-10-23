---
id: hl-c08-compiler-support
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 18
---
## Q
在 CoderPad 之类的在线环境里用 C++20 特性前要注意什么？

## A
- 标准版本 ≠ 编译器支持度：不同编译器/标准库实现某个特性的时间不同。
- CoderPad 默认的 `-std` 可能是 **17**，先确认再用 C++20 特性（`ranges`、`std::format`、`<=>`、concepts 等）。
