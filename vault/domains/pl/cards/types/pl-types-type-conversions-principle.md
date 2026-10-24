---
id: pl-types-type-conversions-principle
node: types.type-conversions
type: qa
step: 1
---
## Q
显式类型转换有哪几种，各自可能怎样失败？语言在「转换失败时怎么办」上有哪些设计选择？

## A
程序经常需要把一个值当作另一种类型来用。转换按风险分为四类：

1. 无损转换（widening）：`int32` 到 `int64`，目标装得下所有源值，不会失败。
2. 有损转换（narrowing）：`int64` 到 `int32`、浮点到整数，目标装不下，可能丢信息。
3. 向下转型（downcast / type assertion）：把基类或接口引用当作具体子类用，对象的真实类型不一定符合。
4. 解析（parse）：字符串到数字，输入内容不一定合法。

要解决的问题：转换点是 bug 的高发处，因为它们是类型系统「承认自己无法完全保证」的地方。语言对失败的处理有三种设计：

- 静默失败：截断或饱和，返回一个错值（C 和 C++ 的强制转换、Go 的 `int32(x)`、Java 的 `(byte)`）。快，但不报错。
- 报告失败：抛异常或 panic（Java 的 `ClassCastException`、Go 的断言失败），或者返回可检查的结果（Go 的 `v, ok := x.(T)`、Rust 的 `Result`）。
- 在类型里区分：把「不会失败」和「可能失败」做成不同的接口（Rust 的 `From` 与 `TryFrom`），让编译器和读者看到风险。

取舍轴是「便利与速度」对「失败可见」：转换越随便，越容易写，错误越晚才发现。
