---
id: hi-sd-gopuff-2-entities-api
node: sd.problem-breakdowns.gopuff.exam
type: qa
step: 2
---
## Q
**核心实体与接口：Item 与 Inventory 的区别**｜系统设计 · 题目拆解

Gopuff 的核心实体有哪些？为什么要把 Item 和 Inventory 分开？接口需要哪些参数？

## A
**要点。**

| 实体 | 含义 |
|---|---|
| Item | 一种商品，如某品牌薯片，顾客关心的是它 |
| Inventory | 某个 DC 里的一件实物，汇总它得到某商品对某位用户的可售数量 |
| DistributionCenter | 实物所在的物理地点，用来判断哪些商品对用户可售 |
| Order | 用户订购的一批 Inventory，外加配送与账单信息 |

**为什么。** 类比面向对象里的「类」与「实例」：Item 是类，Inventory 是带位置的实例。

**接口。** 只需两个：按位置（可加关键词）查询可售商品，带分页；下单。下单也要传位置，因为后端要确认库存足够近、能在 1 小时内送达。

**易错。** 先从最具体的实体（商品、用户）往抽象的（订单、购物车）列，不容易漏。
