---
id: hl-c06-ranges-views-lazy
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 14
---
## Q
C++20 的 range、view 和管线 `|` 是什么？和 Java Stream 有何异同？

## A
- **range**：任何有 `begin()/end()` 的东西。**view**：轻量、**惰性**的 range，不拥有元素，也不分配。
- `|` 把 view 串成管线，**只在遍历时**才一个元素一个元素地计算；没有中间集合，没有装箱。和 Java Stream 类似，但零分配。
- `std::ranges::sort(v)` 等算法直接收容器；**投影**参数让你按成员排序而不写比较器。
- 缺点：调试/报错更难读；C++20 的 views 不含 `zip`/`enumerate`/`to<vector>`（C++23 才有）。
