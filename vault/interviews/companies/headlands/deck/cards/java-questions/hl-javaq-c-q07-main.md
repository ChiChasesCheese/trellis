---
id: hl-javaq-c-q07-main
node: java-questions.c-languages
type: qa
step: 1
---
## Q
详细比较 Java 和 Python，各自什么时候用？
Compare Java and Python in detail. When would you use each?

## A
一句话：Java **静态类型、JIT 编译、真正多线程、延迟可预测**；Python **动态类型、解释执行、GIL 限制 CPU 并行、开发快生态强**。

- **延迟敏感 / 长期服务 / 大型团队 → Java**。
- **研究、胶水、数据分析、原型 → Python**，热点交给 NumPy 等 C 扩展。
- 对 Headlands 这类公司：研究员用 Python 做原型和分析，系统 / 基础设施用 Java / C++；热路径的延迟和吞吐需要静态类型、可预测性能和真线程。
- 口述时带一个实用差异：Java 的 `int` 是 32 位、溢出回绕，Python 有大整数；整数除法 Java 向零截断，Python 向下取整。
