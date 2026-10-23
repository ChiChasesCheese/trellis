---
id: hl-j08-basic-rule
node: java21.j08-var
type: qa
step: 2
---
## Q
`var` 局部变量类型推断（local variable type inference）的基本规则是什么？`var fills = new ArrayList<Fill>();`、`var count = 0;`、`for (var f : fills)` 各是什么类型？

## A
规则：**编译器看右边初始化表达式的类型，当作变量的类型**，之后与你手写该类型完全一样。

```java
var fills = new ArrayList<Fill>();   // ArrayList<Fill>
var count = 0;                        // int
var name = "AAPL";                    // String
for (var f : fills) { ... }           // f : Fill
```
