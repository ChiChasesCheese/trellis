---
id: hi-c-sd-problem-breakdowns-x01-pick-by-weakness
node: sd.in-a-hurry.problem-breakdowns.exam
type: qa
step: 3
---
## Q
**常见题目拆解 · 按弱项挑题练**｜考点 · 必会

你上周做 Ticketmaster 时在"占座过期与超卖"上卡壳，还有一周准备。请从全部题目里挑 4 道练同一类能力，并说明每道练到什么角度。

## A
- **Flash Sale：** 同一能力的放大版：瞬间高并发、有限库存、排队保护后端。
- **Online Auction：** 同一商品的出价竞争，另加实时推送。
- **Uber：** 司机被多人叫的竞争，加上位置匹配。
- **Payment System：** 竞争变成重复请求——用幂等和状态机而不是锁。
- **用法：** 先找共同的模式，再按难度从低到高排；每道只盯"竞争"这一个深入点，其余用快速方案带过。
