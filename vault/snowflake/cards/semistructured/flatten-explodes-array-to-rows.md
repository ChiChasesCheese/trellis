---
id: flatten-explodes-array-to-rows
node: semistructured.flatten-lateral-joins
type: qa
tags: [grown]
---
## Q
表 `orders` 的 VARIANT 列 `v` 中有一个 `items` 数组，想得到「每个商品一行」的结果。为什么要用 `FLATTEN`，写法大致是什么？

## A
路径表达式 `v:items` 只能取出整个数组这一个值，无法把数组变成多行。`FLATTEN` 是一个表函数（table function），输入一个数组或对象，为其中每个元素输出一行。写法：`SELECT o.id, f.value:sku::string FROM orders o, LATERAL FLATTEN(input => o.v:items) f;`，一个订单有 3 个商品就产生 3 行，每行带着原订单的列。
