---
id: hl-j08-not-dynamic
node: java21.j08-var
type: qa
step: 3
---
## Q
Java 的 `var` 是动态类型吗？`var x = 1; x = "s";` 会怎样？它和 JavaScript 的 `var` 有什么本质区别？

## A
**不是动态类型。** `var` 的类型在**编译期**确定，不可更改：

```java
var x = 1;        // x 是 int
x = "s";          // 编译错误：incompatible types: String cannot be converted to int
```
JavaScript / Python 的变量可先后装不同类型；Java 的 `var` 只是"让编译器替你填类型"，也不是"少写点字"的万能药。
