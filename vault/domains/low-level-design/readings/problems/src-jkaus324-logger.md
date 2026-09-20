---
nodes: [problems.components.logger]
url: https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/020-logger-system
tags: [no-archive]
---
# machine-coding-interview-questions — 020-logger-system

值得读：同一道题在五种语言里的并排实现，适合看"有 `interface` 关键字的语言"和 Python 在同一个
设计上的写法差异——尤其是 Java 里必须显式 `implements` 的地方，Python 用 `typing.Protocol` 的
结构化子类型就够了。它的异步部分只有"扔进队列、工作线程消费"，没有关闭时的排空与汇合，也没有
队列满时的丢弃计数；本题解把 flush → drain → join 的关闭三步和 `dropped_count` 列成了第 3 关的
硬性评分点，并用一个"八线程写满 800 条、队列只有 16 个位置、关闭后一条不少"的测试把它钉死。
仓库没有 LICENSE 文件，因此只链接、不归档。
