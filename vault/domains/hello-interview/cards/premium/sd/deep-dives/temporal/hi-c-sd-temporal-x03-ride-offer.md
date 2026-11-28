---
id: hi-c-sd-temporal-x03-ride-offer
node: sd.deep-dives.temporal.exam
type: qa
step: 3
---
## Q
**Temporal · 用 Workflow 实现"逐个司机发单"**｜考点 · 必会

乘客叫车，系统按距离排序候选司机，逐个发出订单：每位司机有 10 秒响应，拒绝或超时就换下一位，乘客中途取消要立刻停止。用 Temporal 的概念画出这个 Workflow，并说明状态存在哪里。

## A
- **Workflow：** 循环遍历候选司机；对每位：调用 Activity 向司机推送订单，然后等待"司机响应 Signal 或 10 秒计时器"，先到者胜；接受则调用 Activity 完成匹配并结束；拒绝或超时则下一位。
- **Signal：** 司机的接受或拒绝通过 Signal 送给对应 Workflow；乘客取消也是一个 Signal，Workflow 收到后停止循环并通知当前司机撤销。
- **计时器：** 10 秒等待用持久计时器，不占 worker，服务重启不丢。
- **状态存在哪：** Workflow 的局部变量（候选列表、当前下标）通过重放从事件历史重建；不需要自己建状态表。
- **要点：** 司机推送要幂等（可能重试），候选列表如何得到放进 Activity，保证 Workflow 本身确定性。
- **对照：** 若不用 Temporal，你要自己存"当前轮到谁""何时超时"，并有后台任务扫描超时，正是它替你做的事。
