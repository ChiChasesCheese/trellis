---
id: hl-cq-q40-object-model-memory
node: cpp-questions.j-cross-language
type: qa
step: 2
---
## Q
Java 和 C++ 在对象模型、赋值 `b = a`、内存回收这三方面有什么不同？

## A
| 方面 | Java | C++ |
|---|---|---|
| 对象模型 | 除原始类型外都是堆对象，变量存引用 | 对象就是值：栈上、成员内联、容器里连续 |
| 赋值 `b = a` | 两个名字指向同一对象 | **拷贝**一个新对象 |
| 内存回收 | GC | RAII：确定性析构 |
