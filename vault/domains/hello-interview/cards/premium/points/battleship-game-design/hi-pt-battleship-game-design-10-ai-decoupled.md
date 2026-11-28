---
id: hi-pt-battleship-game-design-10-ai-decoupled
node: qb.lld.battleship-game-design.points
type: qa
step: 10
---
## Q
**海战棋 · AI 与引擎解耦**｜加分 · 出自：海战棋 › 深入 7

要加 AI 对手或网络对战，引擎 `Game` 要不要改？AI 通过什么与它交互？

## A
**不用改。** 对战循环放在 `Game` 之外，AI 只通过 `board_view` 和 `fire` 说话：输入是它能看到的棋盘，输出是下一发坐标。

**联网。** 服务器是唯一的裁判，客户端只拿到 `board_view`，永远拿不到对手的内部状态。

**回放。** 把每个成功的操作记成事件，状态由事件重放得到。
