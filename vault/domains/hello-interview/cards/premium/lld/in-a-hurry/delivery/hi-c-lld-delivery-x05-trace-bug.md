---
id: hi-c-lld-delivery-x05-trace-bug
node: lld.in-a-hurry.delivery.exam
type: qa
step: 5
---
## Q
**LLD 答题框架 · 验证能抓到什么**｜考点 · 必会

一个落子方法先把当前玩家换成对手，再检查是否获胜并把 `winner` 设为 `current_player`。用一次落子走一遍，会发现什么？

## A
- 走：X 落子，换人后 `current_player` 是 O，获胜检测通过，`winner` 被写成 O
- **结果：** 赢家与实际相反
- **根因：** 状态转换顺序错
- **修法：** 先判胜负并用落子的 `player` 记赢家，只有游戏还在进行时才换人
- 这类错误靠"初始状态 → 每步状态"的逐步跟踪最容易暴露
