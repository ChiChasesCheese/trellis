---
id: hl-j13-nested-guard
node: java21.j13-unnamed-variables
type: qa
step: 12
---
## Q
`Placed(Order order)` 中 `Order(id, side, px, qty)` 有四个字段，要按 `qty >= 1000` 分 BIG/SMALL 并带上 `side`，用嵌套解构 + `when` 怎么写？新写法比旧写法好在哪？

## A
```java
static String classify(Msg m) {
    return switch (m) {
        case Placed(Order(_, Side s, _, var q)) when q >= 1000 -> "BIG " + s;
        case Placed(Order(_, Side s, _, _)) -> "SMALL " + s;
        case Cancelled _ -> "CANCEL";
    };
}
```
四个字段只取 `side` 和 `qty`。旧写法要么 `case Placed p -> { Order o = p.order(); if (o.qty() >= 1000) ... }`，要么给 `id`、`px` 起 `var unusedId, var unusedPx`；新写法**一行说清「关心哪两个字段」**。
