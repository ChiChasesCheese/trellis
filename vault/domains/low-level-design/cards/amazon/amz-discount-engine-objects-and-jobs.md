---
id: amz-discount-engine-objects-and-jobs
node: amazon.amz-discount-engine
type: qa
step: 2
tags: [grown]
---
## Q
在 Amazon 购物车折扣引擎设计里，需要哪几个核心类？各自只负责什么？

## A
这个系统读一个购物车和一批促销规则，算出每件商品该付多少并列出每笔减免。

- `LineItem`：一行商品（SKU、单价、数量），不可变。
- `Cart`：容器，同 SKU 合并成一行。
- `LineDiscount`：行级折扣，`is_eligible(line)` 问能不能用，`apply(line, 剩余价格)` 问减多少。
- `CartDiscount`：只看折后总额的折扣（满减）。
- `PriceEngine`：遍历、钳位、记账，不认识任何具体折扣。
- `Receipt`：带标签的账单。

拆分依据：折扣依赖的数据范围（一行 or 整车）。
