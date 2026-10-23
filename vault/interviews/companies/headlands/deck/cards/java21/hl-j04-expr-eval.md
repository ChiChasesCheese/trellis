---
id: hl-j04-expr-eval
node: java21.j04-record-patterns
type: qa
step: 17
---
## Q
补全代码：定义 `sealed interface Expr permits Const, Add, Mul, Neg`，用 record 模式写 `eval(Expr e)`。这种"一个 sealed 层级 + 每种操作一个 switch"适合什么场景？

## A
```java
sealed interface Expr permits Const, Add, Mul, Neg {}
record Const(long value) implements Expr {}
record Add(Expr left, Expr right) implements Expr {}
record Mul(Expr left, Expr right) implements Expr {}
record Neg(Expr inner) implements Expr {}

static long eval(Expr e) {
    return switch (e) {
        case Const(var v) -> v;
        case Add(var l, var r) -> eval(l) + eval(r);
        case Mul(var l, var r) -> eval(l) * eval(r);
        case Neg(var x) -> -eval(x);
    };
}
```
编译器保证每个 `switch` 处理全。量化 / 交易系统里的**定价公式、风控规则、订单路由条件、查询过滤器**都是这种树。
