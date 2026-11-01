---
id: hi-lld-connect-four-2-entities
node: lld.problem-breakdowns.connect-four
type: qa
step: 2
---
## Q
**实体与职责划分**｜低层设计 · 题目拆解

四子棋里 Game、Board、Player 三个类各管什么？为什么不把所有东西塞进一个类？

## A
**要点。**

| 类 | 职责 | 不管 |
|---|---|---|
| Game | 调度者：持有 Board，记录轮到谁、游戏状态；校验后叫 Board 落子，判胜负，换人 | 网格数学 |
| Board | 网格状态、落子（子如何下坠）、列是否满、是否连成四子 | 轮到谁、谁赢了 |
| Player | 纯数据：名字和棋色 | 任何游戏逻辑 |

**为什么。** 单一职责（single responsibility）：规则分两层，Game 管游戏规则（回合、状态），Board 管物理规则（边界、落点、连线），各自单独好测。

**易错。** 反方向的毛病是拆得过碎：只有名字和颜色的 Player 不需要接口和子类。
