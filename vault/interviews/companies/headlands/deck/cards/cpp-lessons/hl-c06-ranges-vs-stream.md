---
id: hl-c06-ranges-vs-stream
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 20
---
## Q
面试问：C++ ranges 比 Java Stream 好在哪里？
Interview question: What are the advantages of C++ ranges over Java Streams?

## A
- **惰性视图零分配**：没有中间集合，没有装箱。
- 与迭代器兼容，可以和传统算法混用。
- **编译期展开**，lambda 内联。
- 代价：调试/报错信息更难读；C++20 缺少 `zip`、`enumerate`、`to<vector>` 等视图（C++23 才有）。
