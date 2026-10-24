---
id: pl-abstraction-polymorphism-kinds-principle
node: abstraction.polymorphism-kinds
type: qa
step: 1
---
## Q
编程语言里的多态（polymorphism）要解决什么问题？有哪三种形式，它们沿着什么轴区分？

## A
问题：同一段代码或同一个名字要作用于多种类型，又不想为每种类型复制一份。不做多态的办法只有两个：复制粘贴，或者退化成「万能类型 + 强制转换」（早期 Java 的 `Object`、Go 1.18 之前的 `interface{}`），后者把类型错误推迟到运行期。

1967 年 Strachey 把多态分成两类，后来 Cardelli 与 Wegner 细分为三种：

- **参数多态**（parametric polymorphism，泛型）：一份代码对所有类型一视同仁，完全不看具体类型。例：`reverse<T>(list)`。
- **子类型多态**（subtype polymorphism）：调用方只依赖一个共同的上层类型，运行时按对象的实际类型挑选行为。例：`shape.area()`。
- **特设多态**（ad hoc polymorphism）：同一个名字对不同类型对应不同的代码，由语言按类型选择。例：重载、`impl Trait for Type`。

区分它们的轴有两条：**代码是共享的还是按类型各写一份**（参数多态共享，特设多态各写各的），以及**选择发生在编译期还是运行期**（特设多态通常编译期，子类型多态通常运行期）。后面所有的语言特性（接口、泛型、分派）都落在这张图的某个位置上。
