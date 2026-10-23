---
id: hl-j04-nested-order
node: java21.j04-record-patterns
type: qa
step: 7
---
## Q
嵌套 record 模式 `Value(Mean(var n, var d))` 从外到内怎么匹配？写出用它化简表达式 `0 + r` 和 `--x` 的两个分支。

## A
从外到内：先查是不是 `Value`，再查 `mean()` 的值是不是 `Mean`（静态类型就是 `Mean`，所以必然是，除非为 `null`），然后取出 `n`、`d`。不管嵌几层，写法都对称。

```java
case Add(Const(var a), var r) when a == 0 -> simplify(r);   // 0 + r  ->  r
case Neg(Neg(var x)) -> simplify(x);                        // --x    ->  x
```
一次看两层，不用中间变量。
