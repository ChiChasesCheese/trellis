---
id: hl-j01-no-instance-field
node: java21.j01-record
type: qa
step: 8
---
## Q
下面的 `record` 有什么问题？怎么加一份状态？

```java
record P(int x) { int y; }
```

## A
`record` 不能声明**实例字段**，编译报 `field declaration must be static`。

要加状态就**加组件**：`record P(int x, int y)`。

原因：record 的全部状态必须都在括号里，编译器才能据此生成 `equals` / `hashCode` / `toString`，读者也一眼知道状态不多不少。
