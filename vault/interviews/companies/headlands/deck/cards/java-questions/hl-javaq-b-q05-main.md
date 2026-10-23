---
id: hl-javaq-b-q05-main
node: java-questions.b-versions
type: qa
step: 1
---
## Q
Java 8、11、17、21 的主要差别是什么？你实际会用哪些特性？
What are the main differences between Java 8, 11, 17 and 21? Which features would you actually use?

## A
Java 的对应物不是 C++11/14/17/20 那样的语言标准，而是 **LTS**（长期支持，long-term support）发布：8 → 11 → 17 → 21。每 6 个月发一版，但生产上多数只用 LTS。回答要有结构：**每个版本一句话 + 一个你真会用的例子**。

- **8**：lambda、Stream、Optional、`java.time`。
- **11**：`var`、HttpClient、字符串 / 集合小工具。
- **17**：record、sealed 类、文本块、`switch` 表达式、`instanceof` 模式。
- **21**：`switch` 模式匹配 + record 模式、**虚拟线程**、Sequenced Collections、分代 ZGC。
- 日常最爱用：record 和 sealed 配模式 switch 建模事件；I/O 密集代码用虚拟线程。
