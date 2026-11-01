---
id: hi-lld-connect-four-3-game-state
node: lld.problem-breakdowns.connect-four
type: qa
step: 3
---
## Q
**游戏状态：布尔标志 vs 枚举**｜低层设计 · 题目拆解

用 `isOver`、`hasWinner`、`isDraw` 三个布尔值表示游戏状态，有什么问题？更好的表示是什么？

## A
**要点。** 领域里只有三种状态（进行中、获胜、平局），三个布尔值却有 8 种组合，其中 `isOver=false` 却 `hasWinner=true`、或同时赢又平，都是非法的，类型系统拦不住，每次更新都要靠人记得同步全部标志。

改成一个枚举 `GameState { IN_PROGRESS, WON, DRAW }`：「不可能同时赢和平」直接由结构保证（让非法状态无法表示，make invalid states unrepresentable）。调用方写 `state == WON` 意图清楚，将来加 PAUSED 也只多一个枚举值。

**取舍。** 还留一个漏洞：`winner` 字段仍可能与 `state` 不一致。理想做法是让 WON 携带获胜者，Rust、Swift、Kotlin 的 sealed class、TypeScript 的可辨识联合都支持；Java、Python 不方便，面试里用「枚举加可空 winner」即可，提一句理想形态展示深度，不必硬做。
