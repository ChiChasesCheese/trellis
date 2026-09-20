---
id: problems-snake-and-ladder-turn-is-a-transaction
node: problems.games.snake-and-ladder
type: qa
step: 5
tags: [grown]
---
## Q
蛇梯棋（Snake and Ladder）加一条规则：连续掷出三个六，这一轮整轮作废。前两个六已经把人往前挪了两段——这条规则对回合循环的结构提出了什么要求？

## A
它逼着**整个回合变成一个事务**：一轮之内的所有位移必须能被整体撤销。两种实现方式，代价不同。

一是走一步改一步、作废时反着撤销——需要为每种位移写逆操作（退掉一次爬梯、退掉一次换位），而逆操作是新的出错面。二是把一轮的位移先写进一份局部的 `pending` 字典，轮末再整体提交；作废就是**丢弃 `pending`**，不需要任何逆操作。

```python
if verdict is RollAgain.CANCEL:
    cancelled, pending, changes = True, {}, []
    break
```

选第二种。代价是一轮之内读位置要写成 `pending.get(player, positions[player])`；回报是「作废」从撤销变成丢弃，而且「同时移动两个人」的换位规则也天然被包在同一个事务里。通用结论：**只要存在一条能让整轮白走的规则，回合就必须是事务性的**，这一点要在写第一行循环之前就想清楚。
