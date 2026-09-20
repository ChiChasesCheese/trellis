---
nodes: [problems.games.snake-and-ladder, patterns.strategy]
tags: [problem]
---
# Drill：蛇梯棋（Snake and Ladder）

一块可配置的棋盘、若干玩家、一颗骰子，先到终点的赢。十分钟就能跑起来，所以这道题的分全在
别处：**你的循环凭什么停得下来**、**换一条玩法要改几行**、**掷骰子的东西你怎么写测试**。
按真实机考的节奏分关做，做完一关再看下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：可配置的棋盘（格子数、蛇、梯子都是构造参数）、多个玩家、一颗骰子、
  一个会停下来的回合循环。**棋盘必须在构造时校验自己**：同一格不能是两条跳跃的起点、
  跳跃的**起点**不许落在起点格或终点格上、终点必须在棋盘上且不许回到起点格、蛇向下梯子向上、
  **并且没有任何一次跳跃的终点是另一次跳跃的起点**。注意这几条是非对称的：终点**可以**是
  终点格（经典棋盘上 80→100 那架梯子踩到就赢），别顺手把它也禁掉。写之前先回答两个问题：
  为什么"首尾相接"那一条是这道题存在的理由？如果面试官偏要支持连跳，你要额外做什么？
  失败路径各抛一个有名字的异常，不准返回 `False`。
- 第 2 关（约 15 分钟）：骰子变成注入的（一个 `Callable[[], int]` 就够，随机源是带种子的
  `random.Random`），然后一次加四条玩法变体——六点才能出发、掷到六加掷一次、连续三个六整轮
  作废、必须精确踩到终点格。**不许在回合循环里加第五个 `if`**：把循环钉死，在它上面开几个
  命名的决策点，每条规则是一个能被单独测试的纯函数。这一关有两个坑，撞上了再回头看题解：
  「掷到六再掷一次」不是把点数加起来；「三个六作废」会逼你把整个回合变成事务。
- 第 3 关（约 15 分钟）：人数任意；棋局结束时给出**完整名次**而不是只有赢家（想清楚同一格
  上两个人怎么排先后）；保留一份可回放的走子日志，并且日志被截断时轮数计数不能跟着错。
  交出去的位置表必须是快照，不能是内部那本字典。
- 第 4 关（选做，约 10 分钟）：加一个传送门格、一个「按刚才点数再走一次」的格子、一个
  「和当前领先者换位」的格子。验收标准很硬：**不许改回合循环的任何一行**，而且已经到达终点
  的人谁都不许把他拽回棋盘中间。

**怎么练**：把 `vault/domains/low-level-design/problems/snake-and-ladder/starter.py` 的方法体
补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/snake-and-ladder -q`。

**评分点**
- 说得出蛇梯棋有**两种性质不同的不终止**：一种靠棋盘构造时的校验根除，一种只能靠显式轮数
  上限兜底（[[problems-snake-and-ladder-two-kinds-of-nontermination]]、
  [[problems-snake-and-ladder-validate-at-construction]]）。
- 校验写在构造函数里而不是一个要你记得去调的 `validate()`；校验通过之后走子只查一次表，
  代码里没有追跳跃链的 `while`（[[problems-snake-and-ladder-validate-at-construction]]、
  [[method-invariant-ownership]]）。
- 骰子是一个函数类型而不是抽象基类加一层只会转发的壳；说得清"策略模式没被拒绝，被拒绝的是
  它的 Java 载体"（[[problems-snake-and-ladder-die-is-a-callable]]、[[patterns-strategy-callable]]）。
- 「掷到六再掷一次」实现成再走一段而不是把点数相加，并且有一条测试专门钉住它
  （[[problems-snake-and-ladder-extra-turn-is-not-pip-sum]]）。
- 一轮的位移先攒在局部、轮末整体提交，于是「整轮作废」是丢弃而不是撤销
  （[[problems-snake-and-ladder-turn-is-a-transaction]]）。
- 位置由棋局统一持有、没有 `Player` 类，蛇和梯子也不分两个子类；两个"拒绝"都说得出翻转条件
  （[[problems-snake-and-ladder-two-refused-classes]]、[[oop-entity-vs-value-object]]）。
- 新格子效果返回位置变化交给引擎提交，而不是自己改状态；引擎校验效果的输出
  （[[problems-snake-and-ladder-effects-compose]]）。
- 交出去的位置表是先拷贝再包只读的快照，日志是元组，轮数是独立计数器
  （[[oop-getter-collection-leak]]）。
- 测试要么用定死点数的骰子，要么固定种子只断言与种子无关的不变量；没有任何一条"频率在某个
  区间内"的断言（[[problems-snake-and-ladder-testing-without-flakes]]）。
- 模型层一把锁都没有，并且说得出并发真来了锁该加在哪一层、GIL 帮不上什么
  （[[problems-snake-and-ladder-lock-per-game-and-gil]]）。

**题解**：[[solution-snake-and-ladder]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
