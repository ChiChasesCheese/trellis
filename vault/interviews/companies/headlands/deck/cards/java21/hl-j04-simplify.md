---
id: hl-j04-simplify
node: java21.j04-record-patterns
type: qa
step: 18
---
## Q
写出表达式树化简 `simplify(Expr e)` 的前几个分支：消去 `0 + r`、`l + 0`、`l * 1`、`1 * r`、`--x`，其余递归化简子树。

## A
```java
return switch (e) {
    case Add(Const(var a), var r) when a == 0 -> simplify(r);
    case Add(var l, Const(var b)) when b == 0 -> simplify(l);
    case Mul(var l, Const(var b)) when b == 1 -> simplify(l);
    case Mul(Const(var a), var r) when a == 1 -> simplify(r);
    case Neg(Neg(var x)) -> simplify(x);
    case Add(var l, var r) -> new Add(simplify(l), simplify(r));
    ...
};
```
**更具体的分支写前面**，最后才是一般形式。例：`(0 + (2 + 3) * --1)` 化简成 `(2 + 3) * 1`，值为 5。
