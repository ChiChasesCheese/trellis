---
id: hl-cq-q11-ctor-throws
node: cpp-questions.c-memory-ownership
type: qa
step: 4
---
## Q
追问：C++ 构造函数抛异常时，哪些析构会运行？对资源管理的启示是什么？
What if a constructor throws?

## A
- 已经构造好的**成员**会被析构；**对象自己的析构函数不会运行**，因为这个对象从未完整存在。
- 启示：拥有资源的成员本身就应该是 RAII 类型，这样构造中途失败也不会泄漏。
