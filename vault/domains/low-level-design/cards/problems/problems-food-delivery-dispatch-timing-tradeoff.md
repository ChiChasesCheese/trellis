---
id: problems-food-delivery-dispatch-timing-tradeoff
node: problems.marketplaces.food-delivery
type: qa
step: 4
tags: [grown]
---
## Q
外卖派单：餐厅一接单就让骑手出发，和掐着出餐时间再出发，各自的成本落在谁身上？给出一个能写成一行的派单判据。

## A
派早了，**骑手**在店门口空等——他的有效工时被占用，平台要么多付钱要么少接单。派晚了，**顾客**吃到凉菜——投诉里「凉了」永远排第一。两边都有成本，所以面试时必须说清楚你在优化哪一个。

一个优化食物温度的判据：骑手**现在出发**会在 `now + 路程` 到店，只要这个时刻还早于 `出餐时刻 - 可接受空等`，就再等一轮。

```python
arrival = now + self._travel(courier.location, pickup)
if arrival < order.ready_at - self._max_courier_wait:
    continue          # 还早，下一轮再说
```

于是发车时刻自动落在 `ready_at - 路程 - 可接受空等`：骑手最多空等那一小段，而做好的菜一秒都不用等。

失败模式要主动交代：如果那一刻没有空闲骑手，这一单只能等，菜真的会凉。真实平台在这里会提前扩大搜索半径、并给这一单加钱提高接单意愿。
