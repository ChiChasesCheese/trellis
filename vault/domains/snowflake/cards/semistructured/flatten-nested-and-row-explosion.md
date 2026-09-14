---
id: flatten-nested-and-row-explosion
node: semistructured.flatten-lateral-joins
type: qa
tags: [grown]
---
## Q
订单包含商品数组，每个商品又包含折扣数组。要展开到「每个折扣一行」该怎么写？这样做在性能上要注意什么？

## A
串联两层 LATERAL FLATTEN：先 `LATERAL FLATTEN(input => o.v:items) i`，再 `LATERAL FLATTEN(input => i.value:discounts) d`，第二层引用第一层的输出（如需遍历任意深度的结构，也可以用 `RECURSIVE => TRUE`）。展开后的行数是各层元素数的乘积，数据量可能成倍膨胀，后续的连接和聚合都在膨胀后的行上计算；应尽早过滤，只展开真正需要的层级。
