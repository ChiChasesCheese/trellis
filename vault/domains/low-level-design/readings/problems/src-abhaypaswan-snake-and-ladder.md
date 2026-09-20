---
nodes: [problems.games.snake-and-ladder]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/snake-and-ladder
tags: []
---
# lld-python — Snake and Ladder

值得读：少见的**纯 Python** 蛇梯棋题解，也是唯一一份把"不许有跳跃首尾相接"写进需求、并且
真的提供了 `Board.validate()` 的。它的骰子是 `Dice` 外加 `DiceRollStrategy` 抽象基类和两个
子类，蛇和梯子是 `Jump` 的两个子类，位置存在 `Player` 上，`MoveResult` 这条不可变记录让
回合结果可断言而不是被打印掉。本题解在三处往前推了一格：校验挪进 `Board.__init__`（要你
记得去调的校验不是校验）、策略的载体从类层次换成 `Callable[[], int]`（那个只做转发的
`Dice` 壳被删掉）、位置从 `Player` 收回 `Game`（否则"和领先者换位"这种规则没法原子地移动
两个人）；另外它没有处理"整局循环在精确落子规则下可能不终止"和"连续三个六作废整轮需要
事务性回合"这两件事。
