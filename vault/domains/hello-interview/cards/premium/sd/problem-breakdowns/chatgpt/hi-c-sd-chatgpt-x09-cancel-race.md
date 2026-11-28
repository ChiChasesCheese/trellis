---
id: hi-c-sd-chatgpt-x09-cancel-race
node: sd.problem-breakdowns.chatgpt.exam
type: qa
step: 9
---
## Q
**ChatGPT · 排错：取消和完成同时到达**｜考点 · 追问

工作者刚写完 `done`，几乎同时用户的取消请求把 Run 改成 cancelled。或者相反。最终记录会错在哪里？怎么保证状态一致？

## A
- **错在哪里：** 两个写入者各自无条件 `UPDATE runs SET status=…`，后写的覆盖先写的。助手消息已完整保存，Run 却显示 cancelled；或 Run 显示 done，但用户已经按了停止并以为不会计费。
- **修法：** 状态转换做成**条件更新**：`UPDATE runs SET status='cancelled' WHERE runId=? AND status IN ('queued','streaming')`，受影响行数为 0 说明已到终态，取消无效，把这个结果如实告诉用户。完成同理：`… SET status='done' WHERE status='streaming'`。
- **模式。** 转换表状态机：只允许 queued→streaming→{done, cancelled, failed} 这些合法边，终态之后不能再改。
- **计费：** 用写入时记录的实际输出 token 数结算，与状态无关。
- **控制信号：** 取消信号发布后，工作者可能已经完成，要容忍对已结束 Run 的取消信号并忽略。
