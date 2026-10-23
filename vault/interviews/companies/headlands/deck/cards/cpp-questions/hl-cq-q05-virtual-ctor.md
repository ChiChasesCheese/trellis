---
id: hl-cq-q05-virtual-ctor
node: cpp-questions.a-why-fast
type: qa
step: 28
---
## Q
追问：在构造函数里调用虚函数会发生什么？
What happens if you call a virtual function in a constructor?

## A
调用的是**当前正在构造的那个类**的版本，而不是最派生类的重写，因为此时派生部分还不存在。
