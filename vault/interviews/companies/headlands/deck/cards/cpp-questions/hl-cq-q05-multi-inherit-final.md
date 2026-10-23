---
id: hl-cq-q05-multi-inherit-final
node: cpp-questions.a-why-fast
type: qa
step: 29
---
## Q
追问：多重继承时对象里有几个 vptr？`final` 能给虚函数调用带来什么？
Multiple inheritance? What does `final` buy you?

## A
- **多重继承**：对象为每个多态基类各存一个 vptr；在不同基类之间转换指针时，指针值会被调整。
- **`final`**：告诉编译器不会再有进一步的重写，所以通过该类型的调用可以被**去虚化**（devirtualized），变成直接调用甚至内联。
