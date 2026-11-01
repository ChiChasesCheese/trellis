---
id: hi-lld-delivery-4-class-design
node: qb.lld.beverage-vending-system.pre-lld-in-a-hurry-delivery
type: qa
step: 4
---
## Q
**第三步：从需求推出类的状态与行为**｜低层设计 · 速览

类设计阶段怎么从需求推出每个类的状态（state）和行为（behavior）？“Tell, Don't Ask” 规则放在哪个类？为什么不画 UML？

## A
**顺序。** 自顶向下：先协调者（如 Game），再支撑实体（Board、Player）。每个类回答两个问题：它要记住什么才能满足需求（状态），它要做什么（行为）。把需求映射成表，避免臆测和臃肿。

**例子（Game）。**
- “轮流落子” → 要记两个玩家、轮到谁、棋盘
- “获胜或棋盘满则结束” → 要记游戏状态（进行中、获胜、平局）和赢家
- 行为：`makeMove(player, row, col)` 返回布尔、`getCurrentPlayer()`、`getGameState()`、`getWinner()`、`getBoard()`

**规则放哪。** 规则跟着拥有相关状态的实体走，也就是封装，即 Tell, Don't Ask：对象管理自己的状态并暴露行为，而不是只给 getter 让调用方做判断。流程和生命周期规则（“现在能不能执行这个操作”）放协调者；数据相关规则（“这格是否已被占用”）放拥有数据的实体。出问题时一眼就知道查哪个类。

**取舍。** 不用 UML：它为检查和运行代码很昂贵的年代而设计，如今工程师直接用代码设计（写类的骨架、用接口），微软 2016 年就在 Visual Studio 里移除了 UML 工具。面试里边想边改，形式感只会拖慢你。如果面试官明确要求，先问简化的类表示可否。
