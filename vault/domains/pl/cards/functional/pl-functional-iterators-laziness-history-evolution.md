---
id: pl-functional-iterators-laziness-history-evolution
node: functional.iterators-laziness
type: qa
step: 11
---
## Q
迭代器与流水线风格是怎样进入主流语言的？为什么各语言都在加？

## A
时间线：

- **2001 年，Python 2.2**：生成器（PEP 255），用 `yield` 把惰性序列写成普通函数。
- **2014 年，Java 8**：Stream API 与 lambda 同时到来，把声明式的集合变换带入主流企业开发。
- **2015 年，Rust 1.0**：`Iterator` trait 与零成本适配器是语言的核心卖点之一。
- **2024 年，Go 1.23**：range-over-func 与 `iter` 包，用最小的语言改动补上通用迭代的缺口。

动因是同一个：**数据变换的流水线写法更接近人的思考**（「过滤，转换，取前 10 个」），并且让「怎么遍历」与「做什么」解耦，同一套工具能处理集合、文件、网络流和无限序列。

趋势的演进：
1. 惰性成为默认（Python 3 的 `map`、`filter`、`zip` 都改成了迭代器）；
2. 编译器的优化能力决定了抽象的成本，所以静态编译语言偏向类型层面的零成本（Rust），运行时语言偏向 JIT 优化（Java）；
3. 序列的统一接口越来越简单：Python 的两方法协议、Go 的一个函数签名。

一个值得注意的反向趋势：随着 `async` 流（`AsyncIterator`、Rust 的 `Stream`、Java 的 reactive streams）出现，迭代器需要同时处理「元素之间的等待」，这让原来简单的拉取协议变复杂，是目前各语言仍在摸索的方向。
