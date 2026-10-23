---
id: hl-cq-q44-checklist
node: cpp-questions.k-experience
type: qa
step: 7
---
## Q
CoderPad 现场 C++ 的四步检查清单是什么？写代码时有哪些 C++ 习惯？

## A
1. **开场**：确认语言、输入输出格式、数据规模，写 2–3 个测试用例（含空输入、重复、边界）。
2. **骨架**：`#include`、`main`、能编译的空函数；先让它跑起来，再加功能。
3. **习惯**：`const auto&` 遍历；大对象 `const T&` 传参；`reserve`；`emplace_back`；可能超过 20 亿的量用 `std::int64_t`；名字有意义；函数短。
4. **说复杂度和分配**：“这里每次 O(log n)，一次堆分配；如果需要更快我可以改成……”
