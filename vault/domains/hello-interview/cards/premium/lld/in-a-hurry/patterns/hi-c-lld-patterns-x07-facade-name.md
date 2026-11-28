---
id: hi-c-lld-patterns-x07-facade-name
node: lld.in-a-hurry.patterns.exam
type: qa
step: 7
---
## Q
**设计模式 · 被问到"你用了 Facade 吗"**｜考点 · 必会

你的 `Game` 类协调了 `Board`、`Player` 和状态。面试官问"这是什么模式"，怎么答？

## A
- **答：** 这是门面（Facade），一个协调者，对外只暴露 `make_move`、`get_state`
- **不要：** 先宣布"我用了 Facade 模式"，再去构造一个没必要的门面
- **价值：** 调用方不需要懂内部协作；规则（回合、结束）集中在这里
- **边界：** 门面不该吞掉各组件自己的数据规则，那是 `Board` 的事
