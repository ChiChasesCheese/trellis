---
id: amz-pizza-order-unsorted-toppings-mistake
node: amazon.amz-pizza-order
type: qa
step: 9
tags: [grown]
---
## Q
在披萨订单里，配料不排序会出什么错？给一个具体输入，并说明修复。

## A
「橄榄 + 蘑菇」和「蘑菇 + 橄榄」是同一款披萨，但配料元组不同，不相等、哈希也不同：订单里占两行，每行数量 1。规则「同款买一送一」要求一行数量至少 2，所以不触发，顾客该免一份却没免。

修复：`build()` 里 `tuple(sorted(...))`，同样的搭配得到同一个 `Pizza`，订单合并成一行数量 2，买一送一免掉一份。去重也要在这里做，重复的配料直接报 `InvalidChoiceError`。
