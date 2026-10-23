---
id: hl-cq-q05-virtual-dtor
node: cpp-questions.a-why-fast
type: qa
step: 27
---
## Q
C++ 里通过基类指针 `delete` 派生类对象，如果基类析构函数不是 `virtual` 会怎样？应该怎么写？

## A
- **未定义行为**。典型表现是派生类部分没被销毁，只运行了基类的析构。
- 实测非虚析构：只输出 `~BadBase`，`~BadDerived` 没有运行；虚析构：先 `~GoodDerived` 再 `~GoodBase`。
- 写法：用于多态的基类写 `virtual ~Base() = default;`。
