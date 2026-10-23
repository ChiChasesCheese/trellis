---
id: hl-c12-zero-cost-sort
node: cpp-lessons.c12-why-cpp-is-fast
type: qa
step: 3
---
## Q
零开销抽象的实证：三种求和写法生成什么代码？排序 500 万个 `int`，`std::sort`、`std::sort + lambda`、`qsort` 各多少毫秒？

## A
- `sum_raw`（裸指针循环）、`std::accumulate`、范围 `for` 生成近乎相同的**向量化循环**（汇编指令数 75 / 79 / 79 条）。
- 排序 500 万个 `int`：`std::sort` 73.1 ms，`std::sort` + lambda 200.2 ms，`qsort` 272.0 ms；`qsort` 约是 `std::sort` 的 3.7 倍，结果相同。
- 原因：比较函数在**编译期已知**，直接内联进排序循环；`qsort` 每次比较都要经**函数指针间接调用**。
- 默认 `<` 版本更快，是因为该标准库对整数的默认比较有专用路径；确切倍数依赖实现。
