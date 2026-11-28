---
id: hi-c-sd-multi-step-processes-n17-external-events-deepdive
node: sd.patterns.multi-step-processes.notes
type: qa
step: 18
---
## Q
**多步流程 · 追问：怎么处理外部事件和长时间等待**｜摘要 · 追问

等客户签字可能 5 分钟也可能 5 天，怎么高效地等、超时怎么处理？

## A
- **机制：** 工作流用信号（signal）接收外部事件。注册信号处理函数，发出签字请求，然后 `condition(() => signature !== undefined, '30 days')` 等待，带超时。
- **超时流程：** 30 天没收到就发提醒，再等 7 天，仍没有就取消文档；收到就处理签字。
- **外部系统如何投递：** 签字服务的 webhook 触发时，处理程序用工作流 ID 调引擎 API，引擎唤醒对应的执行。
- **等待期间：** 工作流不占线程、不占 worker 内存，只有持久化的状态和一个持久的定时器。
- **适用：** 人工任务、webhook 回调、对接外部系统。
