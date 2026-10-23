---
id: hl-j01-minimal-syntax
node: java21.j01-record
type: qa
step: 4
---
## Q
写出声明三字段 `Fill`（`String symbol`、`long priceTicks`、`long qty`）的 `record` 最简形式。括号里的"记录组件"（record component）一次做哪三件事？

## A
```java
record Fill(String symbol, long priceTicks, long qty) {}
```

括号里的**记录组件**一次做三件事：
1. 声明**字段**（永远是 `private final`）；
2. 声明**规范构造器**的参数；
3. 声明**访问器**。

一行就替代了 Java 8 的 30 行样板。
