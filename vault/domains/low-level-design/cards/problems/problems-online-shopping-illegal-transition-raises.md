---
id: problems-online-shopping-illegal-transition-raises
node: problems.marketplaces.online-shopping
type: qa
step: 4
tags: [grown]
---
## Q
电商订单的状态变更被要求做一次转移表不允许的跳转（比如还没付款就发货），应该抛异常还是静默忽略？状态字段本身该怎么暴露？

## A
抛异常。被吞掉的非法转移意味着调用方以为自己发货了，而订单其实还没付款——这种错误不会立刻爆炸，只会在对账时浮现。状态字段对外是**只读属性**，唯一的改法是 `transition_to(state, at)`：有了 setter，状态机的不变式就等于不存在，任何一处都能把订单偷偷改成“已发货”。另外每次转移都往历史里追加一条“从哪来、到哪去、什么时候”的记录——“这张单什么时候付的款”是客服每天要回答的问题，只能来自事中记录，不能事后推算。
