---
id: hi-c-lld-connect-four-n08-game-api
node: lld.problem-breakdowns.connect-four.notes
type: qa
step: 8
---
## Q
**四子棋 · Game 的字段与接口**｜摘要 · 必会

`Game` 最终有哪些字段和方法？为什么 `makeMove` 是唯一改变状态的方法？

## A
- **字段：** 棋盘、两名玩家、当前玩家、状态枚举、赢家；赢家可为空，因为平局或进行中本来就没有赢家，用"空"表达比塞一个特殊的"无人"值更直白。
- **构造：** `Game(p1, p2)` 让玩家 1 先手，状态设为进行中，赢家为空。
- **唯一的写入口：** `makeMove(player, column) -> bool` 是唯一会改变状态的方法，所以所有规则（回合、结束、非法走法）都集中在这里，出问题只需查这一处。
- **其余只读：** `getCurrentPlayer`、`getGameState`、`getWinner`、`getBoard` 让界面和调用方读取信息，而不必自己重复实现回合逻辑。
