---
id: hl-cq-q40-generics-safety-concurrency
node: cpp-questions.j-cross-language
type: qa
step: 3
---
## Q
Java 和 C++ 在泛型、越界 / 溢出、并发这三方面有什么不同？

## A
| 方面 | Java | C++ |
|---|---|---|
| 泛型 | 擦除，装箱 | 模板，按类型实例化 |
| 越界 / 溢出 | 抛异常 / 回绕，有定义 | `v[i]` 越界是 UB；有符号溢出是 UB |
| 并发 | `synchronized`、`volatile`、JMM | `mutex`、`atomic`、C++ 内存模型；`volatile` 不是同步 |
