---
id: pl-abstraction-polymorphism-kinds-unique-rust-trait-unifies
node: abstraction.polymorphism-kinds
type: qa
step: 6
---
## Q
为什么说 Rust 的 trait 把三种多态收进了同一个机制？这和 Java 把它们分开提供有什么本质区别？

## A
同一个 trait 同时是三样东西：按类型提供实现的地方（特设多态，`impl Describe for i32`）、泛型的约束（参数多态，`T: Describe`）、运行期多态的入口（子类型多态，`&dyn Describe`）。

Java 的做法是分开提供：继承和接口管子类型，泛型管参数，重载管特设，三者互相独立，所以才有「泛型加重载在类型擦除后冲突」这类交叉规则。例如 `g(List<String>)` 与 `g(List<Integer>)` 同时存在，编译器报 `name clash: have the same erasure`。

更深的差别在**谁有权给类型加能力**。Java 的接口必须由类的作者在定义类时写上 `implements`；Rust 的实现可以事后补，只要 trait 或类型有一个是你自己的。能力因此成为独立于类型定义的东西，而不是类型层级的一部分。

C++ 的做法和 Java 一样是分开提供：虚函数管子类型，模板管参数，重载与模板特化管特设，三者各有一套规则，它们的交叉（模板里的重载决议、特化与重载的优先顺序）是 C++ 最难精通的部分之一。
源头是 Haskell 的类型类（type class）：把「这个类型能做什么」从类型定义中剥离。Rust 没有继承却不缺多态，原因就在这里：行为挂在 trait 实现上，而不是类的层级里。代价是学习曲线更陡，同时要引入孤儿规则（orphan rule）来防止两个库给同一个类型加互相冲突的实现。
