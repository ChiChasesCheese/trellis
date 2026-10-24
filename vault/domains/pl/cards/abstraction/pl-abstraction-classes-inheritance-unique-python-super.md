---
id: pl-abstraction-classes-inheritance-unique-python-super
node: abstraction.classes-inheritance
type: qa
step: 7
---
## Q
Python 的 `super()` 为什么不等于「调用父类」？这揭示了 Python 多继承怎样的设计哲学？

## A
`super()` 的真实含义是「在**当前实例的类**的 MRO 里，找排在我后面的那个类」。在菱形继承中，`B.hi` 里的 `super().hi()` 并不调用 `A.hi`，而是调用 `C.hi`（实例是 `D` 时，MRO 为 D、B、C、A）。同一份 `B` 的代码，被 `B()` 使用和被 `D()` 使用时，`super()` 指向不同的类。

这叫**协作式多继承**（cooperative multiple inheritance）：每个类只负责自己那一段，然后把调用交给「下一个人」，由整条链共同完成工作。要让它成立，所有类必须遵守约定：

- 方法签名兼容，通常用 `**kwargs` 往后传。
- 每个类都调用 `super()`，不能中途断掉。
- 链的最后一个类（通常是 `object` 的子类）负责终止。

这体现了 Python 的哲学：不通过语言限制来防止滥用，而是提供一个**数学上自洽的规则**（C3）并信任程序员遵守约定（「我们都是成年人」）。对比之下，Java 通过语言禁止多继承来避免问题；Python 选择让它可用，代价是约定一旦被破坏（某个类忘了调用 `super()`），后面的类就悄悄不执行。
