---
id: pl-abstraction-classes-inheritance-history-evolution
node: abstraction.classes-inheritance
type: qa
step: 10
---
## Q
继承在主流语言里的地位是怎样变化的？现代语言怎样限制它的副作用？

## A
1990 年代是继承的高峰：C++ 与 Java 鼓励用类层级建模世界，GUI 框架、企业框架都以深层继承为骨架。2000 年代中期起风向转变，《Effective Java》（2001 年初版）提出「组合优于继承」，GoF 的设计模式一书更早就这样主张。

此后的语言演进呈现出一条明确的线：

- **默认封闭**：Kotlin 的类默认 `final`，要继承必须写 `open`；Swift 也有类似的 `final` 与模块级限制。
- **封闭的层级**：Java 17 的 `sealed` 类让作者明确列出允许的子类，使继承层级成为可穷尽的和类型，而不是开放的扩展点。
- **替代品**：Java 8 的接口 `default` 方法、`record`（不能继承其他类）、Python 的 `dataclass`，用来取代曾经靠继承得到的样板代码。
- **彻底放弃**：Go（2009）与 Rust（2015）从一开始就不提供实现继承。

演进的动机是同一个：层级一旦被外部代码继承，就成了不可更改的公共 API。把继承变成需要作者主动打开的开关，等于让「承诺」变得显式。方向不是消灭继承，而是让它只出现在确实需要的地方。
