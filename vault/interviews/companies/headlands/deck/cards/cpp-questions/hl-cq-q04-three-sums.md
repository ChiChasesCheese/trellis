---
id: hl-cq-q04-three-sums
node: cpp-questions.a-why-fast
type: qa
step: 21
---
## Q
手写 `for` 求和、`std::accumulate`、带 lambda 的 `accumulate` 三种写法，在 `-O0` 和 `-O2` 下的汇编有什么差别？循环 `s += i`（0 到 n-1 求和）在 `-O2` 变成什么？

## A
用 `clang++ -O2 -S` 统计：
- `-O0`：`accumulate` 两个版本各保留 1 次对模板函数的 `call`（14 条指令）；手写循环 25 条、0 次调用。
- `-O2`：三个版本都**内联**并**向量化**，0 次调用，用了 SIMD 指令（`.2d`、`.4s` 是 SIMD 寄存器）。
- 高斯求和 `gauss(n)` 的循环体 `s += i` 在 `-O2` 下**没有循环**，变成一次乘法的闭式（约 8 条指令）。

结论：这就是零开销抽象的实际含义——标准库写法和手写一样快。
