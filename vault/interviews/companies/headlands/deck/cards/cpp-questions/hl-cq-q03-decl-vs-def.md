---
id: hl-cq-q03-decl-vs-def
node: cpp-questions.a-why-fast
type: qa
step: 16
---
## Q
追问：C++ 里“声明”和“定义”有什么区别？
Declaration vs definition?

## A
- **声明**（declaration）：引入一个名字和它的类型，例如 `int square(int x);`。
- **定义**（definition）：在声明的基础上，还分配存储或给出函数体。
- 声明可以重复出现；定义每个程序只能有一次（ODR）。
