---
id: hl-cq-q25-template-errors-coderpad
node: cpp-questions.f-ub-debug
type: qa
step: 14
---
## Q
模板错误信息很长，怎么读？在 CoderPad 里写 C++ 应该怎么开场？常用头文件有哪些？

## A
- **读模板错误**：看**第一条 `error:`**，再看 “in instantiation of … requested here” 找到是你的哪一行调用。
- **CoderPad 开场**：先写一个能编译运行的最小骨架（`#include`、`using`、`main`），再逐步加功能。
- **常用头文件**：`<iostream> <vector> <string> <map> <unordered_map> <algorithm> <cstdint> <optional> <memory>`。
