---
id: hl-cq-cs02-vs-other-languages
node: cpp-questions.cheatsheet
type: qa
step: 2
---
## Q
一句话背诵：C++ 和其他编译型语言（Java、Go、Rust）比，差别到底在哪？

## A
- 差别在编译后还剩多少运行时工作，以及你对布局有多少控制权。
- Java / Go 有 GC；Java 除原始类型外都是堆对象加引用——`vector<Order>` 连续，`ArrayList<Order>` 是指针数组。
- 对 Rust：同一个 LLVM 后端，差别是生态，不是机器码。
