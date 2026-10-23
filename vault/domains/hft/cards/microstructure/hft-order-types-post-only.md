---
id: hft-order-types-post-only
node: microstructure.order-types
type: qa
step: 3
---
## Q
post-only（只做挂单）订单是什么？为什么做市商喜欢用它？

## A
post-only 订单保证自己**只做 maker**：如果它一到交易所就会立刻与簿上的订单成交（也就是会变成 taker），交易所就拒绝它（或把价格调整到不会成交的位置），而不是让它成交。

原因：很多交易所对 taker 收费、对 maker 返佣，量级是 taker 付约每股 0.003 美元，maker 得约 0.002 美元。做市商挂单时如果价格已变，本想当 maker 却变成了 taker，一进一出差约 0.005 美元每股，而一只活跃股票的半价差也常常只有 0.005 美元，这笔交易的利润可能就全没了。

代价：被拒绝时既没有成交也没有排上队，需要重新发单。
