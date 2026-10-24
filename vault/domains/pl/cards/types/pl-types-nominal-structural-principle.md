---
id: pl-types-nominal-structural-principle
node: types.nominal-structural
type: qa
step: 1
---
## Q
名义类型（nominal typing）和结构类型（structural typing）的区别是什么？它要解决「这个值能不能当那个类型用」的哪种问题？

## A
问题：函数写着「接受一个会叫的东西」，传进来一个 `Dog`，编译器凭什么判断 `Dog` 满足这个要求？

设计空间有三种回答：

1. 名义类型：看声明。`Dog` 必须明确写出「我实现了 `Speaker`」（Java 的 `implements`，Rust 的 `impl Speaker for Dog`），编译器查这张声明表。名字不在表里，即使方法一模一样也不行。
2. 结构类型：看形状。只要 `Dog` 拥有 `Speaker` 要求的全部方法，签名一致，就算满足，不需要任何声明。Go 的接口就是这样。
3. 鸭子类型（duck typing）：运行时才看。调用 `x.speak()` 时，对象有 `speak` 就能用，没有就抛 `AttributeError`。Python 默认如此。

对比的要点是谁来建立「满足」关系：名义类型要求类型的作者提前声明，关系清晰，但无法事后让别人的类型满足你的接口；结构类型把关系推迟到使用点，解耦更彻底，但可能出现「碰巧满足」。

一句话定位：Java 和 Rust 是名义的，Go 是结构的（编译期），C++ 两者都有（继承是名义的，模板是编译期结构的），Python 是鸭子类型，后来用 `typing.Protocol` 加了可选的结构检查。
