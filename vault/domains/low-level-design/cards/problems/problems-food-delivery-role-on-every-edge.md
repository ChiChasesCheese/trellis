---
id: problems-food-delivery-role-on-every-edge
node: problems.marketplaces.food-delivery
type: qa
step: 1
tags: [grown]
---
## Q
外卖（Food Delivery）的订单要在顾客、餐厅、骑手三方之间流转。状态机除了「能不能走这条边」还必须回答什么？这个信息放在哪里？

## A
必须同时回答「**谁**有资格走」。顾客不能把订单标成「已送达」，骑手不能替餐厅接单，餐厅接单之后顾客不能单方面取消。

把角色直接挂在**边**上，写成一张 `{当前态: {目标态: 允许的角色}}` 的嵌套表：

```python
TRANSITIONS = {
    OrderState.PLACED: {
        OrderState.ACCEPTED: frozenset({Actor.RESTAURANT}),
        OrderState.REJECTED: frozenset({Actor.RESTAURANT, Actor.PLATFORM}),
        OrderState.CANCELLED: frozenset({Actor.CUSTOMER, Actor.PLATFORM}),
    },
    OrderState.ACCEPTED: {
        OrderState.READY: frozenset({Actor.RESTAURANT}),
        OrderState.CANCELLED: frozenset({Actor.PLATFORM}),
    },
}
```

判据：**例外用第二张表，通例进第一张表。** 两方系统（比如网约车）里往往只有「取消」需要分方，那就单独列一张小的许可表；三方系统里**每一条边都属于某一方**，许可就该和边住在一起——否则两张表的键必须一一对应，漏掉一行没人发现。

把权限散成十个方法里的十个 `if` 是最差的写法：没有任何一处能一眼看全「谁能做什么」，而这恰恰是三方系统最需要被审计的东西。
