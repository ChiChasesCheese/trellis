---
id: hl-c04-implicit-generation
node: cpp-lessons.c04-move-semantics
type: qa
step: 9
---
## Q
编译器什么时候自动生成移动操作？声明了析构函数或拷贝操作的类，放进 `vector` 时会怎样？

## A
- 你声明了**析构函数或拷贝操作**，编译器就**不再自动生成**移动操作；拷贝操作仍会生成。
- 你声明了**移动操作**，拷贝操作被**删除**。
- 例：一个声明了拷贝构造和析构函数的 `Tracer` 类，`v.push_back(Tracer("tmp"))` 时临时对象被**复制**进 `vector`，不会被移动。
- 因此：要么什么都不写（Rule of 0），要么五个一起考虑。
