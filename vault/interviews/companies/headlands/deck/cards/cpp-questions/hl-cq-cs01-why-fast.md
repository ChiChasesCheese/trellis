---
id: hl-cq-cs01-why-fast
node: cpp-questions.cheatsheet
type: qa
step: 1
---
## Q
一句话背诵：为什么 C++ 快？`std::sort` 和 `qsort` 的差距是多少？

## A
- 提前编译成原生码 + **没有强制运行时**（无 GC、默认不查边界）+ 优化器看得见整个翻译单元所以能内联。
- 500 万 `int`：`std::sort` **81 ms**，`qsort` **303 ms**（比较函数是否被内联）。
- 性能是“可以做到”，不是“自动得到”。
