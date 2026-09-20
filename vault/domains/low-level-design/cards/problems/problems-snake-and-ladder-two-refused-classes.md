---
id: problems-snake-and-ladder-two-refused-classes
node: problems.games.snake-and-ladder
type: qa
step: 6
tags: [grown]
---
## Q
蛇梯棋（Snake and Ladder）的流行题解里几乎都有两个类：`Snake` / `Ladder` 两个子类，以及一个带 `position` 和 `move()` 的 `Player`。为什么这两个都该删掉？什么时候这个答案会翻转？

## A
判断一个类该不该存在，只问一句：**它拥有哪条不变量？**

`Snake` 和 `Ladder` 的差别只有方向（终点比起点小还是大）和一个称呼。方向是**从数据算出来的**：一个 `Jump(start, end)` 加一个 `kind` 属性就够了。继承在这里没买到任何东西，反而引入了新错误面——`Snake(5, 20)` 这种「向上的蛇」必须靠子类构造校验去挡，而算出来的 `kind` 根本不给这个错误留位置。

`Player` 的 `position` 看似是它自己的，但只要存在「和领先者换位」这类**同时移动两个人**的规则，「谁在哪一格」就必须由一个对象整体维护，否则一次换位就是两个对象各改各的，中间出异常会留下两人同格或互相错位。位置归 `Game`，`Player` 就只剩一个名字，那它就是 `str`。

翻转条件：蛇和梯子出现**行为**差异时（梯子只能爬三次、被蛇咬要扣分），子类才开始划算；玩家携带真正的行为时（会自己决策的机器人），`Player` 才该出现，形状是「不可变身份 + 一个可选的决策函数」。
