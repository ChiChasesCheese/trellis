---
id: hl-c04-rule-of-0-3-5
node: cpp-lessons.c04-move-semantics
type: qa
step: 8
---
## Q
面试问：Rule of 0、Rule of 3、Rule of 5 分别是什么？哪个是首选？
Interview question: What are the rules of zero, three and five?

## A
特殊成员函数共五个：析构、拷贝构造、拷贝赋值、移动构造、移动赋值。
- **Rule of 0（首选）**：成员本身都会自己管理资源（`string`、`vector`、`unique_ptr`），那就**一个都不写**，编译器生成的全是对的。
- **Rule of 3**：只要手写了析构/拷贝构造/拷贝赋值**中的一个**（说明你在管理原始资源），其余两个也几乎一定要写。
- **Rule of 5**：现代版本，再加上移动构造和移动赋值。
- 手写资源管理类而不是组合标准库类型，是大多数移动相关 bug 的来源，Rule of 0 能避免。
