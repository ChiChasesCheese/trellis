---
id: hi-c-lld-delivery-x06-map-extension
node: lld.in-a-hurry.delivery.exam
type: qa
step: 6
---
## Q
**LLD 答题框架 · 扩展点对应关系**｜考点 · 追问

井字棋设计写完，面试官依次问"加撤销""加 AI 对手""棋盘改成 N×N"。各自应该指向设计里的哪里？

## A
- **撤销：** 状态变更集中在 `makeMove`，加命令历史栈
- **AI 对手：** 新增一个会选落点的玩家，`Game` 只调用 `makeMove`，不改规则代码
- **N×N：** 尺寸原本在范围外，`Board` 把尺寸做成构造参数，胜负检测要同步泛化
- **提醒：** 范围外清单里的项最容易成为追问，所以第一步要写清楚
