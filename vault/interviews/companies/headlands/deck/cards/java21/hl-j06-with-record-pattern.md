---
id: hl-j06-with-record-pattern
node: java21.j06-instanceof-pattern
type: qa
step: 11
---
## Q
Java 21 里 `instanceof` 右边除了类型模式，还可以是什么？写一个按成交量过滤事件的例子。

## A
还可以是 **record 模式**，规则完全一样，只是顺便拆开 record：

```java
if (e instanceof Trade(var px, var qty) && qty >= minQty) out.add(qty + "@" + px);
```
`px`、`qty` 是绑定变量，`&&` 右边可以直接用 `qty`。这在"一个条件里同时用类型和字段"的场合很方便。
