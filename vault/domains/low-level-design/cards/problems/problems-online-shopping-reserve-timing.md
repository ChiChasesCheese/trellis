---
id: problems-online-shopping-reserve-timing
node: problems.marketplaces.online-shopping
type: qa
step: 1
tags: [grown]
---
## Q
在线购物（Online Shopping，电商下单系统）设计里，库存该在加购物车时锁、在下单时锁、还是扣款成功后再扣？三种做法各自的代价是什么？

## A
加购即锁会**少卖**（undersell）：加购的人比下单的人多一个数量级，大促时热门商品被一堆永远不会结账的购物车占死，真正想买的人看到无货。扣款后再扣现货会**超卖**（oversell）：先收钱再发现没货，只能退款道歉——本质是把会失败的步骤排在了不可逆的步骤后面。通行做法是下单时预留（reservation）并给它一个过期时间，覆盖“跳到支付页付款”那几分钟。它承认“加进购物车不等于买得到”，这正是电商“手慢无”的来源，是刻意的取舍而不是缺陷。
